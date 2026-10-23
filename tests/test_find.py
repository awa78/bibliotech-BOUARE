import pytest


@pytest.mark.parametrize(
    "kind, item_id, collection",
    [
        ("b", "B001", "b"),
        ("m", "M001", "m"),
        ("l", "L001", "l"),
    ],
)
def test_find_returns_existing_item(library, kind, item_id, collection):
    result = library.find(kind, item_id)

    expected = next(
        item for item in getattr(library, collection)
        if item["id"] == item_id
    )
    assert result is expected


@pytest.mark.parametrize(
    "kind, item_id",
    [
        ("b", "B999"),
        ("m", "M999"),
        ("l", "L999"),
        ("unknown", "B001"),
    ],
)
def test_find_returns_none_for_unknown_item(library, kind, item_id):
    assert library.find(kind, item_id) is None