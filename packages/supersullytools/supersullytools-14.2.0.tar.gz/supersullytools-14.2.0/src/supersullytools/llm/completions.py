from abc import ABC
from base64 import b64decode
from datetime import datetime, timezone
from logging import Logger
from typing import TYPE_CHECKING, Literal, Optional, TypeVar, Union

import boto3
import openai
from pydantic import AwareDatetime, BaseModel, computed_field

if TYPE_CHECKING:
    from mypy_boto3_bedrock_runtime import BedrockRuntimeClient
    from openai import Client

    from supersullytools.llm.trackers import CompletionTracker, UsageStats


class PromptMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ImagePromptMessage(BaseModel):
    role: Literal["user"] = "user"
    content: str
    images: list[str]  # images in base64 encoded format
    image_formats: list[Literal["jpeg", "png"]]


class CompletionModel(BaseModel, ABC):
    provider: str
    make: str
    llm: str
    llm_id: str
    input_price_per_1k: float
    output_price_per_1k: float

    cached_input_price_per_1k: Optional[float] = None
    supports_images: bool


class CompletionResponse(BaseModel):
    content: str
    input_tokens: int
    cached_input_tokens: int = 0
    reasoning_tokens: int = 0
    output_tokens: int
    llm_metadata: CompletionModel
    generated_at: AwareDatetime
    response_metadata: Optional[dict] = None
    stop_reason: str
    completion_time_ms: int

    @computed_field
    @property
    def completion_cost(self) -> float:
        if self.cached_input_tokens and self.llm_metadata.cached_input_price_per_1k:
            input_tokens = self.input_tokens
            cached_input_tokens = self.cached_input_tokens
            regular_cost = ((input_tokens - cached_input_tokens) / 1000) * self.llm_metadata.input_price_per_1k
            cached_cost = (cached_input_tokens / 1000) * self.llm_metadata.cached_input_price_per_1k
            input_cost = regular_cost + cached_cost
        else:
            input_cost = self.input_tokens / 1000 * self.llm_metadata.input_price_per_1k
        output_cost = self.output_tokens / 1000 * self.llm_metadata.output_price_per_1k
        return round(input_cost + output_cost, 4)


class PromptAndResponse(BaseModel):
    prompt: list[PromptMessage | ImagePromptMessage]
    response: CompletionResponse


class OpenAiModel(CompletionModel):
    provider: Literal["OpenAI"] = "OpenAI"
    supports_system_msgs: bool = True


class OllamaModel(CompletionModel):
    provider: Literal["Ollama"] = "Ollama"
    make: str = "Ollama"
    supports_system_msgs: bool = True

    input_price_per_1k: float = 0.0
    output_price_per_1k: float = 0.0


class BedrockCompletionResponse(BaseModel):
    """A helper class to use with parsing bedrock responses from AWS"""

    content: str
    input_tokens: int
    output_tokens: int


class BedrockModel(CompletionModel):
    provider: Literal["AWS Bedrock"] = "AWS Bedrock"


CompletionModelType = TypeVar("CompletionModelType", bound=CompletionModel)


