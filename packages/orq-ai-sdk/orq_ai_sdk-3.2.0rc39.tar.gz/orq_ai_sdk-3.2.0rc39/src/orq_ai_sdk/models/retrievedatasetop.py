"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from datetime import datetime
import dateutil.parser
from orq_ai_sdk.types import BaseModel
from orq_ai_sdk.utils import FieldMetadata, PathParamMetadata
import pydantic
from typing import Optional
from typing_extensions import Annotated, NotRequired, TypedDict


class RetrieveDatasetRequestTypedDict(TypedDict):
    dataset_id: str


class RetrieveDatasetRequest(BaseModel):
    dataset_id: Annotated[
        str, FieldMetadata(path=PathParamMetadata(style="simple", explode=False))
    ]


class RetrieveDatasetMetadataTypedDict(TypedDict):
    total_versions: float
    datapoints_count: float


class RetrieveDatasetMetadata(BaseModel):
    total_versions: float

    datapoints_count: float


class RetrieveDatasetResponseBodyTypedDict(TypedDict):
    r"""Dataset retrieved successfully. Returns the complete dataset object."""

    id: str
    r"""The unique identifier of the dataset"""
    display_name: str
    r"""The display name of the dataset"""
    project_id: str
    r"""The unique identifier of the project it belongs to"""
    workspace_id: str
    r"""The unique identifier of the workspace it belongs to"""
    metadata: RetrieveDatasetMetadataTypedDict
    created_by_id: NotRequired[str]
    r"""The unique identifier of the user who created the dataset"""
    updated_by_id: NotRequired[str]
    r"""The unique identifier of the user who last updated the dataset"""
    created: NotRequired[datetime]
    r"""The date and time the resource was created"""
    updated: NotRequired[datetime]
    r"""The date and time the resource was last updated"""


class RetrieveDatasetResponseBody(BaseModel):
    r"""Dataset retrieved successfully. Returns the complete dataset object."""

    id: Annotated[str, pydantic.Field(alias="_id")]
    r"""The unique identifier of the dataset"""

    display_name: str
    r"""The display name of the dataset"""

    project_id: str
    r"""The unique identifier of the project it belongs to"""

    workspace_id: str
    r"""The unique identifier of the workspace it belongs to"""

    metadata: RetrieveDatasetMetadata

    created_by_id: Optional[str] = None
    r"""The unique identifier of the user who created the dataset"""

    updated_by_id: Optional[str] = None
    r"""The unique identifier of the user who last updated the dataset"""

    created: Optional[datetime] = None
    r"""The date and time the resource was created"""

    updated: Optional[datetime] = dateutil.parser.isoparse("2025-03-11T11:09:42.848Z")
    r"""The date and time the resource was last updated"""
