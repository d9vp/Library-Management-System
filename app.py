from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from model import db, Book, Author, Issuer, Issue, Inventory
from datetime import datetime, timedelta, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search_text = request.form.get('searchInput', '').strip() # Getting title text to search from form input
        search_issue_id = request.form.get('searchIssueID')  # Getting issue ID from form input
        if search_text:
            inventory_items = filter_inventory_by_title(search_text)
        elif search_issue_id:
            inventory_items = filter_inventory_by_issue_id(int(search_issue_id))
        else:
            inventory_items = Inventory.query.all()
    else:
        inventory_items = Inventory.query.all()

    inventory_data = prepare_inventory_data(inventory_items)
    now = datetime.now().date()  # Get current date

    return render_template("index.html", inventory=inventory_data, now=now)

def filter_inventory_by_title(search_text):
    # Filter inventory items where book title contains search_text
    filtered_inventory = Inventory.query \
        .join(Book) \
        .filter(Book.title.ilike(f"%{search_text}%")) \
        .all()
    return filtered_inventory

def filter_inventory_by_issue_id(issue_id):
    # Query issues based on issue_id
    issues = Issue.query.filter_by(issue_id=issue_id).all()
    inventory_items = [issue.inventory for issue in issues]

    return inventory_items



@app.route("/issue/<int:inventory_id>", methods=['GET', 'POST'])
def issue_book_form(inventory_id):
    inventory_item = Inventory.query.get_or_404(inventory_id)
    
    if inventory_item.is_available:
        if request.method == 'POST':
            # Handle form submission for issuing a book
            issuer_id = request.form.get('issuer_id')
            issue_date = request.form.get('issue_date')  # Assuming issue_date is also submitted
            due_date = (datetime.now() + timedelta(days=14)).date()  # 14 days from issue date

            # Create a new issue record in the database
            new_issue = Issue(
                inventory_id=inventory_id,
                issuer_id=issuer_id,
                issue_date=issue_date,
                due_date=due_date
            )
            db.session.add(new_issue)
            db.session.commit()

            # Update inventory availability (if needed)
            inventory_item.is_available = False
            db.session.commit()

            flash('Book issued successfully!', 'success')
            return redirect(url_for('home'))

        return render_template("issue_form.html", inventory_id=inventory_id)
    else:
        flash('Book is currently not available for issuing.', 'danger')
        return redirect(url_for('home'))


@app.route("/return/<int:issue_id>", methods=['GET', 'POST'])
def return_book_form(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    inventory_item = Inventory.query.get_or_404(issue.inventory_id)
    diff = (datetime.now().date() - issue.due_date).days
    fine_amount = max(diff, 0) * 10  # Calculate fine amount

    if not inventory_item.is_available:
        issuer = Issuer.query.get_or_404(issue.issuer_id)

        if request.method == 'POST':
            # Set return_date to today's date
            return_date = date.today()

            # Update return details
            issue.return_date = return_date
            issue.is_returned = True
            db.session.commit()

            # Update inventory availability
            inventory_item.is_available = True
            db.session.commit()

            flash('Book returned successfully!', 'success')
            return redirect(url_for('home'))

        # Rendering return form with calculated fine amount and issuer details
        return render_template("return_form.html", issue=issue, fine_amount=fine_amount, issuer=issuer)

    else:
        flash('Book is already available.', 'danger')
        return redirect(url_for('home'))


def prepare_inventory_data(inventory_items):
    inventory_data = []
    for item in inventory_items:
        book = Book.query.get(item.book_id)
        author = Author.query.get(book.author_id) if book else None

        # Getting active issue (if any) for the current inventory item
        active_issue = Issue.query.filter_by(inventory_id=item.inventory_id, is_returned=False).first()
        issue_id = active_issue.issue_id if active_issue else None  # Getting issue_id if active_issue exists

        if book:
            data = {
                'serial_number': item.inventory_id,
                'title': book.title,
                'author': author.name if author else 'Unknown',
                'is_available': item.is_available,
                'active_issue': active_issue,  # Including active issue in inventory data
                'issue_id': issue_id  # Storing issue_id or None
            }
            inventory_data.append(data)

    return inventory_data


if __name__ == "__main__":
    app.run(debug=True)
