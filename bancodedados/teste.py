import mysql.connector
from mysql.connector import Error

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123abc",
        database="usuarios_db"
    )

    if conn.is_connected():
        print("✅ Conexão com MySQL bem-sucedida!")

except Error as e:
    print("❌ Erro na conexão:", e)

finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("🔒 Conexão encerrada.")