class CompletionHandler:
    def __init__(
        self,
        logger: Logger,
        openai_client: Optional["Client"] = None,
        bedrock_runtime_client: Optional["BedrockRuntimeClient"] = None,
        # models to use, defaults to all standard otherwise
        available_models: Optional[list["CompletionModel"]] = None,
        # extra models to add to above, useful for adding custom models to the standard list
        extra_models: Optional[list["CompletionModel"]] = None,
        completion_tracker: Optional["CompletionTracker"] = None,
        debug_output_prompt_and_response=False,
        enable_openai=True,
        enable_bedrock=True,
        enable_ollama=False,
        ollama_address=None,
        ollama_use_https=False,
        ollama_load_dynamic_models=True,
        default_max_response_tokens: int = 1000,
    ):
        self.logger = logger
        self.enable_openai = enable_openai
        self.enable_bedrock = enable_bedrock
        self.enable_ollama = enable_ollama

        self.completion_tracker = completion_tracker

        self.openai_client = None
        if self.enable_openai:
            self.openai_client = openai_client or openai.Client()

        self.bedrock_runtime_client = None
        if self.enable_bedrock:
            self.bedrock_runtime_client = bedrock_runtime_client or boto3.client("bedrock-runtime")

        if self.enable_ollama:
            if ollama_address is None:
                raise ValueError("Must specify ollama_address when enable_ollama is True")
            s = "s" if ollama_use_https else ""
            self.ollama_client = openai.Client(base_url=f"http{s}://{ollama_address}/v1", api_key="ollama")

        self.debug_output_prompt_and_response = debug_output_prompt_and_response
        if available_models:
            self.available_models = available_models
        else:
            if enable_bedrock and enable_openai:
                self.available_models = DEFAULT_USE_MODELS
            elif enable_bedrock:
                self.available_models = [x for x in DEFAULT_USE_MODELS if isinstance(x, BedrockModel)]
            elif enable_openai:
                self.available_models = [x for x in DEFAULT_USE_MODELS if isinstance(x, OpenAiModel)]
            else:
                # what do?
                raise ValueError("No models specified")
            # add ollama models from the server
            if enable_ollama and ollama_load_dynamic_models:
                ollama_models = []
                for idx, model in enumerate(self.ollama_client.models.list()):
                    ollama_models.append(OllamaModel(llm=model.id, llm_id=model.id, supports_images=True))
                self.available_models += ollama_models

        self.default_max_response_tokens = default_max_response_tokens

    def get_model_by_name_or_id(self, model_name_or_id: str) -> "CompletionModelType":
        try:
            return next(x for x in self.available_models if x.llm == model_name_or_id)
        except StopIteration:
            try:
                return next(x for x in self.available_models if x.llm_id == model_name_or_id)
            except StopIteration:
                raise ValueError(f"No model found {model_name_or_id=}") from None

    def get_completion(
        self,
        model: Union[str, "CompletionModel"],
        prompt: str | list[PromptMessage | ImagePromptMessage],
        max_response_tokens: Optional[int] = None,
        extra_trackers: Optional[list["UsageStats"]] = None,
    ) -> "CompletionResponse":
        if max_response_tokens is None:
            max_response_tokens = self.default_max_response_tokens
        if isinstance(model, str):
            model = self.get_model_by_name_or_id(model)

        if isinstance(prompt, str):
            prompt = [PromptMessage(content=prompt, role="user")]

        match model:
            case OpenAiModel():
                response = self._get_openai_completion(model, prompt, max_response_tokens)
            case BedrockModel():
                response = self._get_bedrock_completion(model, prompt, max_response_tokens)
            case OllamaModel():
                response = self._get_ollama_completion(model, prompt, max_response_tokens)
            case _:
                raise ValueError(model)
        try:
            if self.completion_tracker:
                self.completion_tracker.track_completion(model, prompt, response)
        except Exception:
            self.logger.warning("Error tracking completion! Continuing", exc_info=True)

        try:
            if extra_trackers:
                if self.completion_tracker:
                    self.completion_tracker.track_completion(
                        model, prompt, response, override_trackers=extra_trackers, store_prompt_and_response=False
                    )
                else:
                    self.logger.warning("Extra trackers provided but no completion tracker configured!")
        except Exception:
            self.logger.warning("Error with extra trackers! Continuing", exc_info=True)

        self.logger.debug("Completion generated\n" + response.model_dump_json(indent=2, exclude={"content"}))

        return response

    def _get_bedrock_completion(
        self,
        llm: BedrockModel,
        prompt: list[PromptMessage | ImagePromptMessage],
        max_response_tokens: int,
        temperature=0.0,
    ) -> "CompletionResponse":
        prompt = [] or prompt
        if not self.enable_bedrock:
            raise RuntimeError("Bedrock completions disabled!")
        # boto_input = llm.prepare_bedrock_body(prompt, max_response_tokens)

        self.logger.info(f"Generating Bedrock Completion {llm.llm_id}")

        # Invoke Bedrock API

        if prompt[0].role == "system":
            system_msg = prompt[0]
            prompt = prompt[1:]
        else:
            system_msg = None

        started_at = datetime.now(timezone.utc)
        messages = []
        debug_print_messages = []
        for msg in prompt:
            add_role = "user" if msg.role == "system" else msg.role
            debug_print_messages.append({"role": add_role, "content": [{"text": msg.content}]})
            match msg:
                case PromptMessage():
                    messages.append({"role": add_role, "content": [{"text": msg.content}]})
                case ImagePromptMessage():
                    if not llm.supports_images:
                        raise ValueError("Specified model does not have image prompt support")
                    content = [{"text": msg.content}]
                    for image, image_fmt in zip(msg.images, msg.image_formats):
                        content.append({"image": {"format": image_fmt, "source": {"bytes": b64decode(image)}}})
                    messages.append(
                        {
                            "role": add_role,
                            "content": content,
                        }
                    )
                case _:
                    raise ValueError("Bad prompt type")

        if self.debug_output_prompt_and_response:
            self.logger.debug(f"LLM input:\n{messages}")

        if system_msg:
            system_prompt = [{"text": system_msg.content}]
        else:
            system_prompt = []
        bedrock_response = self.bedrock_runtime_client.converse(
            modelId=llm.llm_id,
            messages=messages,
            system=system_prompt,
            inferenceConfig={"temperature": temperature, "maxTokens": max_response_tokens},
            # additionalModelRequestFields=additional_model_fields,
        )

        # return response
        response_body = bedrock_response["output"]["message"]["content"][0]["text"].strip()
        finished_at = datetime.now(timezone.utc)
        self.logger.info("Generation complete")
        if self.debug_output_prompt_and_response:
            self.logger.debug(f"LLM Response:\n{bedrock_response}")

        token_usage = bedrock_response["usage"]
        input_tokens = token_usage["inputTokens"]
        output_tokens = token_usage["outputTokens"]
        # total_tokens = token_usage["totalTokens"]
        # stop_reason = bedrock_response["stopReason"]

        return CompletionResponse(
            content=response_body,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            llm_metadata=CompletionModel.model_validate(llm, from_attributes=True),
            generated_at=finished_at,
            completion_time_ms=int((finished_at - started_at).total_seconds() * 1000),
            stop_reason=bedrock_response["stopReason"],
            response_metadata={"usage": bedrock_response["usage"], "metrics": bedrock_response["metrics"]},
        )

    def _get_ollama_completion(
        self, llm: OpenAiModel, prompt: list[PromptMessage | ImagePromptMessage], max_response_tokens: int
    ) -> "CompletionResponse":
        if not self.enable_ollama:
            raise RuntimeError("Ollama completions disabled!")
        chat_history = []
        debug_print_chat_history = []
        for msg in prompt:
            debug_print_chat_history.append({"role": msg.role, "content": msg.content})
            if msg.role == "system":
                role = msg.role if llm.supports_system_msgs else "user"
            else:
                role = msg.role
            match msg:
                case PromptMessage():
                    chat_history.append({"role": role, "content": msg.content})
                case ImagePromptMessage():
                    content = [{"type": "text", "text": msg.content}]
                    debug_print_chat_history.append({"role": role, "content": msg.content, "include_image": True})
                    for image, image_fmt in zip(msg.images, msg.image_formats):
                        content.append(
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/{image_fmt};base64,{image}"},
                            }
                        )
                    chat_history.append(
                        {
                            "role": role,
                            "content": content,
                        }
                    )
                case _:
                    raise ValueError("Base prompt type")
        started_at = datetime.now(timezone.utc)

        self.logger.info("Generating Open AI ChatCompletion")
        if self.debug_output_prompt_and_response:
            self.logger.debug(f"LLM input:\n{chat_history}")
        openai_response = self.ollama_client.chat.completions.create(
            model=llm.llm_id, messages=chat_history, max_completion_tokens=max_response_tokens
        )
        if self.debug_output_prompt_and_response:
            self.logger.debug(f"LLM response:\n{openai_response}")
        finished_at = datetime.now(timezone.utc)

        return CompletionResponse(
            content=openai_response.choices[0].message.content,
            input_tokens=openai_response.usage.prompt_tokens,
            # reasoning_tokens=openai_response.usage.completion_tokens_details.reasoning_tokens or 0,
            # cached_input_tokens=openai_response.usage.prompt_tokens_details.cached_tokens or 0,
            output_tokens=openai_response.usage.completion_tokens,
            llm_metadata=CompletionModel.model_validate(llm, from_attributes=True),
            generated_at=finished_at,
            stop_reason=openai_response.choices[0].finish_reason,
            response_metadata=openai_response.model_dump(mode="json", exclude={"choices"}),
            completion_time_ms=int((finished_at - started_at).total_seconds() * 1000),
        )

    def _get_openai_completion(
        self, llm: OpenAiModel, prompt: list[PromptMessage | ImagePromptMessage], max_response_tokens: int
    ) -> "CompletionResponse":
        if not self.enable_openai:
            raise RuntimeError("OpenAI completions disabled!")
        chat_history = []
        debug_print_chat_history = []
        for msg in prompt:
            debug_print_chat_history.append({"role": msg.role, "content": msg.content})
            if msg.role == "system":
                role = msg.role if llm.supports_system_msgs else "user"
            else:
                role = msg.role
            match msg:
                case PromptMessage():
                    chat_history.append({"role": role, "content": msg.content})
                case ImagePromptMessage():
                    content = [{"type": "text", "text": msg.content}]
                    debug_print_chat_history.append({"role": role, "content": msg.content, "include_image": True})
                    for image, image_fmt in zip(msg.images, msg.image_formats):
                        content.append(
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/{image_fmt};base64,{image}"},
                            }
                        )
                    chat_history.append(
                        {
                            "role": role,
                            "content": content,
                        }
                    )
                case _:
                    raise ValueError("Base prompt type")
        started_at = datetime.now(timezone.utc)

        self.logger.info("Generating Open AI ChatCompletion")
        if self.debug_output_prompt_and_response:
            self.logger.debug(f"LLM input:\n{chat_history}")
        openai_response = self.openai_client.chat.completions.create(
            model=llm.llm_id, messages=chat_history, max_completion_tokens=max_response_tokens
        )
        if self.debug_output_prompt_and_response:
            self.logger.debug(f"LLM response:\n{openai_response}")
        finished_at = datetime.now(timezone.utc)

        return CompletionResponse(
            content=openai_response.choices[0].message.content,
            input_tokens=openai_response.usage.prompt_tokens,
            reasoning_tokens=openai_response.usage.completion_tokens_details.reasoning_tokens or 0,
            cached_input_tokens=openai_response.usage.prompt_tokens_details.cached_tokens or 0,
            output_tokens=openai_response.usage.completion_tokens,
            llm_metadata=CompletionModel.model_validate(llm, from_attributes=True),
            generated_at=finished_at,
            stop_reason=openai_response.choices[0].finish_reason,
            response_metadata=openai_response.model_dump(mode="json", exclude={"choices"}),
            completion_time_ms=int((finished_at - started_at).total_seconds() * 1000),
        )


