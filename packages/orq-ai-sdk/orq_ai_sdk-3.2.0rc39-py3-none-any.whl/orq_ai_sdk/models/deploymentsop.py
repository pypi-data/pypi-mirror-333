"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from orq_ai_sdk.types import (
    BaseModel,
    Nullable,
    OptionalNullable,
    UNSET,
    UNSET_SENTINEL,
)
from orq_ai_sdk.utils import FieldMetadata, QueryParamMetadata
import pydantic
from pydantic import model_serializer
from typing import Any, Dict, List, Literal, Optional, Union
from typing_extensions import Annotated, NotRequired, TypeAliasType, TypedDict


Sort = Literal["asc", "desc"]
r"""List sorting preference."""


class DeploymentsRequestTypedDict(TypedDict):
    sort: NotRequired[Sort]
    r"""List sorting preference."""
    limit: NotRequired[float]
    r"""A limit on the number of objects to be returned. Limit can range between 1 and 50, and the default is 10"""
    starting_after: NotRequired[str]
    r"""A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 20 objects, ending with `01JJ1HDHN79XAS7A01WB3HYSDB`, your subsequent call can include `after=01JJ1HDHN79XAS7A01WB3HYSDB` in order to fetch the next page of the list."""
    ending_before: NotRequired[str]
    r"""A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 20 objects, starting with `01JJ1HDHN79XAS7A01WB3HYSDB`, your subsequent call can include `before=01JJ1HDHN79XAS7A01WB3HYSDB` in order to fetch the previous page of the list."""


class DeploymentsRequest(BaseModel):
    sort: Annotated[
        Optional[Sort],
        FieldMetadata(query=QueryParamMetadata(style="form", explode=True)),
    ] = "asc"
    r"""List sorting preference."""

    limit: Annotated[
        Optional[float],
        FieldMetadata(query=QueryParamMetadata(style="form", explode=True)),
    ] = 10
    r"""A limit on the number of objects to be returned. Limit can range between 1 and 50, and the default is 10"""

    starting_after: Annotated[
        Optional[str],
        FieldMetadata(query=QueryParamMetadata(style="form", explode=True)),
    ] = None
    r"""A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 20 objects, ending with `01JJ1HDHN79XAS7A01WB3HYSDB`, your subsequent call can include `after=01JJ1HDHN79XAS7A01WB3HYSDB` in order to fetch the next page of the list."""

    ending_before: Annotated[
        Optional[str],
        FieldMetadata(query=QueryParamMetadata(style="form", explode=True)),
    ] = None
    r"""A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 20 objects, starting with `01JJ1HDHN79XAS7A01WB3HYSDB`, your subsequent call can include `before=01JJ1HDHN79XAS7A01WB3HYSDB` in order to fetch the previous page of the list."""


Object = Literal["list"]

DeploymentsType = Literal["function"]
r"""The type of the tool. Currently, only `function` is supported."""

DeploymentsDeploymentsResponseType = Literal["object"]


class DeploymentsParametersTypedDict(TypedDict):
    r"""The parameters the functions accepts, described as a JSON Schema object.

    Omitting `parameters` defines a function with an empty parameter list.
    """

    type: DeploymentsDeploymentsResponseType
    properties: Dict[str, Any]
    required: NotRequired[List[str]]
    additional_properties: NotRequired[bool]


class DeploymentsParameters(BaseModel):
    r"""The parameters the functions accepts, described as a JSON Schema object.

    Omitting `parameters` defines a function with an empty parameter list.
    """

    type: DeploymentsDeploymentsResponseType

    properties: Dict[str, Any]

    required: Optional[List[str]] = None

    additional_properties: Annotated[
        Optional[bool], pydantic.Field(alias="additionalProperties")
    ] = None


class DeploymentsFunctionTypedDict(TypedDict):
    name: str
    r"""The name of the function to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64."""
    parameters: DeploymentsParametersTypedDict
    r"""The parameters the functions accepts, described as a JSON Schema object.

    Omitting `parameters` defines a function with an empty parameter list.
    """
    description: NotRequired[str]
    r"""A description of what the function does, used by the model to choose when and how to call the function."""
    strict: NotRequired[bool]


class DeploymentsFunction(BaseModel):
    name: str
    r"""The name of the function to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64."""

    parameters: DeploymentsParameters
    r"""The parameters the functions accepts, described as a JSON Schema object.

    Omitting `parameters` defines a function with an empty parameter list.
    """

    description: Optional[str] = None
    r"""A description of what the function does, used by the model to choose when and how to call the function."""

    strict: Optional[bool] = None


