"""Test parsing implemented by the `selectors` module."""

from pytest import mark

from csspring.selectors import parse_selector_list
from csspring.syntax.parsing import ComponentValue, normalize_input, Product, source, tokens, QualifiedRule

from collections.abc import Sequence
from itertools import chain
from typing import cast

from .test_parser import css_file_path, parse_file_at, valid_css_file_name_stems

@mark.parametrize('text', (
    'foo',
    ' foo',
    ' foo ',
    ' /* baz */ foo ',
    'foo bar',
    'foo, bar',
    'foo > bar',
    'foo/**/',
    'foo > bar > baz',
    'foo /* x */ > bar',
    'foo[bar]',
    'foo[ bar ]',
    'foo[bar=baz]'
    'foo[bar= baz ]'
    'foo[bar= "baz" ]'
    ))
def test_selector_parsing(text: str) -> None:
    """Test whether the text recovered from the product of parsing given text (as a selector [list]) equals given text.

    :param text: Text to parse
    """
    assert source(cast(Product, parse_selector_list(normalize_input(text)))) == text

@mark.parametrize('prelude', tuple(rule.prelude for rule in chain.from_iterable(parse_file_at(path).rules for path in (css_file_path(stem) for stem in valid_css_file_name_stems)) if isinstance(rule, QualifiedRule)))
def test_qualified_rule_prelude_parsing_product_tokens_equal_prelude_tokens(prelude: Sequence[ComponentValue]) -> None:
    """Test whether the sequence of tokens constituting the parse product obtained from parsing given [qualified rule's] prelude (as a selector [list]), equals the sequence of tokens that constitute the prelude.

    :param prelude: A qualified rule's "prelude" (see the corresponding attribute of `csspring.syntax.parsing.QualifiedRule`)
    """
    assert tuple(tokens(cast(Product, parse_selector_list(normalize_input(tokens(prelude)))))) == tuple(tokens(prelude))