class Gpt3p5Turbo(OpenAiModel):
    make: str = "OpenAI"
    llm: str = "GPT 3.5 Turbo"
    llm_id: str = "gpt-3.5-turbo"
    input_price_per_1k: float = 0.000500
    output_price_per_1k: float = 0.001500
    supports_images: bool = False


class Gpt4Turbo(OpenAiModel):
    make: str = "OpenAI"
    llm: str = "GPT 4 Turbo"
    llm_id: str = "gpt-4-turbo"
    input_price_per_1k: float = 0.010000
    output_price_per_1k: float = 0.030000
    supports_images: bool = True


class Gpt4Omni(OpenAiModel):
    make: str = "OpenAI"
    llm: str = "GPT 4 Omni"
    llm_id: str = "gpt-4o"
    input_price_per_1k: float = 0.0025
    cached_input_price_per_1k: float = 0.00125
    output_price_per_1k: float = 0.01
    supports_images: bool = True


class Gpt4OmniSearchPreview(OpenAiModel):
    make: str = "OpenAI"
    llm: str = "GPT 4 Omni - Search Preview"
    llm_id: str = "gpt-4o-search-preview"
    input_price_per_1k: float = 0.0025
    # cached_input_price_per_1k: float = 0.00125
    output_price_per_1k: float = 0.01
    supports_images: bool = True


