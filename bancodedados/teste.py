import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",          
        password="123abc",   
        database="usuarios_db"
    )

    if conn.is_connected():
        print("✅ Conexão com MySQL bem-sucedida!")

except mysql.connector.Error as e:
    print("❌ Erro na conexão:", e)

finally:
    if conn.is_connected():
        conn.close()
