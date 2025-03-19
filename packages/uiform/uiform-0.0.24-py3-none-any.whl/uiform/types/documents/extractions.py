from pydantic import BaseModel, Field, ConfigDict, field_validator, ValidationInfo
from typing import  Any, Literal, List

import datetime
from functools import cached_property

from ..._utils.ai_model import find_provider_from_model

from ..modalities import Modality
from ..ai_model import AIProvider
from ..standards import ErrorDetail, StreamingBaseModel
from ..mime import MIMEData, BaseMIMEData
from ..schemas.object import Schema
from ..image_settings import ImageSettings
from ..chat import ChatCompletionUiformMessage

from openai.types.chat.parsed_chat_completion import ParsedChatCompletion, ParsedChoice

class DocumentExtractRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    document: MIMEData = Field(..., description="Document to be analyzed")
    modality: Modality
    image_settings : ImageSettings = Field(default_factory=ImageSettings, description="Preprocessing operations applied to image before sending them to the llm")
    model: str = Field(..., description="Model used for chat completion")
    json_schema: dict[str, Any] = Field(..., description="JSON schema format used to validate the output data.")
    temperature: float = Field(default=0.0, description="Temperature for sampling. If not provided, the default temperature for the model will be used.", examples=[0.0])

    # Regular fields
    stream: bool = Field(default=False, description="If true, the extraction will be streamed to the user using the active WebSocket connection")
    seed: int | None = Field(default=None, description="Seed for the random number generator. If not provided, a random seed will be generated.", examples=[None])
    store: bool = Field(default=False, description="If true, the extraction will be stored in the database")

    @property
    def provider(self) -> AIProvider:
        """
        Determines the AI provider based on the model specified.

        Returns:
            AIProvider: The AI provider corresponding to the given model.
        """
        return find_provider_from_model(self.model)
    

class BaseDocumentExtractRequest(DocumentExtractRequest):
    document: BaseMIMEData = Field(..., description="Document analyzed (without content, for MongoDB storage)")     # type: ignore

    model_config = ConfigDict(
        json_schema_extra={"document": {"metadata": False}}
    )

    # Add a field validator that converts the input document to BaseMIMEData
    @field_validator("document")
    def convert_document_to_base_mimedata(cls, v: MIMEData | BaseMIMEData, validation_info: ValidationInfo) -> BaseMIMEData:
        return BaseMIMEData(**v.model_dump())

class UiParsedChatCompletion(ParsedChatCompletion): 
    # Additional metadata fields (UIForm)
    likelihoods: Any # Object defining the uncertainties of the fields extracted. Follows the same structure as the extraction object.
    schema_validation_error: ErrorDetail | None = None
    
    # Timestamps
    request_at: datetime.datetime | None = Field(default=None, description="Timestamp of the request")
    first_token_at: datetime.datetime | None = Field(default=None, description="Timestamp of the first token of the document. If non-streaming, set to last_token_at")
    last_token_at: datetime.datetime | None = Field(default=None, description="Timestamp of the last token of the document")


class UiParsedChoiceStream(ParsedChoice):
   finish_reason: Literal["stop", "length", "tool_calls", "content_filter", "function_call"] | None = None      # type: ignore    

class UiParsedChatCompletionStream(StreamingBaseModel, UiParsedChatCompletion):
    choices: List[UiParsedChoiceStream]  # type: ignore


class LogExtractionRequest(BaseModel):
    messages: list[ChatCompletionUiformMessage] # TODO: compatibility with Anthropic
    completion: Any # UiParsedChatCompletion  # TODO: compatibility with Anthropic
    json_schema: dict[str, Any]
    model: str
    temperature: float

DocumentExtractResponse = UiParsedChatCompletion
DocumentExtractResponseStream = UiParsedChatCompletionStream