class Gpt4OmniMini(OpenAiModel):
    make: str = "OpenAI"
    llm: str = "GPT 4 Omni Mini"
    llm_id: str = "gpt-4o-mini"
    input_price_per_1k: float = 0.000150
    cached_input_price_per_1k: float = 0.000075
    output_price_per_1k: float = 0.0006
    supports_images: bool = True


class Gpt4OmniMiniSearchPreview(OpenAiModel):
    make: str = "OpenAI"
    llm: str = "GPT 4 Omni Mini - Search Preview"
    llm_id: str = "gpt-4o-mini-search-preview"
    input_price_per_1k: float = 0.000150
    # cached_input_price_per_1k: float = 0.000075
    output_price_per_1k: float = 0.0006
    supports_images: bool = True


class OpenAIO1Preview(OpenAiModel):
    make: str = "OpenAI"
    llm: str = "o1-preview"
    llm_id: str = "o1-preview"
    input_price_per_1k: float = 0.015
    cached_input_price_per_1k: float = 0.0075
    output_price_per_1k: float = 0.06
    supports_images: bool = False
    supports_system_msgs: bool = False


class OpenAIO1Mini(OpenAiModel):
    make: str = "OpenAI"
    llm: str = "o1-mini"
    llm_id: str = "o1-mini"
    input_price_per_1k: float = 0.003
    cached_input_price_per_1k: float = 0.0015
    output_price_per_1k: float = 0.012
    supports_images: bool = False
    supports_system_msgs: bool = False


