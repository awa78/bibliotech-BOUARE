def test_inactive_member_is_refused(library, capsys):
    accepted = library.borrow("M004", "B002")

    assert accepted is False
    assert "membre inactif" in capsys.readouterr().out
def test_member_with_overdue_loan_is_refused(library, capsys):
    accepted = library.borrow("M001", "B002")

    assert accepted is False
    assert "emprunts en retard" in capsys.readouterr().out
def test_already_borrowed_document_is_refused(library, capsys):
    accepted = library.borrow("M005", "B001")

    assert accepted is False
    assert "deja emprunte par ce membre" in capsys.readouterr().out
def test_unavailable_document_is_refused(library, capsys):
    accepted = library.borrow("M005", "B003")

    assert accepted is False
    assert "plus d'exemplaire disponible" in capsys.readouterr().out
def test_member_at_loan_limit_is_refused(library, capsys):
    assert library.borrow("M005", "B005") is True
    assert library.borrow("M005", "B002") is True
    capsys.readouterr()

    accepted = library.borrow("M005", "B007")

    assert accepted is False
    assert "limite d'emprunts atteinte (3)" in capsys.readouterr().out
def test_available_document_is_borrowed(library, capsys):
    accepted = library.borrow("M005", "B005")

    assert accepted is True
    output = capsys.readouterr().out
    assert "Emprunt L013 enregistre" in output
    assert "retour avant le 2026-10-28" in output

    loan = library.l[-1]
    assert loan["id"] == "L013"
    assert loan["member"] == "M005"
    assert loan["book"] == "B005"
    assert loan["due"] == "2026-10-28"