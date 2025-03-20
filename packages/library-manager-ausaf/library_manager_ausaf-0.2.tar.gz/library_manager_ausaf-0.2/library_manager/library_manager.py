import os
import json
import pyfiglet
import time
from typing import List, Dict, Any
import inquirer
from tabulate import tabulate
from colorama import Fore, Style, init
from yaspin import yaspin
from yaspin.spinners import Spinners
from termcolor import colored

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)

# Define the book type
Book = Dict[str, Any]

# Global variable to store the library
library: List[Book] = []
library_file = "library.json"

# Simple color scheme
COLORS = {
    "title": Fore.CYAN,
    "success": Fore.GREEN,
    "error": Fore.RED,
    "warning": Fore.YELLOW,
    "info": Fore.WHITE,
    "highlight": Fore.MAGENTA,
    "book_text": Fore.LIGHTWHITE_EX
}

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_library() -> None:
    """Load the library from a file if it exists."""
    global library
    try:
        if os.path.exists(library_file):
            with yaspin(Spinners.bouncingBar, text=colored("Loading library...", "cyan")) as spinner:
                with open(library_file, 'r') as file:
                    library = json.load(file)
                time.sleep(0.8)  # For effect
                spinner.ok("✅")
                print(COLORS["success"] + f"Loaded {len(library)} books from {library_file}")
        else:
            print(COLORS["warning"] + "No existing library found. Starting with an empty library.")
    except Exception as e:
        print(COLORS["error"] + f"Error loading library: {e}")

def save_library() -> None:
    """Save the library to a file."""
    try:
        with yaspin(Spinners.bouncingBar, text=colored("Saving library...", "green")) as spinner:
            with open(library_file, 'w') as file:
                json.dump(library, file, indent=4)
            time.sleep(0.8)  # For effect
            spinner.ok("✅")
            print(COLORS["success"] + f"Library saved to {library_file}")
    except Exception as e:
        print(COLORS["error"] + f"Error saving library: {e}")

def display_header() -> None:
    """Display the application header."""
    clear_screen()
    
    print(COLORS["title"] + "=" * 60)
    title_text = pyfiglet.figlet_format("LibraryManager", font="standard")
    print(COLORS["title"] + title_text)
    print(COLORS["title"] + "=" * 60)
    print(COLORS["info"] + "Manage your personal book collection with ease!")
    
    if library:
        read_count = sum(1 for book in library if book['read'])
        percentage = (read_count / len(library) * 100) if len(library) > 0 else 0
        print(COLORS["highlight"] + f"Currently managing {len(library)} books")
        print(COLORS["highlight"] + f"Read: {read_count} ({percentage:.1f}%)")
    
    print()

def add_book() -> None:
    """Add a new book to the library."""
    print(COLORS["title"] + "\nADD A NEW BOOK")
    print(COLORS["title"] + "-" * 60)
    
    questions = [
        inquirer.Text('title', message="Enter the book title"),
        inquirer.Text('author', message="Enter the author"),
        inquirer.Text('year', message="Enter the publication year"),
        inquirer.Text('genre', message="Enter the genre"),
        inquirer.List('read', 
                     message="Have you read this book?",
                     choices=['Yes', 'No']),
    ]
    
    answers = inquirer.prompt(questions)
    
    if not answers:
        return
    
    # Convert year to integer and read status to boolean
    try:
        answers['year'] = int(answers['year'])
    except ValueError:
        print(COLORS["warning"] + "Invalid year. Using 0 as default.")
        answers['year'] = 0
    
    answers['read'] = answers['read'] == 'Yes'
    
    # Add content field for the book
    answers['content'] = inquirer.prompt([
        inquirer.Text('content', message="Enter a brief description or excerpt (optional)")
    ])['content']
    
    # Add the book to the library
    with yaspin(Spinners.dots, text=colored("Adding book to your collection...", "magenta")) as spinner:
        library.append(answers)
        time.sleep(0.8)  # For effect
        spinner.ok("✅")
    
    print(COLORS["success"] + f"\nBook '{answers['title']}' added successfully!")
    
    # Show a preview of the added book
    print(COLORS["highlight"] + "\nBook Preview:")
    display_books([answers])

