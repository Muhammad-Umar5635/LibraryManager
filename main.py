import streamlit as st
import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    genre TEXT NOT NULL,
                    read BOOLEAN NOT NULL)''')
    conn.commit()
    conn.close()

# Add book to database
def add_book(title, author, year, genre, read):
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    c.execute("INSERT INTO books (title, author, year, genre, read) VALUES (?, ?, ?, ?, ?)",
              (title, author, year, genre, read))
    conn.commit()
    conn.close()

# Load all books
def load_books():
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    conn.close()
    return books

# Remove book by title
def remove_book(title):
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE title = ?", (title,))
    conn.commit()
    conn.close()

# Search books by title or author
def search_books(query):
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    c.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", 
              (f"%{query}%", f"%{query}%"))
    results = c.fetchall()
    conn.close()
    return results

# Mark book as read/unread
def update_read_status(title, status):
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    c.execute("UPDATE books SET read = ? WHERE title = ?", (status, title))
    conn.commit()
    conn.close()

# Get statistics
def get_statistics():
    books = load_books()
    total_books = len(books)
    read_books = sum(1 for book in books if book[5] == 1)
    return total_books, read_books, (read_books / total_books * 100 if total_books else 0)

# Initialize Database
init_db()

# Streamlit UI
st.title("📚 Personal Library Manager")

menu = st.sidebar.radio("Menu", ["Add Book", "Remove Book", "Search Books", "View All Books", "Update Read Status", "Statistics"])

if menu == "Add Book":
    st.subheader("Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1700, max_value=2025, step=1)
    genre = st.selectbox("Genre", ["Fiction", "Motivation", "Science", "Love Story", "Horror", "Others"])
    read = st.checkbox("Have you read this book?")
    
    if st.button("Add Book"):
        if not title or not author or year == 0:
            st.warning("Please fill in all fields before adding the book.")
        else:
            add_book(title, author, year, genre, int(read))
            st.success(f"Book '{title}' added successfully!")

elif menu == "Remove Book":
    st.subheader("Remove a Book")
    title = st.text_input("Enter book title to remove")
    
    if st.button("Remove Book"):
        remove_book(title)
        st.success(f"Book '{title}' removed successfully!")

elif menu == "Search Books":
    st.subheader("Search for Books")
    query = st.text_input("Enter title or author")
    
    if st.button("Search"):
        results = search_books(query)
        if results:
            for book in results:
                st.write(f"📖 **{book[1]}** by {book[2]} ({book[3]}) - Genre: {book[4]} - {'✅ Read' if book[5] else '❌ Not Read'}")
        else:
            st.warning("No books found.")

elif menu == "View All Books":
    st.subheader("All Books")
    books = load_books()
    if books:
        for book in books:
            st.write(f"📖 **{book[1]}** by {book[2]} ({book[3]}) - Genre: {book[4]} - {'✅ Read' if book[5] else '❌ Not Read'}")
    else:
        st.warning("No books in the library.")

elif menu == "Update Read Status":
    st.subheader("Mark Book as Read/Unread")
    books = load_books()
    titles = [book[1] for book in books]

    selected_title = st.selectbox("Select a Book", titles)
    status = st.radio("Update Status", ["Read", "Unread"])
    
    if st.button("Update Status"):
        update_read_status(selected_title, 1 if status == "Read" else 0)
        st.success(f"Book '{selected_title}' marked as {status}.")

elif menu == "Statistics":
    st.subheader("Library Statistics")
    total, read, percentage = get_statistics()
    st.write(f"📚 Total books: **{total}**")
    st.write(f"✅ Books read: **{read}**")
    st.write(f"📊 Percentage read: **{percentage:.2f}%**")

