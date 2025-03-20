<!--Code File to save library data into TXT file  -->
def save_books_to_file(connection, file_path="library.txt"):
    try:
        cursor= connection.cursor()
        query= "SELECT * FROM Books"
        cursor.execute(query)
        results= cursor.fetchall()
        cursor.close()

        with open(file_path, "w") as file:
            for row in results:
                file.write(f"{row}\n")

        print(f"Books data saved to {file_path}")
    except Error as e:
        print(f"Failed to save books to file: {e}")