class DeploymentsToolsTypedDict(TypedDict):
    type: DeploymentsType
    r"""The type of the tool. Currently, only `function` is supported."""
    function: DeploymentsFunctionTypedDict
    id: NotRequired[float]


class DeploymentsTools(BaseModel):
    type: DeploymentsType
    r"""The type of the tool. Currently, only `function` is supported."""

    function: DeploymentsFunction

    id: Optional[float] = None


DeploymentsModelType = Literal[
    "chat",
    "completion",
    "embedding",
    "vision",
    "image",
    "tts",
    "stt",
    "rerank",
    "moderations",
]
r"""The type of the model"""

DeploymentsFormat = Literal["url", "b64_json", "text", "json_object"]
r"""Only supported on `image` models."""

DeploymentsQuality = Literal["standard", "hd"]
r"""Only supported on `image` models."""

DeploymentsResponseFormatType = Literal["json_object"]


class DeploymentsResponseFormat2TypedDict(TypedDict):
    type: DeploymentsResponseFormatType


class DeploymentsResponseFormat2(BaseModel):
    type: DeploymentsResponseFormatType


DeploymentsResponseFormatDeploymentsType = Literal["json_schema"]


class DeploymentsResponseFormatJSONSchemaTypedDict(TypedDict):
    name: str
    strict: bool
    schema_: Dict[str, Any]


class DeploymentsResponseFormatJSONSchema(BaseModel):
    name: str

    strict: bool

    schema_: Annotated[Dict[str, Any], pydantic.Field(alias="schema")]


class DeploymentsResponseFormat1TypedDict(TypedDict):
    type: DeploymentsResponseFormatDeploymentsType
    json_schema: DeploymentsResponseFormatJSONSchemaTypedDict


class DeploymentsResponseFormat1(BaseModel):
    type: DeploymentsResponseFormatDeploymentsType

    json_schema: DeploymentsResponseFormatJSONSchema


DeploymentsResponseFormatTypedDict = TypeAliasType(
    "DeploymentsResponseFormatTypedDict",
    Union[DeploymentsResponseFormat2TypedDict, DeploymentsResponseFormat1TypedDict],
)
r"""An object specifying the format that the model must output.

Setting to `{ \"type\": \"json_schema\", \"json_schema\": {...} }` enables Structured Outputs which ensures the model will match your supplied JSON schema

Setting to `{ \"type\": \"json_object\" }` enables JSON mode, which ensures the message the model generates is valid JSON.

Important: when using JSON mode, you must also instruct the model to produce JSON yourself via a system or user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the token limit, resulting in a long-running and seemingly \"stuck\" request. Also note that the message content may be partially cut off if finish_reason=\"length\", which indicates the generation exceeded max_tokens or the conversation exceeded the max context length.
"""


DeploymentsResponseFormat = TypeAliasType(
    "DeploymentsResponseFormat",
    Union[DeploymentsResponseFormat2, DeploymentsResponseFormat1],
)
r"""An object specifying the format that the model must output.

Setting to `{ \"type\": \"json_schema\", \"json_schema\": {...} }` enables Structured Outputs which ensures the model will match your supplied JSON schema

Setting to `{ \"type\": \"json_object\" }` enables JSON mode, which ensures the message the model generates is valid JSON.

Important: when using JSON mode, you must also instruct the model to produce JSON yourself via a system or user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the token limit, resulting in a long-running and seemingly \"stuck\" request. Also note that the message content may be partially cut off if finish_reason=\"length\", which indicates the generation exceeded max_tokens or the conversation exceeded the max context length.
"""


DeploymentsPhotoRealVersion = Literal["v1", "v2"]
r"""The version of photoReal to use. Must be v1 or v2. Only available for `leonardoai` provider"""

DeploymentsEncodingFormat = Literal["float", "base64"]
r"""The format to return the embeddings"""

DeploymentsReasoningEffort = Literal["low", "medium", "high"]
r"""Constrains effort on reasoning for reasoning models. Reducing reasoning effort can result in faster responses and fewer tokens used on reasoning in a response."""