class Llama2Chat13B(BedrockModel):
    make: str = "Meta"
    llm: str = "Llama 2 Chat 13B"
    llm_id: str = "meta.llama2-13b-chat-v1"
    input_price_per_1k: float = 0.000750
    output_price_per_1k: float = 0.001000
    supports_images: bool = False


class Llama3p1Instruct8B(Llama2Chat13B):
    make: str = "Meta"
    llm: str = "Llama 3.1 Instruct 8B"
    llm_id: str = "meta.llama3-1-8b-instruct-v1:0"
    input_price_per_1k: float = 0.00022
    output_price_per_1k: float = 0.00022
    supports_images: bool = False


class Llama3p1Instruct70B(Llama2Chat13B):
    make: str = "Meta"
    llm: str = "Llama 3.1 Instruct 70B"
    llm_id: str = "meta.llama3-1-70b-instruct-v1:0"
    input_price_per_1k: float = 0.00099
    output_price_per_1k: float = 0.00099
    supports_images: bool = False


class Llama3p1Instruct405B(Llama2Chat13B):
    make: str = "Meta"
    llm: str = "Llama 3.1 Instruct 405B"
    llm_id: str = "meta.llama3-1-405b-instruct-v1:0"
    input_price_per_1k: float = 0.00532
    output_price_per_1k: float = 0.00532
    supports_images: bool = False


