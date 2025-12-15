import pytest

from netbyte.core import parse_hex_bytes, to_hex


@pytest.mark.parametrize(
    "text,expected",
    [
        ("DE AD BE EF", b"\xDE\xAD\xBE\xEF"),
        ("de ad be ef", b"\xDE\xAD\xBE\xEF"),
        ("0xDE,0xAD,0xBE,0xEF", b"\xDE\xAD\xBE\xEF"),
        ("deadbeef", b"\xDE\xAD\xBE\xEF"),
        ("\n\t  ", b""),
    ],
)
def test_parse_hex_bytes(text, expected):
    assert parse_hex_bytes(text) == expected


def test_parse_hex_bytes_odd_length_rejected():
    with pytest.raises(ValueError, match="even number"):
        parse_hex_bytes("ABC")


def test_to_hex_includes_printable_references_and_newline_marker():
    out = to_hex(b"Hi\n")
    # Printable bytes show references, newline shows (\n) marker.
    assert "48(H)" in out
    assert "69(i)" in out
    assert "0A(\\n)" in out
    assert out.endswith("\n")