class DeploymentsModelParametersTypedDict(TypedDict):
    r"""Model Parameters: Not all parameters apply to every model"""

    temperature: NotRequired[float]
    r"""Only supported on `chat` and `completion` models."""
    max_tokens: NotRequired[float]
    r"""Only supported on `chat` and `completion` models."""
    top_k: NotRequired[float]
    r"""Only supported on `chat` and `completion` models."""
    top_p: NotRequired[float]
    r"""Only supported on `chat` and `completion` models."""
    frequency_penalty: NotRequired[float]
    r"""Only supported on `chat` and `completion` models."""
    presence_penalty: NotRequired[float]
    r"""Only supported on `chat` and `completion` models."""
    num_images: NotRequired[float]
    r"""Only supported on `image` models."""
    seed: NotRequired[float]
    r"""Best effort deterministic seed for the model. Currently only OpenAI models support these"""
    format_: NotRequired[DeploymentsFormat]
    r"""Only supported on `image` models."""
    dimensions: NotRequired[str]
    r"""Only supported on `image` models."""
    quality: NotRequired[DeploymentsQuality]
    r"""Only supported on `image` models."""
    style: NotRequired[str]
    r"""Only supported on `image` models."""
    response_format: NotRequired[Nullable[DeploymentsResponseFormatTypedDict]]
    r"""An object specifying the format that the model must output.

    Setting to `{ \"type\": \"json_schema\", \"json_schema\": {...} }` enables Structured Outputs which ensures the model will match your supplied JSON schema

    Setting to `{ \"type\": \"json_object\" }` enables JSON mode, which ensures the message the model generates is valid JSON.

    Important: when using JSON mode, you must also instruct the model to produce JSON yourself via a system or user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the token limit, resulting in a long-running and seemingly \"stuck\" request. Also note that the message content may be partially cut off if finish_reason=\"length\", which indicates the generation exceeded max_tokens or the conversation exceeded the max context length.
    """
    photo_real_version: NotRequired[DeploymentsPhotoRealVersion]
    r"""The version of photoReal to use. Must be v1 or v2. Only available for `leonardoai` provider"""
    encoding_format: NotRequired[DeploymentsEncodingFormat]
    r"""The format to return the embeddings"""
    reasoning_effort: NotRequired[DeploymentsReasoningEffort]
    r"""Constrains effort on reasoning for reasoning models. Reducing reasoning effort can result in faster responses and fewer tokens used on reasoning in a response."""
    budget_tokens: NotRequired[float]
    r"""Gives the model enhanced reasoning capabilities for complex tasks. A value of 0 disables thinking. The minimum budget tokens for thinking are 1024. The Budget Tokens should never exceed the Max Tokens parameter. Only supported by `Anthropic`"""


