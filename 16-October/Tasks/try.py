import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="student_capstone",
        use_pure=True
    )
    print("✅ Connection successful.")
    conn.close()
except mysql.connector.Error as err:
    print("❌ Connection error:", err)
