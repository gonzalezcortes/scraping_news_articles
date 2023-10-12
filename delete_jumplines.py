import sqlite3

conn = sqlite3.connect("articlesWSJ.db")
cursor = conn.cursor()

query_fetch = "SELECT id, headline FROM articles_index"

query_update = "UPDATE articles_index SET headline = ? WHERE id = ?"

cursor.execute(query_fetch)
rows = cursor.fetchall()

for row in rows:
    id, headline = row
    if "\n" in headline:
        new_headline = headline.replace("\n", "")
        
        cursor.execute(query_update, (new_headline, id))
        conn.commit()
        
        print(f"ID {id} was modified to: {new_headline}")

conn.close()
print("end")