class DeploymentsModelParameters(BaseModel):
    r"""Model Parameters: Not all parameters apply to every model"""

    temperature: Optional[float] = None
    r"""Only supported on `chat` and `completion` models."""

    max_tokens: Annotated[Optional[float], pydantic.Field(alias="maxTokens")] = None
    r"""Only supported on `chat` and `completion` models."""

    top_k: Annotated[Optional[float], pydantic.Field(alias="topK")] = None
    r"""Only supported on `chat` and `completion` models."""

    top_p: Annotated[Optional[float], pydantic.Field(alias="topP")] = None
    r"""Only supported on `chat` and `completion` models."""

    frequency_penalty: Annotated[
        Optional[float], pydantic.Field(alias="frequencyPenalty")
    ] = None
    r"""Only supported on `chat` and `completion` models."""

    presence_penalty: Annotated[
        Optional[float], pydantic.Field(alias="presencePenalty")
    ] = None
    r"""Only supported on `chat` and `completion` models."""

    num_images: Annotated[Optional[float], pydantic.Field(alias="numImages")] = None
    r"""Only supported on `image` models."""

    seed: Optional[float] = None
    r"""Best effort deterministic seed for the model. Currently only OpenAI models support these"""

    format_: Annotated[Optional[DeploymentsFormat], pydantic.Field(alias="format")] = (
        None
    )
    r"""Only supported on `image` models."""

    dimensions: Optional[str] = None
    r"""Only supported on `image` models."""

    quality: Optional[DeploymentsQuality] = None
    r"""Only supported on `image` models."""

    style: Optional[str] = None
    r"""Only supported on `image` models."""

    response_format: Annotated[
        OptionalNullable[DeploymentsResponseFormat],
        pydantic.Field(alias="responseFormat"),
    ] = UNSET
    r"""An object specifying the format that the model must output.

    Setting to `{ \"type\": \"json_schema\", \"json_schema\": {...} }` enables Structured Outputs which ensures the model will match your supplied JSON schema

    Setting to `{ \"type\": \"json_object\" }` enables JSON mode, which ensures the message the model generates is valid JSON.

    Important: when using JSON mode, you must also instruct the model to produce JSON yourself via a system or user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the token limit, resulting in a long-running and seemingly \"stuck\" request. Also note that the message content may be partially cut off if finish_reason=\"length\", which indicates the generation exceeded max_tokens or the conversation exceeded the max context length.
    """

    photo_real_version: Annotated[
        Optional[DeploymentsPhotoRealVersion], pydantic.Field(alias="photoRealVersion")
    ] = None
    r"""The version of photoReal to use. Must be v1 or v2. Only available for `leonardoai` provider"""

    encoding_format: Optional[DeploymentsEncodingFormat] = None
    r"""The format to return the embeddings"""

    reasoning_effort: Annotated[
        Optional[DeploymentsReasoningEffort], pydantic.Field(alias="reasoningEffort")
    ] = None
    r"""Constrains effort on reasoning for reasoning models. Reducing reasoning effort can result in faster responses and fewer tokens used on reasoning in a response."""

    budget_tokens: Annotated[Optional[float], pydantic.Field(alias="budgetTokens")] = (
        None
    )
    r"""Gives the model enhanced reasoning capabilities for complex tasks. A value of 0 disables thinking. The minimum budget tokens for thinking are 1024. The Budget Tokens should never exceed the Max Tokens parameter. Only supported by `Anthropic`"""

    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        optional_fields = [
            "temperature",
            "maxTokens",
            "topK",
            "topP",
            "frequencyPenalty",
            "presencePenalty",
            "numImages",
            "seed",
            "format",
            "dimensions",
            "quality",
            "style",
            "responseFormat",
            "photoRealVersion",
            "encoding_format",
            "reasoningEffort",
            "budgetTokens",
        ]
        nullable_fields = ["responseFormat"]
        null_default_fields = []

        serialized = handler(self)

        m = {}

        for n, f in self.model_fields.items():
            k = f.alias or n
            val = serialized.get(k)
            serialized.pop(k, None)

            optional_nullable = k in optional_fields and k in nullable_fields
            is_set = (
                self.__pydantic_fields_set__.intersection({n})
                or k in null_default_fields
            )  # pylint: disable=no-member

            if val is not None and val != UNSET_SENTINEL:
                m[k] = val
            elif val != UNSET_SENTINEL and (
                not k in optional_fields or (optional_nullable and is_set)
            ):
                m[k] = val

        return m


DeploymentsProvider = Literal[
    "cohere",
    "openai",
    "anthropic",
    "huggingface",
    "replicate",
    "google",
    "google-ai",
    "azure",
    "aws",
    "anyscale",
    "perplexity",
    "groq",
    "fal",
    "leonardoai",
    "nvidia",
    "jina",
    "togetherai",
    "elevenlabs",
]

DeploymentsRole = Literal[
    "system",
    "assistant",
    "user",
    "exception",
    "tool",
    "prompt",
    "correction",
    "expected_output",
]
r"""The role of the prompt message"""

Deployments2DeploymentsResponseType = Literal["image_url"]


class Deployments2ImageURLTypedDict(TypedDict):
    url: str
    r"""Either a URL of the image or the base64 encoded data URI."""
    id: NotRequired[str]
    r"""The orq.ai id of the image"""
    detail: NotRequired[str]
    r"""Specifies the detail level of the image. Currently only supported with OpenAI models"""


class Deployments2ImageURL(BaseModel):
    url: str
    r"""Either a URL of the image or the base64 encoded data URI."""

    id: Optional[str] = None
    r"""The orq.ai id of the image"""

    detail: Optional[str] = None
    r"""Specifies the detail level of the image. Currently only supported with OpenAI models"""


class Deployments2Deployments2TypedDict(TypedDict):
    r"""The image part of the prompt message. Only supported with vision models."""

    type: Deployments2DeploymentsResponseType
    image_url: Deployments2ImageURLTypedDict


class Deployments2Deployments2(BaseModel):
    r"""The image part of the prompt message. Only supported with vision models."""

    type: Deployments2DeploymentsResponseType

    image_url: Deployments2ImageURL


Deployments2DeploymentsType = Literal["text"]


class Deployments21TypedDict(TypedDict):
    r"""Text content part of a prompt message"""

    type: Deployments2DeploymentsType
    text: str


class Deployments21(BaseModel):
    r"""Text content part of a prompt message"""

    type: Deployments2DeploymentsType

    text: str


DeploymentsContentDeployments2TypedDict = TypeAliasType(
    "DeploymentsContentDeployments2TypedDict",
    Union[Deployments21TypedDict, Deployments2Deployments2TypedDict],
)


