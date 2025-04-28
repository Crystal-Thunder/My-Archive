from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Data models
class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    available: bool = True

# In-memory database
library = []

# Routes
@app.post("/books/", response_model=Book)
def add_book(book: Book):
    for existing_book in library:
        if existing_book.id == book.id:
            raise HTTPException(status_code=400, detail="Book with this ID already exists.")
    library.append(book)
    return book

@app.get("/books/", response_model=List[Book])
def get_books(available: Optional[bool] = None):
    if available is None:
        return library
    return [book for book in library if book.available == available]

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in library:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found.")

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(library):
        if book.id == book_id:
            library[index] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found.")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(library):
        if book.id == book_id:
            del library[index]
            return {"message": "Book deleted successfully."}
    raise HTTPException(status_code=404, detail="Book not found.")