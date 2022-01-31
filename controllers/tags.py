import os
import os.path
import sqlite3

con = sqlite3.connect(os.getcwd() + '/database.db')
cur = con.cursor()

class Tags():

    def __init__(self):
        pass

    def loadTags(self):
        query = "SELECT * FROM tags"
        tags = cur.execute(query).fetchall()
        return tags

    def addTag(self, name, tag):
        ok = True
        query = "SELECT name, tag FROM tags"
        datasets = cur.execute(query).fetchall()
        for dataset in datasets:
            if dataset[0] == name or dataset[1] == tag:
                ok = False
        if ok:
            query = "INSERT INTO tags (tag,name) VALUES(?,?)"
            cur.execute(query, (tag, name))
            con.commit()
            return True
        else:
            return False

    def deleteTag(self, item):
        query = "SELECT * FROM tags"
        tags = cur.execute(query).fetchall()
        for tag in tags:
            if tag[2] == item.split(" - ")[0]:
                query = "DELETE FROM tags WHERE id=?"
                cur.execute(query, (tag[0],))
                con.commit()