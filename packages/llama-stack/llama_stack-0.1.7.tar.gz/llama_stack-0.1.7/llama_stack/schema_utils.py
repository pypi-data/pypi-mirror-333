# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Protocol, TypeVar

from .strong_typing.schema import json_schema_type, register_schema  # noqa: F401


@dataclass
class WebMethod:
    route: Optional[str] = None
    public: bool = False
    request_examples: Optional[List[Any]] = None
    response_examples: Optional[List[Any]] = None
    method: Optional[str] = None
    raw_bytes_request_body: Optional[bool] = False


class HasWebMethod(Protocol):
    __webmethod__: WebMethod


T = TypeVar("T", bound=HasWebMethod)  # Bound T to classes that match this protocol


def webmethod(
    route: Optional[str] = None,
    method: Optional[str] = None,
    public: Optional[bool] = False,
    request_examples: Optional[List[Any]] = None,
    response_examples: Optional[List[Any]] = None,
    raw_bytes_request_body: Optional[bool] = False,
) -> Callable[[T], T]:
    """
    Decorator that supplies additional metadata to an endpoint operation function.

    :param route: The URL path pattern associated with this operation which path parameters are substituted into.
    :param public: True if the operation can be invoked without prior authentication.
    :param request_examples: Sample requests that the operation might take. Pass a list of objects, not JSON.
    :param response_examples: Sample responses that the operation might produce. Pass a list of objects, not JSON.
    """

    def wrap(cls: T) -> T:
        cls.__webmethod__ = WebMethod(
            route=route,
            method=method,
            public=public or False,
            request_examples=request_examples,
            response_examples=response_examples,
            raw_bytes_request_body=raw_bytes_request_body,
        )
        return cls

    return wrap
