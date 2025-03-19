from pydantic import BaseModel, Field
from typing import Any, Literal
import datetime

from ..modalities import Modality
from ..mime import MIMEData

class PromptifyBase(BaseModel):
    model: str = "gpt-4o-2024-11-20"
    temperature: float = 0.0
    modality: Modality = "native"
    stream: bool = False

class PromptifyRequest(PromptifyBase):
    raw_schema: dict[str, Any]
    documents: list[MIMEData]

