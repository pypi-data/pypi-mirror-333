# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["VoiceUpdateParams"]


class VoiceUpdateParams(TypedDict, total=False):
    worker_id: Required[Annotated[str, PropertyInfo(alias="workerId")]]

    config: str

    flow_id: Annotated[str, PropertyInfo(alias="flowId")]

    name: str

    phone_number: Annotated[str, PropertyInfo(alias="phoneNumber")]
