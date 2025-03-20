from mysql.connector import Error
from utils.functions import connect_to_mysql, add_book, book_data, remove_book, get_book_title, get_search_input, search_books, display_all_books, display_statistics, save_books_to_file
import inquirer

# Function for selection of Task

def main(conn):  # 
    while True:
        questions = [
            inquirer.List(
                "task",
                message="📚 Personal Library Manager - Choose an option",
                choices=[
                    "📖 Add a book",
                    "❌ Remove a book",
                    "🔎 Search for a book",
                    "📚 Display all books",
                    "📊 Display statistics",
                    "💾 Save books to file",
                    "🚪 Exit"
                ]
            )
        ]
        choice = inquirer.prompt(questions)["task"]

        if choice == "📖 Add a book":
            add_book(conn, **book_data())  # ✅ Use conn properly
        elif choice == "❌ Remove a book":
            title_to_remove = get_book_title()
            remove_book(conn, title_to_remove)
        elif choice == "🔎 Search for a book":
            search_term = get_search_input()
            search_books(conn, search_term)
        elif choice == "📚 Display all books":
            display_all_books(conn)
        elif choice == "📊 Display statistics":
            display_statistics(conn)
        elif choice == "💾 Save books to file":
            save_books_to_file(conn)  
        elif choice == "🚪 Exit":
            print("Goodbye! 👋")
            break  

        
if __name__ == "__main__":
  conn =  connect_to_mysql()
  
  if conn:

    main(conn)      
    conn.close()

