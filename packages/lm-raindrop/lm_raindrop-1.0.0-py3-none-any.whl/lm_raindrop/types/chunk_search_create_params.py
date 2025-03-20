# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

__all__ = ["ChunkSearchCreateParams"]


class ChunkSearchCreateParams(TypedDict, total=False):
    input: Required[str]
    """Natural language query or question.

    Can include complex criteria and relationships
    """

    request_id: Required[str]
    """Client-provided search session identifier.

    We recommend using a UUID or ULID for this value.
    """

    bucket_ids: List[str]
    """Optional list of specific bucket IDs to search in.

    If not provided, searches the latest version of all accessible buckets
    """