def remove_book() -> None:
    """Remove a book from the library."""
    if not library:
        print(COLORS["warning"] + "Your library is empty. Nothing to remove.")
        return
    
    print(COLORS["title"] + "\nREMOVE A BOOK")
    print(COLORS["title"] + "-" * 60)
    
    # Create a list of book titles for selection
    book_choices = [f"{book['title']} by {book['author']}" for book in library]
    book_choices.append("Cancel")
    
    questions = [
        inquirer.List('book',
                     message="Select a book to remove",
                     choices=book_choices),
    ]
    
    answers = inquirer.prompt(questions)
    
    if not answers or answers['book'] == "Cancel":
        return
    
    selected_book = answers['book']
    
    # Confirm deletion
    confirm = inquirer.prompt([
        inquirer.Confirm('confirm', 
                        message=f"Are you sure you want to remove '{selected_book}'?",
                        default=False)
    ])
    
    if not confirm or not confirm['confirm']:
        print(COLORS["warning"] + "Removal cancelled.")
        return
    
    # Find and remove the selected book
    with yaspin(Spinners.dots, text=colored("Removing book from your collection...", "red")) as spinner:
        for i, book in enumerate(library):
            if f"{book['title']} by {book['author']}" == selected_book:
                removed_book = library.pop(i)
                time.sleep(0.8)  # For effect
                spinner.ok("✅")
                print(COLORS["success"] + f"\nBook '{removed_book['title']}' removed successfully!")
                return
        
        spinner.fail("❌")
        print(COLORS["error"] + "Book not found.")

def search_book() -> None:
    """Search for books by title or author."""
    if not library:
        print(COLORS["warning"] + "Your library is empty. Nothing to search.")
        return
    
    print(COLORS["title"] + "\nSEARCH FOR BOOKS")
    print(COLORS["title"] + "-" * 60)
    
    questions = [
        inquirer.List('search_by',
                     message="Search by",
                     choices=['Title', 'Author', 'Genre', 'Year', 'Read Status']),
    ]
    
    answers = inquirer.prompt(questions)
    
    if not answers:
        return
    
    search_by = answers['search_by'].lower()
    
    if search_by == 'read status':
        status_choice = inquirer.prompt([
            inquirer.List('status',
                         message="Select read status",
                         choices=['Read', 'Unread'])
        ])
        
        if not status_choice:
            return
        
        is_read = status_choice['status'] == 'Read'
        
        with yaspin(Spinners.dots, text=colored("Searching your collection...", "blue")) as spinner:
            matching_books = [book for book in library if book['read'] == is_read]
            time.sleep(0.8)  # For effect
            spinner.ok("✅")
        
        if matching_books:
            print(COLORS["success"] + f"\nFound {len(matching_books)} {status_choice['status'].lower()} books:")
            display_books(matching_books)
        else:
            print(COLORS["warning"] + f"No {status_choice['status'].lower()} books found in your library.")
        
        return
    
    search_term = inquirer.prompt([
        inquirer.Text('term', message=f"Enter the {search_by}")
    ])
    
    if not search_term:
        return
    
    term = search_term['term'].lower()
    
    # Search for matching books
    with yaspin(Spinners.dots, text=colored("Searching your collection...", "blue")) as spinner:
        if search_by == 'year':
            try:
                year_term = int(term)
                matching_books = [book for book in library if book['year'] == year_term]
            except ValueError:
                matching_books = []
                spinner.fail("❌")
                print(COLORS["warning"] + "Invalid year format.")
                return
        else:
            matching_books = [
                book for book in library 
                if term in str(book[search_by]).lower()
            ]
        time.sleep(0.8)  # For effect
        spinner.ok("✅")
    
    if matching_books:
        print(COLORS["success"] + f"\nFound {len(matching_books)} matching books:")
        display_books(matching_books)
    else:
        print(COLORS["warning"] + f"No books found matching '{term}' in {search_by}.")

