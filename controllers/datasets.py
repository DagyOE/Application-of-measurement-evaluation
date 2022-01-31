import pandas as pd
import os
import os.path
import sqlite3

con = sqlite3.connect(os.getcwd() + '/database.db')
cur = con.cursor()

class Dataset():

    def __init__(self):
        pass

    def loadDatasets(self):
        query = "SELECT * FROM datasets"
        datasets = cur.execute(query).fetchall()
        return datasets

    def addDataset(self, url, name):
        ok = True
        for arr in os.listdir('datasets'):
            if arr.split('.')[0] == name:
                ok = False
        if ok:
            data = pd.read_csv(url, delimiter='\t', names=['id', 'date-time', 'x', 'y', 'res', 'final'])
            data.to_csv('datasets/' + name + '.csv')
            filelink = 'datasets/' + name + '.csv'
            try:
                query = "INSERT INTO datasets (name,link) VALUES(?,?)"
                cur.execute(query, (name, filelink))
                con.commit()
                return filelink
            except:
                filelink = 1
                return filelink
        else:
            filelink = 0
            return filelink

    def deleteDataset(self, item):
        query = "SELECT * FROM datasets"
        datasets = cur.execute(query).fetchall()
        for dataset in datasets:
            if dataset[1] == item.split(" - ")[0]:
                query = "DELETE FROM datasets WHERE id=?"
                cur.execute(query, (dataset[0],))
                con.commit()
                os.remove(os.path.join("datasets", dataset[1] + ".csv"))