import sqlite3

conn = sqlite3.connect('articlesWSJ.db')
cursor = conn.cursor()

cursor.execute("""
SELECT link, MIN(id)
FROM articles_index
GROUP BY link
HAVING COUNT(link) > 1;
""")

duplicates = cursor.fetchall()

counter = 0
for link, min_id in duplicates:
    print(f"Deleting duplicate for Link: {link}, ID: {min_id}")
    cursor.execute("DELETE FROM articles_index WHERE id = ?", (min_id,))
    counter += 1

conn.commit()
conn.close()

print(f'{counter} elements deleted')