def display_books(books_to_display=None) -> None:
    """Display all books or a subset of books in a formatted table."""
    books_list = books_to_display if books_to_display is not None else library
    
    if not books_list:
        print(COLORS["warning"] + "Your library is empty.")
        return
    
    # Prepare data for tabulate
    table_data = []
    for i, book in enumerate(books_list, 1):
        read_status = Fore.GREEN + "Read" + Style.RESET_ALL if book['read'] else Fore.RED + "Unread" + Style.RESET_ALL
        table_data.append([
            i,
            Fore.CYAN + book['title'] + Style.RESET_ALL,
            Fore.MAGENTA + book['author'] + Style.RESET_ALL,
            Fore.YELLOW + str(book['year']) + Style.RESET_ALL,
            Fore.BLUE + book['genre'] + Style.RESET_ALL,
            read_status
        ])
    
    headers = ["#", "Title", "Author", "Year", "Genre", "Status"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def display_statistics() -> None:
    """Display statistics about the library."""
    if not library:
        print(COLORS["warning"] + "Your library is empty. No statistics available.")
        return
    
    print(COLORS["title"] + "\nLIBRARY STATISTICS")
    print(COLORS["title"] + "-" * 60)
    
    with yaspin(Spinners.dots, text=colored("Calculating statistics...", "yellow")) as spinner:
        total_books = len(library)
        read_books = sum(1 for book in library if book['read'])
        percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
        
        # Count books by genre
        genres = {}
        for book in library:
            genre = book['genre']
            genres[genre] = genres.get(genre, 0) + 1
        
        # Author statistics
        authors = {}
        for book in library:
            author = book['author']
            authors[author] = authors.get(author, 0) + 1
            
        time.sleep(0.8)  # For effect
        spinner.ok("✅")
    
    # Display statistics
    print(COLORS["info"] + f"Total books: {total_books}")
    print(COLORS["info"] + f"Read books: {read_books}")
    print(COLORS["info"] + f"Unread books: {total_books - read_books}")
    print(COLORS["info"] + f"Percentage read: {percentage_read:.1f}%")
    
    # Display genre distribution
    print(COLORS["title"] + "\nGenre Distribution:")
    print(COLORS["title"] + "-" * 60)
    
    genre_data = []
    for genre, count in sorted(genres.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_books) * 100
        genre_data.append([
            Fore.MAGENTA + genre + Style.RESET_ALL,
            count,
            f"{percentage:.1f}%"
        ])
    
    print(tabulate(genre_data, headers=["Genre", "Count", "Percentage"], tablefmt="simple"))
    
    # Author statistics
    if len(authors) > 1:  # Only show if we have multiple authors
        print(COLORS["title"] + "\nTop Authors:")
        print(COLORS["title"] + "-" * 60)
        
        author_data = []
        for author, count in sorted(authors.items(), key=lambda x: x[1], reverse=True)[:5]:  # Top 5 authors
            percentage = (count / total_books) * 100
            author_data.append([
                Fore.CYAN + author + Style.RESET_ALL,
                count,
                f"{percentage:.1f}%"
            ])
        
        print(tabulate(author_data, headers=["Author", "Books", "Percentage"], tablefmt="simple"))

def read_book() -> None:
    """Read a book from the library."""
    if not library:
        print(COLORS["warning"] + "Your library is empty. Nothing to read.")
        return
    
    print(COLORS["title"] + "\nREAD A BOOK")
    print(COLORS["title"] + "-" * 60)
    
    # First, let the user search for a book
    questions = [
        inquirer.List('search_by',
                     message="Find a book by",
                     choices=['Title', 'Author', 'Genre', 'Year', 'Show All Books']),
    ]
    
    answers = inquirer.prompt(questions)
    
    if not answers:
        return
    
    search_by = answers['search_by']
    matching_books = []
    
    if search_by == 'Show All Books':
        matching_books = library
    else:
        search_by = search_by.lower()
        search_term = inquirer.prompt([
            inquirer.Text('term', message=f"Enter the {search_by}")
        ])
        
        if not search_term:
            return
        
        term = search_term['term'].lower()
        
        # Search for matching books
        with yaspin(Spinners.dots, text=colored("Searching your collection...", "blue")) as spinner:
            if search_by == 'year':
                try:
                    year_term = int(term)
                    matching_books = [book for book in library if book['year'] == year_term]
                except ValueError:
                    matching_books = []
                    spinner.fail("❌")
                    print(COLORS["warning"] + "Invalid year format.")
                    return
            else:
                matching_books = [
                    book for book in library 
                    if term in str(book[search_by]).lower()
                ]
            time.sleep(0.8)  # For effect
            spinner.ok("✅")
    
    if not matching_books:
        print(COLORS["warning"] + "No matching books found.")
        return
    
    # Display the matching books
    print(COLORS["success"] + f"\nFound {len(matching_books)} books:")
    display_books(matching_books)
    
    # Let the user select a book to read
    book_choices = [f"{book['title']} by {book['author']}" for book in matching_books]
    book_choices.append("Cancel")
    
    book_selection = inquirer.prompt([
        inquirer.List('book',
                     message="Select a book to read",
                     choices=book_choices),
    ])
    
    if not book_selection or book_selection['book'] == "Cancel":
        return
    
    selected_book_title = book_selection['book']
    
    # Find the selected book
    selected_book = None
    for book in matching_books:
        if f"{book['title']} by {book['author']}" == selected_book_title:
            selected_book = book
            break
    
    if not selected_book:
        print(COLORS["error"] + "Book not found.")
        return
    
    # Display the book reading interface with loading animation
    with yaspin(Spinners.bouncingBar, text=colored("Opening book...", "cyan")) as spinner:
        time.sleep(1)  # For effect
        spinner.ok("📖")
    
    clear_screen()
    print(COLORS["title"] + "=" * 60)
    print(COLORS["title"] + f"READING: {selected_book['title']}")
    print(COLORS["title"] + "=" * 60)
    print(COLORS["highlight"] + f"Author: {selected_book['author']}")
    print(COLORS["highlight"] + f"Year: {selected_book['year']}")
    print(COLORS["highlight"] + f"Genre: {selected_book['genre']}")
    print(COLORS["title"] + "-" * 60)
    
    # Display book content or a placeholder
    if 'content' in selected_book and selected_book['content']:
        print(COLORS["book_text"] + "\n" + selected_book['content'])
    else:
        print(COLORS["book_text"] + "\nThis book has no content or excerpt available.")
        print(COLORS["book_text"] + "You can add content when adding or editing a book.")
    
    print(COLORS["title"] + "\n" + "-" * 60)
    
    # If the book was unread, ask if the user wants to mark it as read
    if not selected_book['read']:
        mark_read = inquirer.prompt([
            inquirer.Confirm('mark_read',
                            message="Would you like to mark this book as read?",
                            default=True)
        ])
        
        if mark_read and mark_read['mark_read']:
            # Find the book in the main library and mark it as read
            with yaspin(Spinners.dots, text=colored("Updating read status...", "green")) as spinner:
                for book in library:
                    if book['title'] == selected_book['title'] and book['author'] == selected_book['author']:
                        book['read'] = True
                        time.sleep(0.5)  # For effect
                        spinner.ok("✅")
                        print(COLORS["success"] + f"\nMarked '{book['title']}' as read!")
                        break

def main_menu() -> None:
    """Display the main menu and handle user choices."""
    while True:
        display_header()
        
        questions = [
            inquirer.List('choice',
                         message="What would you like to do?",
                         choices=[
                             'Add a book',
                             'Remove a book',
                             'Search for a book',
                             'Read a book',
                             'Display all books',
                             'Display statistics',
                             'Save library',
                             'Exit'
                         ]),
        ]
        
        answers = inquirer.prompt(questions)
        
        if not answers:
            break
        
        choice = answers['choice']
        
        if choice == 'Add a book':
            add_book()
        elif choice == 'Remove a book':
            remove_book()
        elif choice == 'Search for a book':
            search_book()
        elif choice == 'Read a book':
            read_book()
        elif choice == 'Display all books':
            print(COLORS["title"] + "\nYOUR LIBRARY")
            print(COLORS["title"] + "-" * 60)
            display_books()
        elif choice == 'Display statistics':
            display_statistics()
        elif choice == 'Save library':
            save_library()
        elif choice == 'Exit':
            with yaspin(Spinners.bouncingBar, text=colored("Saving your library before exit...", "yellow")) as spinner:
                save_library()
                time.sleep(0.5)  # For effect
                spinner.ok("👋")
            
            print(COLORS["title"] + "\nThank you for using the Library Manager!")
            print(COLORS["title"] + "=" * 60)
            title_text = pyfiglet.figlet_format("By ausaf ul islam", font="small")
            print(COLORS["warning"] + f"{title_text}")
            print(COLORS["title"] + "=" * 60)
            break
        
        # Pause before showing the menu again
        input("\nPress Enter to continue...")

def main():
    """Personal Library Manager - Manage your book collection."""
    clear_screen()
    
    # Display welcome message with loading animation
    title_text = pyfiglet.figlet_format("Library Manager", font="slant")
    print(COLORS["title"] + title_text)
    print(COLORS["title"] + "=" * 60)
    print(COLORS["info"] + "Welcome to your Personal Library Manager!")
    
    with yaspin(Spinners.bouncingBar, text=colored("Initializing...", "magenta")) as spinner:
        time.sleep(1)  # For effect
        spinner.ok("✅")
    
    load_library()
    main_menu()

if __name__ == "__main__":
    main()