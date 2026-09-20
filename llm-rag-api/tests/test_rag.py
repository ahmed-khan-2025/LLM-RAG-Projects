from pathlib import Path

from app.documents import load_document, split_text


BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENT = (
    BASE_DIR
    / "data"
    / "employee_handbook.txt"
)


def test_load_document():

    text = load_document(
        str(DOCUMENT)
    )

    assert len(text) > 0


def test_split_text():

    text = "one two three four five six seven eight"

    chunks = split_text(
        text,
        chunk_size=3
    )

    assert len(chunks) == 3


def test_vacation_policy_exists():

    text = load_document(
        str(DOCUMENT)
    )

    assert "25 vacation days" in text


def test_remote_work_policy_exists():

    text = load_document(
        str(DOCUMENT)
    )

    assert "3 days per week" in text