class Claude3Sonnet(BedrockModel):
    make: str = "Anthropic"
    llm: str = "Claude 3 Sonnet"
    llm_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    input_price_per_1k: float = 0.003
    output_price_per_1k: float = 0.015
    supports_images: bool = True


class Claude3p5Sonnet(BedrockModel):
    make: str = "Anthropic"
    llm: str = "Claude 3.5 Sonnet"
    llm_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    input_price_per_1k: float = 0.003
    output_price_per_1k: float = 0.015
    supports_images: bool = True


class Claude3p5SonnetV2(BedrockModel):
    make: str = "Anthropic"
    llm: str = "Claude 3.5 Sonnet V2"
    llm_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0"
    input_price_per_1k: float = 0.003
    output_price_per_1k: float = 0.015
    supports_images: bool = True


class Claude3Haiku(Claude3Sonnet):
    make: str = "Anthropic"
    llm: str = "Claude 3 Haiku"
    llm_id: str = "anthropic.claude-3-haiku-20240307-v1:0"
    input_price_per_1k: float = 0.00025
    output_price_per_1k: float = 0.00125
    supports_images: bool = True


class Claude3p5Haiku(Claude3Sonnet):
    make: str = "Anthropic"
    llm: str = "Claude 3.5 Haiku"
    llm_id: str = "anthropic.claude-3-5-haiku-20241022-v1:0"
    input_price_per_1k: float = 0.001
    output_price_per_1k: float = 0.005
    supports_images: bool = True


class Claude3Opus(Claude3Sonnet):
    make: str = "Anthropic"
    llm: str = "Claude 3 Opus"
    llm_id: str = "anthropic.claude-3-opus-20240229-v1:0"
    input_price_per_1k: float = 0.015
    output_price_per_1k: float = 0.075
    supports_images: bool = True


class Mistral7B(BedrockModel):
    make: str = "Mistral AI"
    llm: str = "Mistral 7B Instruct"
    llm_id: str = "mistral.mistral-7b-instruct-v0:2"
    input_price_per_1k: float = 0.000150
    output_price_per_1k: float = 0.000200
    supports_images: bool = False


class Mixtral8x7B(Mistral7B):
    make: str = "Mistral AI"
    llm: str = "Mixtral 8x7B Instruct"
    llm_id: str = "mistral.mixtral-8x7b-instruct-v0:1"
    input_price_per_1k: float = 0.000450
    output_price_per_1k: float = 0.000700
    supports_images: bool = False


ALL_MODELS = [
    Gpt3p5Turbo(),
    Gpt4Omni(),
    Gpt4OmniSearchPreview(),
    Gpt4OmniMini(),
    Gpt4OmniMiniSearchPreview(),
    Gpt4Turbo(),
    OpenAIO1Preview(),
    OpenAIO1Mini(),
    Gpt4Turbo(),
    Llama2Chat13B(),
    Llama3p1Instruct8B(),
    Llama3p1Instruct70B(),
    Llama3p1Instruct405B(),
    Mistral7B(),
    Mixtral8x7B(),
    Claude3Haiku(),
    Claude3p5Haiku(),
    Claude3Sonnet(),
    Claude3p5Sonnet(),
    Claude3p5SonnetV2(),
    Claude3Opus(),
]

DEFAULT_USE_MODELS = [
    Gpt4Omni(),
    Gpt4OmniSearchPreview(),
    Gpt4OmniMini(),
    Gpt4OmniMiniSearchPreview(),
    Gpt4Turbo(),
    OpenAIO1Preview(),
    OpenAIO1Mini(),
    Claude3Haiku(),
    Claude3p5Haiku(),
    Claude3p5Sonnet(),
    Claude3p5SonnetV2(),
    Claude3Opus(),
]
