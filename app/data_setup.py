import sqlite3                      
import hashlib                      
import secrets                     

DB_FILE="data.db"

#=============================MAKE=TABLES=============================#

# users
def create_users_table():
    contents =  """
                CREATE TABLE IF NOT EXISTS users (
                user_id     INTEGER  PRIMARY KEY AUTOINCREMENT,
                username    TEXT     NOT NULL,
                password    TEXT     NOT NULL,
                bio         TEXT     NOT NULL    
                )"""
    create_table(contents)

def create_games_table():
    contents = """
               CREATE TABLE IF NOT EXISTS games (
               game_id      INTEGER  PRIMARY KEY AUTOINCREMENT,
               deck_tiles   TEXT     NOT NULL,
               p1           TEXT     NOT NULL,
               p2           TEXT     NOT NULL,
               p3           TEXT     NOT NULL,
               p4           TEXT     NOT NULL
               )"""
    create_table(contents)
               
#=============================GENERAL=HELPERS=============================#

def create_table(contents):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute(contents)
    db.commit()
    db.close()