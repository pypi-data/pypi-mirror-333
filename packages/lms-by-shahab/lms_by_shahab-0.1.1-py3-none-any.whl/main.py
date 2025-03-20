from utils.functions import (
    connect_to_mysql,
    add_book,
    book_data,
    display_all_books,
    display_statistics,
    search_books,
    userInput,
    remove_book
)
from mysql.connector import Error
import inquirer

if __name__ == "__main__":
    conn = connect_to_mysql()
    if conn:
        def main():
            exitFunc = True
            while exitFunc:
                questions = [
                    inquirer.List(
                        name="option",  # Required parameter: the answer key will be "option"
                        message="What do you want to do?",
                        choices=[
                            "Add a book",
                            "Remove a book",
                            "Search for a book",
                            "Display all books",
                            "Display book statistics",
                            "Exit",
                        ]
                    )
                ]
                answers = inquirer.prompt(questions)
                option = answers["option"]
                print(f"You selected: {option}")
                
                if option == "Add a book":
                    print("Adding a book...")
                    # Call book_data() to collect book details and add the book
                    book_info = book_data()
                    add_book(conn, **book_info)
                    
                elif option == "Remove a book":
                    print("Removing a book...")
                    # Prompt for the title of the book to remove
                    title_to_remove = userInput("Enter the book title to remove: ")
                    remove_book(conn, title_to_remove)
                    
                elif option == "Search for a book":
                    print("Searching for a book...")
                    search_term = userInput("Enter Book Title or Author: ")
                    search_books(conn, search_term)
                    
                elif option == "Display all books":
                    print("Displaying all books...")
                    display_all_books(conn)
                    
                elif option == "Display book statistics":
                    print("Displaying book statistics...")
                    display_statistics(conn)
                    
                elif option == "Exit":
                    print("Thank you for using the library management system by Shahabuddin!")
                    exitFunc = False

        main()
        conn.close()


