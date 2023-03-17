from pydantic import BaseModel
from fastapi import Form

class BookUpdate(BaseModel):
    book_name: str
    book_author: str

    @classmethod
    def as_form(
        cls,
        book_name: str = Form(...),
        book_author: str = Form(...),

    ):
        return cls(
            book_name=book_name,
            book_author=book_author
        )
