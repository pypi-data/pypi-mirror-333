"""
Absfuyu: Inspector
------------------
Inspector

Version: 5.1.0
Date updated: 10/03/2025 (dd/mm/yyyy)
"""

# Module level
# ---------------------------------------------------------------------------
__all__ = ["Inspector"]

# Library
# ---------------------------------------------------------------------------
import inspect
import os
from textwrap import TextWrapper
from textwrap import shorten as text_shorten
from typing import Any

from absfuyu.core.baseclass import (
    AutoREPRMixin,
    MethodNPropertyResult,
    ShowAllMethodsMixin,
)
from absfuyu.dxt.listext import ListExt
from absfuyu.util.text_table import OneColumnTableMaker


# Class
# ---------------------------------------------------------------------------
# TODO: rewrite with each class for docs, method, property, attr, param, title
class Inspector(AutoREPRMixin):
    """
    Inspect an object

    Parameters
    ----------
    obj : Any
        Object to inspect

    line_length: int | None
        Number of cols in inspect output (Split line every line_length).
        Set to ``None`` to use ``os.get_terminal_size()``, by default ``88``

    include_docs : bool, optional
        Include docstring, by default ``True``

    include_mro : bool, optional
        Include class bases (__mro__), by default ``False``

    include_method : bool, optional
        Include object's methods (if any), by default ``False``

    include_property : bool, optional
        Include object's properties (if any), by default ``True``

    include_attribute : bool, optional
        Include object's attributes (if any), by default ``True``

    include_private : bool, optional
        Include object's private attributes, by default ``False``

    include_all : bool, optional
        Include all infomation availble, by default ``False``


    Example:
    --------
    >>> print(Inspector(<object>, **kwargs))
    """

    def __init__(
        self,
        obj: Any,
        *,
        line_length: int | None = 88,
        include_docs: bool = True,
        include_mro: bool = False,
        include_method: bool = False,
        include_property: bool = True,
        include_attribute: bool = True,
        include_private: bool = False,
        include_all: bool = False,
    ) -> None:
        """
        Inspect an object

        Parameters
        ----------
        obj : Any
            Object to inspect

        line_length: int | None
            Number of cols in inspect output (Split line every line_length).
            Set to ``None`` to use ``os.get_terminal_size()``, by default ``88``

        include_docs : bool, optional
            Include docstring, by default ``True``

        include_mro : bool, optional
            Include class bases (__mro__), by default ``False``

        include_method : bool, optional
            Include object's methods (if any), by default ``False``

        include_property : bool, optional
            Include object's properties (if any), by default ``True``

        include_attribute : bool, optional
            Include object's attributes (if any), by default ``True``

        include_private : bool, optional
            Include object's private attributes, by default ``False``

        include_all : bool, optional
            Include all infomation availble, by default ``False``


        Example:
        --------
        >>> print(Inspector(<object>, **kwargs))
        """
        self.obj = obj
        self.include_docs = include_docs
        self.include_mro = include_mro
        self.include_method = include_method
        self.include_property = include_property
        self.include_attribute = include_attribute
        self.include_private = include_private

        if include_all:
            self.include_docs = True
            self.include_mro = True
            self.include_method = True
            self.include_property = True
            self.include_attribute = True
            self.include_private = True

        # Setup line length
        if line_length is None:
            try:
                self._linelength = os.get_terminal_size().columns
            except OSError:
                self._linelength = 88
        elif isinstance(line_length, (int, float)):
            self._linelength = max(int(line_length), 9)
        else:
            raise ValueError("Use different line_length")

        # Textwrap
        self._text_wrapper = TextWrapper(
            width=self._linelength - 4,
            initial_indent="",
            subsequent_indent="",
            tabsize=4,
            break_long_words=True,
            max_lines=8,
        )

        # Output
        self._inspect_output = self._make_output()

    def __str__(self) -> str:
        return self.detail_str()

    # Support
    def _long_list_terminal_size(self, long_list: list) -> list:
        max_name_len = max([len(x) for x in long_list]) + 1
        cols = 1

        if max_name_len <= self._linelength - 4:
            cols = (self._linelength - 4) // max_name_len
        splitted_chunk: list[list[str]] = ListExt(long_list).split_chunk(cols)

        mod_chunk = ListExt(
            [[x.ljust(max_name_len, " ") for x in chunk] for chunk in splitted_chunk]
        ).apply(lambda x: "".join(x))

        return list(mod_chunk)

    # Signature
    def _make_title(self) -> str:
        """
        Inspector's workflow:
        01. Make title
        """
        title_str = (
            str(self.obj)
            if (
                inspect.isclass(self.obj)
                or callable(self.obj)
                or inspect.ismodule(self.obj)
            )
            else str(type(self.obj))
        )
        return title_str

    def _get_signature_prefix(self) -> str:
        # signature prefix
        if inspect.isclass(self.obj):
            return "class"
        elif inspect.iscoroutinefunction(self.obj):
            return "async def"
        elif inspect.isfunction(self.obj):
            return "def"
        return ""

    def get_parameters(self) -> list[str] | None:
        try:
            sig = inspect.signature(self.obj)
        except (ValueError, AttributeError, TypeError):
            return None
        return [str(x) for x in sig.parameters.values()]

    def _make_signature(self) -> list[str]:
        """
        Inspector's workflow:
        02. Make signature
        """
        try:
            return self._text_wrapper.wrap(
                f"{self._get_signature_prefix()} {self.obj.__name__}{inspect.signature(self.obj)}"
            )
        #    not class, func | not type   | is module
        except (ValueError, AttributeError, TypeError):
            return self._text_wrapper.wrap(repr(self.obj))

    # Method and property
    def _get_method_property(self) -> MethodNPropertyResult:
        # if inspect.isclass(self.obj) or inspect.ismodule(self.obj):
        if inspect.isclass(self.obj):
            # TODO: Support enum type
            tmpcls = type(
                "tmpcls",
                (
                    self.obj,
                    ShowAllMethodsMixin,
                ),
                {},
            )
        else:
            tmpcls = type(
                "tmpcls",
                (
                    type(self.obj),
                    ShowAllMethodsMixin,
                ),
                {},
            )
        med_prop = tmpcls._get_methods_and_properties(  # type: ignore
            include_private_method=self.include_private
        )

        try:
            # If self.obj is a subclass of ShowAllMethodsMixin
            _mro = getattr(
                self.obj, "__mro__", getattr(type(self.obj), "__mro__", None)
            )
            if ShowAllMethodsMixin in _mro:  # type: ignore
                return med_prop  # type: ignore
        except AttributeError:  # Not a class
            pass
        med_prop.__delitem__(ShowAllMethodsMixin.__name__)
        return med_prop  # type: ignore

    # Docstring
    def _get_docs(self) -> str:
        """
        Inspector's workflow:
        03. Get docstring and strip
        """
        docs: str | None = inspect.getdoc(self.obj)

        if docs is None:
            return ""

        # Get docs and get first paragraph
        # doc_lines: list[str] = [x.strip() for x in docs.splitlines()]
        doc_lines = []
        for line in docs.splitlines():
            if len(line) < 1:
                break
            doc_lines.append(line.strip())

        return text_shorten(" ".join(doc_lines), width=self._linelength - 4, tabsize=4)

    # Attribute
    @staticmethod
    def _is_real_attribute(obj: Any) -> bool:
        """
        Not method, classmethod, staticmethod, property
        """
        if callable(obj):
            return False
        if isinstance(obj, staticmethod):
            return False
        if isinstance(obj, classmethod):
            return False
        if isinstance(obj, property):
            return False
        return True

    def _get_attributes(self) -> list[tuple[str, Any]]:
        # Get attributes
        cls_dict = getattr(self.obj, "__dict__", None)
        cls_slots = getattr(self.obj, "__slots__", None)
        out = []

        # Check if __dict__ exist and len(__dict__) > 0
        if cls_dict is not None and len(cls_dict) > 0:
            if self.include_private:
                out = [
                    (k, v)
                    for k, v in self.obj.__dict__.items()
                    if self._is_real_attribute(v)
                ]
            else:
                out = [
                    (k, v)
                    for k, v in self.obj.__dict__.items()
                    if not k.startswith("_") and self._is_real_attribute(v)
                ]

        # Check if __slots__ exist and len(__slots__) > 0
        elif cls_slots is not None and len(cls_slots) > 0:
            if self.include_private:
                out = [
                    (x, getattr(self.obj, x))
                    for x in self.obj.__slots__  # type: ignore
                    if self._is_real_attribute(getattr(self.obj, x))
                ]
            else:
                out = [
                    (x, getattr(self.obj, x))
                    for x in self.obj.__slots__  # type: ignore
                    if not x.startswith("_")
                    and self._is_real_attribute(getattr(self.obj, x))
                ]

        return out

    def _handle_attributes_for_output(
        self, attr_list: list[tuple[str, Any]]
    ) -> list[str]:
        return [
            text_shorten(f"- {x[0]} = {x[1]}", self._linelength - 4) for x in attr_list
        ]

    # Get MRO
    def _get_mro(self) -> tuple[type, ...]:
        """Get MRO in reverse and subtract <class 'object'>"""
        if isinstance(self.obj, type):
            return self.obj.__mro__[::-1][1:]
        return type(self.obj).__mro__[::-1][1:]

    def _make_mro_data(self) -> list[str]:
        mro = [
            f"- {i:02}. {x.__module__}.{x.__name__}"
            for i, x in enumerate(self._get_mro(), start=1)
        ]
        mod_chunk = self._long_list_terminal_size(mro)

        # return [text_shorten(x, self._linelength - 4) for x in mod_chunk]
        return mod_chunk

    # Output
    def _make_output(self) -> OneColumnTableMaker:
        table = OneColumnTableMaker(self._linelength)
        body: list[str] = []

        # Signature
        title = self._make_title()
        table.add_title(title)
        sig = self._make_signature()
        if table._title == "":  # Title too long
            _title = [title]
            _title.extend(sig)
            table.add_paragraph(_title)
        else:
            table.add_paragraph(sig)

        # Docstring
        docs = self._get_docs()
        if len(docs) > 0 and self.include_docs:
            body.extend(["Docstring:", docs])

        # Class bases
        clsbases = self._make_mro_data()
        if len(clsbases) > 0 and self.include_mro:
            body.extend(["", f"Bases (Len: {len(self._get_mro())}):"])
            body.extend(clsbases)

        # Method & Property
        try:
            method_n_properties = self._get_method_property().flatten_value().pack()
            if self.include_method:
                ml = [
                    text_shorten(f"- {x}", self._linelength - 4)
                    for x in method_n_properties.methods
                ]
                if len(ml) > 0:
                    head = ["", f"Methods (Len: {len(ml)}):"]
                    head.extend(self._long_list_terminal_size(ml))
                    body.extend(head)
            if self.include_property:
                pl = [
                    text_shorten(
                        f"- {x} = {getattr(self.obj, x, None)}", self._linelength - 4
                    )
                    for x in method_n_properties.properties
                ]
                if len(pl) > 0:
                    head = ["", f"Properties (Len: {len(pl)}):"]
                    head.extend(pl)
                    body.extend(head)
        except (TypeError, AttributeError):
            pass

        # Attribute
        attrs = self._get_attributes()
        if len(attrs) > 0 and self.include_attribute:
            body.extend(["", f"Attributes (Len: {len(attrs)}):"])
            body.extend(self._handle_attributes_for_output(attr_list=attrs))

        # Add to table
        table.add_paragraph(body)

        return table

    def detail_str(self) -> str:
        return self._inspect_output.make_table()
