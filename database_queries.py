from app import db, app
from model import Book, Author, Issuer, Issue, Inventory
from datetime import datetime 

def initialise_db():
    with app.app_context():
        db.create_all()

#-------------------LIST STUFF--------------------------
def list_all_books():
    books = Book.query.all()
    print(books)
    return books

def list_all_authors():
    authors = Author.query.all()
    print(authors)
    return authors

def list_all_issues():
    issues = Issue.query.all()
    print(issues)
    return issues

def list_all_issuers():
    issuers = Issuer.query.all()
    print(issuers)
    return issuers

def list_all_inventory():
    inventory = Inventory.query.all()
    print(inventory)
    return inventory

#-------------------ADD STUFF--------------------------
def add_author(author):
    author = Author(**author)
    db.session.add(author)
    db.session.commit()
    return list_all_authors()

def add_book(book):
    
    # Check if the author_id exists in the Author table before adding the book
    author = db.session.query(Author).filter_by(author_id=book['author_id']).first()
    if author:
        book = Book(**book)
        db.session.add(book)
    else:
        print(f"Author with id {book['author_id']} does not exist. Skipping book addition.")

    db.session.commit()
    return list_all_books()


def add_issue(issue):
    
    issue = Issue(**issue)
    db.session.add(issue)
    db.session.commit()
    return list_all_issues()

def add_issuer(issuer):
    issuer = Issuer(**issuer)
    db.session.add(issuer)
    db.session.commit()
    return list_all_issuers()

def add_inventory(inventory):
    book = db.session.query(Book).filter_by(book_id=inventory['book_id']).first()
    if book:
        inventory = Inventory(**inventory)
        db.session.add(inventory)
    else:
        print(f"Book with id {inventory['book_id']} does not exist. Skipping inventory addition.")
    db.session.commit()

    return list_all_inventory()


if __name__ == "__main__":

    with app.app_context():
        initialise_db()
        
        authors_data = [
            {"name": "J.D. Salinger", "birth_date": datetime(1919,1,1), "country": "USA"},
            {"name": "Harper Lee", "birth_date": datetime(1926,4,28), "country": "USA"},
            {"name": "George Orwell", "birth_date": datetime(1903,6,25), "country": "UK"},
            {"name": "Jane Austen", "birth_date": datetime(1775,12,16), "country": "UK"},
            {"name": "J.R.R. Tolkien", "birth_date": datetime(1892,1,3), "country": "UK"}
        ]
        for t in authors_data:
            print(add_author(t))

        books_data = [
            {"title": "The Catcher in the Rye", "publisher": "Little, Brown", "publication_year": 1951, "author_id": 1},
            {"title": "To Kill a Mockingbird", "publisher": "Harper Perennial", "publication_year": 1960, "author_id": 2},
            {"title": "1984", "publisher": "Signet Classic", "publication_year": 1949, "author_id": 3},
            {"title": "Pride and Prejudice", "publisher": "Penguin Classics", "publication_year": 1813, "author_id": 4},
            {"title": "The Hobbit", "publisher": "Mariner Books", "publication_year": 1937, "author_id": 5}

        ]
        for t in books_data:
            print(add_book(t))

        issuers_data = [
        {"name": "Alice Johnson", "email": "alice.j@example.com", "phone_number": "9827152413"},
        {"name": "Bob Smith", "email": "bob.smith@example.com", "phone_number": "8826229493"},
        {"name": "Claire Brown", "email": "claire.b@example.com", "phone_number": "7826151423"},
        {"name": "David White", "email": "david.w@example.com", "phone_number": "9027162562"},
        {"name": "Emily Green", "email": "emily.g@example.com", "phone_number": "92716628712"}
        ]

        for data in issuers_data:
            print(add_issuer(data))

        inventory_data = [
        {"book_id": 1, "shelf_location": "A1", "is_available": True},
        {"book_id": 2, "shelf_location": "B3", "is_available": True},
        {"book_id": 3, "shelf_location": "C2", "is_available": False},
        {"book_id": 4, "shelf_location": "D1", "is_available": True},
        {"book_id": 5, "shelf_location": "E4", "is_available": False}
        ]

        for data in inventory_data:
            print(add_inventory(data))

        issues_data = [
        {"inventory_id": 1, "issuer_id": 1, "issue_date": datetime(2024, 7, 1), "due_date": datetime(2024, 7, 22), "return_date": datetime(2024, 7, 14), "is_returned": True},
        {"inventory_id": 3, "issuer_id": 2, "issue_date": datetime(2024, 7, 5), "due_date": datetime(2024, 7, 19), "is_returned": False},
        {"inventory_id": 5, "issuer_id": 3, "issue_date": datetime(2024, 7, 10), "due_date": datetime(2024, 7, 24), "is_returned": False},
        {"inventory_id": 2, "issuer_id": 4, "issue_date": datetime(2024, 7, 12), "return_date": datetime(2024, 7, 22),"due_date": datetime(2024, 7, 26), "is_returned": True},
        {"inventory_id": 4, "issuer_id": 5, "is_returned": False}
        ]

        for data in issues_data:
            print(add_issue(data))