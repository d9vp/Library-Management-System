from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from datetime import datetime,timedelta
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'author'
    author_id = db.Column(db.Integer, nullable= False, primary_key = True, autoincrement = True)
    name = db.Column(db.String(200), nullable = False, default="Anonymous")
    birth_date = db.Column(db.Date)
    country = db.Column(db.String(50))

    def __repr__(self):
        return f"{self.author_id}, {self.name}, {self.birth_date}, {self.country}"

class Book(db.Model):
    __tablename__ = 'book'
    book_id = db.Column(db.Integer, nullable= False, primary_key = True, autoincrement = True)
    title = db.Column(db.String(200), nullable=False)
    publisher = db.Column(db.String(20), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.author_id'))
    author = relationship('Author', backref=backref('books', uselist=True))

    def __repr__(self):
        return f"{self.book_id}, {self.title}, {self.publisher}, {self.publication_year}, {self.author_id}"
    
    

class Issuer(db.Model):
    __tablename__ = 'issuer'
    issuer_id=db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name=db.Column(db.Integer, nullable=False)
    email=db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
 
    def __repr__(self) -> str:
        return f"{self.issuer_id}, {self.name}, {self.email}, {self.phone_number}"
    
class Inventory(db.Model):
    __tablename__='inventory'
    inventory_id=  db.Column(db.Integer, nullable= False, primary_key = True, autoincrement = True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'))
    book = relationship('Book', backref=backref('inventory', uselist=False))
    shelf_location	=db.Column(db.String(10), nullable=False)
    is_available=db.Column(db.Boolean,nullable=False,default=True) 

    def __repr__(self):
        return f"{self.inventory_id}, {self.book_id}, {self.shelf_location}, {self.is_available}"
    
class Issue(db.Model) :
    __tablename_ ='issue'
    issue_id=db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.inventory_id'))
    inventory = relationship('Inventory', backref=backref('issues', uselist=True))
    issuer_id = db.Column(db.Integer, db.ForeignKey('issuer.issuer_id'))
    issuer = relationship('Issuer', backref=backref('issues', uselist=True))

    issue_date = db.Column(db.Date, default = datetime.now(), nullable = False)
    due_date=db.Column(db.Date, default=lambda: datetime.now() + timedelta(days=14), nullable=False)
    return_date=db.Column(db.Date)
    is_returned=db.Column(db.Boolean,nullable=False,default=False) 
 
    def __repr__(self) -> str:
        return f"{self.issue_id}, {self.inventory_id}, {self.issuer_id}, {self.issue_date}, {self.due_date},{self.return_date}, {self.is_returned}"
   
    
