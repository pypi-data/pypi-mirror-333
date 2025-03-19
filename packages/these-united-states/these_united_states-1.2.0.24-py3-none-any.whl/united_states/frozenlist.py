# BSD 3-Clause License
#
# Copyright (c) 2020, Avantus LLC
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Provides a read-only interface to a list."""

from typing import Any, Iterator, overload, Sequence, TypeVar, Union


_T = TypeVar('_T')


class ReadOnlyMixin:
    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError(f'{self.__class__.__name__!r} object is read-only')

    def __delattr__(self, name: str) -> None:
        raise AttributeError(f'{self.__class__.__name__!r} object is read-only')


class FrozenList(Sequence[_T], ReadOnlyMixin):
    """Read-only wrapper around a list."""

    __slots__ = '_frozen_items',

    def __init__(self, items: Sequence[_T]) -> None:
        object.__setattr__(self, '_frozen_items', items)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({object.__getattribute__(self, "_frozen_items")!r})'

    def __getattribute__(self, name: str) -> Any:
        if name == '_frozen_items':
            raise AttributeError(f'{self.__class__.__name__!s} object attribute {name!r} is private')
        return super().__getattribute__(name)

    def __len__(self) -> int:
        return len(object.__getattribute__(self, '_frozen_items'))

    def __iter__(self) -> Iterator[_T]:
        return iter(object.__getattribute__(self, '_frozen_items'))

    @overload
    def __getitem__(self, item: int) -> _T:
        pass
    @overload
    def __getitem__(self, item: slice) -> Sequence[_T]:
        pass
    def __getitem__(self, item: Union[int, slice]) -> Union[_T, Sequence[_T]]:
        return object.__getattribute__(self, '_frozen_items').__getitem__(item)  # type: ignore[no-any-return]

    def __contains__(self, item: Any) -> bool:
        return object.__getattribute__(self, '_frozen_items').__contains__(item)  # type: ignore[no-any-return]
