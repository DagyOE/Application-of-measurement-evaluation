import os
import sqlite3
import webbrowser

con = sqlite3.connect(os.getcwd() + '/database.db')
cur = con.cursor()

class Protocols():

    def __init__(self):
        pass

    def loadProtocols(self):
        query = "SELECT * FROM protocols"
        protocols = cur.execute(query).fetchall()
        return protocols

    def openProtocol(self, name):
        filename = 'file:///' + os.getcwd() + '/' + 'protocols/' + name + '.html'
        webbrowser.open_new_tab(filename)

    def deleteProtocol(self, name):
        query = "SELECT * FROM protocols"
        protocols = cur.execute(query).fetchall()
        for protocol in protocols:
            if protocol[1] == name:
                query = "DELETE FROM protocols WHERE id=?"
                cur.execute(query, (protocol[0],))
                con.commit()
                os.remove(os.path.join(protocol[2]))
                os.remove(os.path.join(protocol[3]))