"""DoData functions for dies."""

from __future__ import annotations

import httpx
from typing_extensions import TypedDict

from .common import get as _get
from .common import post
from .common import url as base_url


class Die(TypedDict):
    """Dict for a Die."""

    project_pkey: int
    wafer_pkey: int
    x: int
    y: int


def create(
    project_id: str,
    wafer_id: str,
    x: int,
    y: int,
    # TODO: needs attributes on die
    # attributes: dict[str, int | float | bool | str] = {},
) -> httpx.Response:
    """Upload a new die to DoData.

    Args:
        project_id: The name of the project which owns the die.
        wafer_id: The name of the wafer which owns the die.
        x: x-coordinate of the die.
        y: y-coordinate of the die.
        attributes: Additional information about the die.
    """
    url = f"{base_url}/die"
    params = {
        "project_id": project_id,
        "wafer_id": wafer_id,
        "die_x": x,
        "die_y": y,
    }
    # TODO: needs attributes on die
    # return post(url, params=params, json=attributes)
    response = post(url, params=params)

    return response


def get(project_id: str, wafer_id: str, x: int, y: int) -> Die:
    """Get a die by coordinates, project name, and wafer name."""
    die_response = _get(f"{base_url}/die/{project_id}/{wafer_id}/{x}/{y}")
    return die_response.json()  # type: ignore[no-any-return]
