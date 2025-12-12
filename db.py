import mysql.connector
import json

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NewPassword123!",
    database="pick_my_movie"
)
cur = conn.cursor()