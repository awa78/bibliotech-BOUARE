import pytest

from bibliotech import late_fee


@pytest.mark.parametrize(
    "days_late, kind, member_type, price, expected",
    [
        (0, "book", "standard", 20.0, 0.0),
        (-3, "book", "standard", 20.0, 0.0),
        (4, "book", "standard", 20.0, 2.0),
        (4, "dvd", "standard", 20.0, 4.0),
        (4, "magazine", "standard", 20.0, 0.8),
        (10, "dvd", "student", 20.0, 5.0),
        (10, "dvd", "premium", 20.0, 0.0),
        (100, "book", "standard", 8.0, 8.0),
        (4, "unknown", "standard", 20.0, 2.0),
        (3, "book", "student", 20.0, 0.75),
    ],
    ids=[
        "rendu-a-temps",
        "retard-negatif",
        "livre",
        "dvd",
        "magazine",
        "reduction-etudiant",
        "exoneration-premium",
        "plafond-prix",
        "type-inconnu",
        "montant-au-centime",
    ],
)
def test_late_fee_applies_business_rules(
    days_late, kind, member_type, price, expected
):
    actual = late_fee(days_late, kind, member_type, price)

    assert actual == pytest.approx(expected)