DeploymentsContentDeployments2 = TypeAliasType(
    "DeploymentsContentDeployments2", Union[Deployments21, Deployments2Deployments2]
)


DeploymentsContentTypedDict = TypeAliasType(
    "DeploymentsContentTypedDict",
    Union[str, List[DeploymentsContentDeployments2TypedDict]],
)
r"""The contents of the user message. Either the text content of the message or an array of content parts with a defined type, each can be of type `text` or `image_url` when passing in images. You can pass multiple images by adding multiple `image_url` content parts."""


DeploymentsContent = TypeAliasType(
    "DeploymentsContent", Union[str, List[DeploymentsContentDeployments2]]
)
r"""The contents of the user message. Either the text content of the message or an array of content parts with a defined type, each can be of type `text` or `image_url` when passing in images. You can pass multiple images by adding multiple `image_url` content parts."""


DeploymentsDeploymentsType = Literal["function"]


class DeploymentsDeploymentsFunctionTypedDict(TypedDict):
    name: str
    arguments: str
    r"""JSON string arguments for the functions"""


class DeploymentsDeploymentsFunction(BaseModel):
    name: str

    arguments: str
    r"""JSON string arguments for the functions"""


class DeploymentsToolCallsTypedDict(TypedDict):
    type: DeploymentsDeploymentsType
    function: DeploymentsDeploymentsFunctionTypedDict
    id: NotRequired[str]
    index: NotRequired[float]


class DeploymentsToolCalls(BaseModel):
    type: DeploymentsDeploymentsType

    function: DeploymentsDeploymentsFunction

    id: Optional[str] = None

    index: Optional[float] = None


class DeploymentsMessagesTypedDict(TypedDict):
    role: DeploymentsRole
    r"""The role of the prompt message"""
    content: DeploymentsContentTypedDict
    r"""The contents of the user message. Either the text content of the message or an array of content parts with a defined type, each can be of type `text` or `image_url` when passing in images. You can pass multiple images by adding multiple `image_url` content parts."""
    tool_calls: NotRequired[List[DeploymentsToolCallsTypedDict]]


class DeploymentsMessages(BaseModel):
    role: DeploymentsRole
    r"""The role of the prompt message"""

    content: DeploymentsContent
    r"""The contents of the user message. Either the text content of the message or an array of content parts with a defined type, each can be of type `text` or `image_url` when passing in images. You can pass multiple images by adding multiple `image_url` content parts."""

    tool_calls: Optional[List[DeploymentsToolCalls]] = None


class DeploymentsPromptConfigTypedDict(TypedDict):
    tools: List[DeploymentsToolsTypedDict]
    model: str
    model_type: DeploymentsModelType
    r"""The type of the model"""
    model_parameters: DeploymentsModelParametersTypedDict
    r"""Model Parameters: Not all parameters apply to every model"""
    provider: DeploymentsProvider
    messages: List[DeploymentsMessagesTypedDict]


class DeploymentsPromptConfig(BaseModel):
    tools: List[DeploymentsTools]

    model: str

    model_type: DeploymentsModelType
    r"""The type of the model"""

    model_parameters: DeploymentsModelParameters
    r"""Model Parameters: Not all parameters apply to every model"""

    provider: DeploymentsProvider

    messages: List[DeploymentsMessages]


class DataTypedDict(TypedDict):
    id: str
    r"""Unique identifier for the object."""
    created: str
    r"""Date in ISO 8601 format at which the object was created."""
    updated: str
    r"""Date in ISO 8601 format at which the object was last updated."""
    key: str
    r"""The deployment unique key"""
    description: str
    r"""An arbitrary string attached to the object. Often useful for displaying to users."""
    prompt_config: DeploymentsPromptConfigTypedDict
    version: str
    r"""THe version of the deployment"""


class Data(BaseModel):
    id: str
    r"""Unique identifier for the object."""

    created: str
    r"""Date in ISO 8601 format at which the object was created."""

    updated: str
    r"""Date in ISO 8601 format at which the object was last updated."""

    key: str
    r"""The deployment unique key"""

    description: str
    r"""An arbitrary string attached to the object. Often useful for displaying to users."""

    prompt_config: DeploymentsPromptConfig

    version: str
    r"""THe version of the deployment"""


class DeploymentsResponseBodyTypedDict(TypedDict):
    r"""List all deployments"""

    object: Object
    data: List[DataTypedDict]
    has_more: bool


class DeploymentsResponseBody(BaseModel):
    r"""List all deployments"""

    object: Object

    data: List[Data]

    has_more: bool
