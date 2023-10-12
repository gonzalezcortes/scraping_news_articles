import sqlite3

name = 'articlesWSJ.db'
conn = sqlite3.connect(name)

c = conn.cursor()

# Table "articles_index"
c.execute('''CREATE TABLE IF NOT EXISTS articles_index (
          id INTEGER PRIMARY KEY AUTOINCREMENT, 
          
          year TEXT, 
          month TEXT, 
          day TEXT, 
          
          headline TEXT, 
          article_time TEXT,
          
          keyword TEXT,
          link TEXT, 
          
          scraped_at TEXT,
          scanned_status INTEGER)''')

# Table "article"
c.execute('''CREATE TABLE IF NOT EXISTS article (
                article_id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_src TEXT,

                scanned_time TEXT,
                title TEXT,
                sub_title TEXT,


                corpus TEXT,
                index_id INTEGER,

                FOREIGN KEY(index_id) REFERENCES articles_index(id))''')


c.execute('''CREATE TABLE IF NOT EXISTS exploration (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          link TEXT,
          
          year TEXT, 
          month TEXT, 
          day TEXT, 
          page_num TEXT,
          
          checked_at TEXT,
          values_or_not INTEGER,
          count_articles INTEGER
          );
''')

conn.commit()
conn.close()

print("DB and tables created")
