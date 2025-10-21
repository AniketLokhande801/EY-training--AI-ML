import mysql.connector

# 🔧 Update these credentials for your MySQL Workbench setup
config = {
    'host': 'localhost',
    'user': 'root',               # your MySQL username
    'password': '1234',  # your MySQL password
    'database': 'student_management'
}


def get_connection():
    """
    Create and return a MySQL connection.
    """
    return mysql.connector.connect(**config)


def init_db():
    """
    Initialize the MySQL database:
      - Create database if not exists
      - Create table if not exists
      - Insert initial data only if table is empty
    """
    # Step 1: Connect to MySQL server (without selecting DB yet)
    conn = mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        use_pure=True
    )
    cursor = conn.cursor()

    # Step 2: Create database if not exists
    cursor.execute("CREATE DATABASE IF NOT EXISTS student_management")
    conn.commit()

    # Step 3: Switch to this database
    cursor.execute("USE student_management")

    # Step 4: Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            StudentID INT PRIMARY KEY,
            Name VARCHAR(50),
            Age INT,
            Course VARCHAR(50)
        )
    """)
    conn.commit()

    # Step 5: Check if data exists
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]

    # Step 6: Insert initial records only if empty
    if count == 0:
        insert_query = """
            INSERT INTO students (StudentID, Name, Age, Course) VALUES
            (101, 'Neha', 21, 'AI'),
            (102, 'Arjun', 22, 'ML'),
            (103, 'Sophia', 20, 'Data Science'),
            (104, 'Ravi', 23, 'AI'),
            (105, 'Meena', 21, 'ML');
        """
        cursor.execute(insert_query)
        conn.commit()
        print("✅ Initial data inserted successfully into MySQL database.")
    else:
        print("ℹ️  Data already exists in the students table — skipping initial insert.")

    conn.close()


# Run this file directly to create DB, table, and initial data
if __name__ == "__main__":

    init_db()
