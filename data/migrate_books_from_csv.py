import csv

from data.database import get_session
from data.models import Book

CSV_PATH = "books.csv"


def main():
    session = get_session()
    try:
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Ajusta estos nombres según tu CSV:
                title = row.get("title") or row.get("Title")
                author = row.get("author") or row.get("Author")
                isbn = row.get("isbn") or row.get("ISBN")

                book = Book(
                    title=title,
                    author=author,
                    isbn=isbn,
                    available=True,
                )
                session.add(book)

        session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    main()
