import pandas as pd
from datetime import datetime
import os.path
import sqlite3

con = sqlite3.connect(os.getcwd() + '/database.db')
cur = con.cursor()

class Load():

    def __init__(self):
        self.data = False
        self.url = False
        self.borders = False
        self.num = False
        self.all = False
        self.tag_name = False
        self.create = False

    def loadData(self, url, num):
        self.num = num
        now = datetime.now()
        date = now.strftime("%Y-%m-%d-%H-%M-%S-")
        name = url.split("/")[-1].split(".")[0]
        data = pd.read_csv(url, delimiter='\t', names=['id', 'date-time', 'x', 'y', 'res', 'final'])
        self.url = 'stamps/' + date + name + '.csv'
        data.to_csv(self.url)
        measured_data = pd.read_csv(self.url, usecols=['x', 'y'])
        self.data = []
        x = 0
        y = self.num
        for i in range(0, (int(len(measured_data)/self.num))):
            self.data.append({
                "id": i+1,
                "x": measured_data[x:y].mean()[0],
                "y": measured_data[x:y].mean()[1],
            })
            x += self.num
            y += self.num
        return self.data

    def border_points(self, url):
        points = pd.read_csv(url, usecols=['x', 'y'])
        self.borders = {
            "xmin": (points.mean()[0] - (points.max()[0] - points.min()[0]) * 1),
            "xmax": (points.mean()[0] + (points.max()[0] - points.min()[0]) * 1),
            "ymin": (points.mean()[1] - (points.max()[1] - points.min()[1]) * 1),
            "ymax": (points.mean()[1] + (points.max()[1] - points.min()[1]) * 1),
        }
        return self.borders

    def check_valid(self):
        checked = []
        for point in self.data:
            if point['x'] < self.borders['xmax'] and point['x'] > self.borders['xmin'] and point['y'] < \
                    self.borders['ymax'] and point['y'] > self.borders['ymin']:
                checked.append({
                    "id": point['id'],
                    "check": "OK",
                })
            else:
                checked.append({
                    "id": point['id'],
                    "check": "NO",
                })
        self.ok = 0
        self.no = 0
        for check in checked:
            if check['check'] == "OK":
                self.ok += 1
            elif check['check'] == "NO":
                self.no += 1
        return checked

    def result(self, num):
        name = self.url.split("/")[-1].split("-")[-2]
        print(name)
        data = pd.read_csv(self.url)
        query = "SELECT * FROM tags"
        tags = cur.execute(query).fetchall()
        for tag in tags:
            print(tag[1])
            if tag[1] == name:
                self.tag_name = tag[2]
                break
            else:
                self.tag_name = False
        if self.tag_name is not False:
            result = {
                "name": self.tag_name,
                "date": data.iloc[0]['date-time'].split(' ')[0],
                "time": data.iloc[0]['date-time'].split(' ')[1].split('.')[0],
                "onePiece": num,
                "all": len(data),
                "ok": self.ok,
                "no": self.no,
            }
            return result
        else:
            print("chyba2")
            return False

    def single(self, id):
        data = pd.read_csv(self.url, usecols=['x', 'y'])
        x = (int(id) - 1) * self.num
        y = x + self.num
        row = []
        id = 0
        for index, rows in data[x:y].iterrows():
            id += 1
            my_list = [id, rows.x, rows.y]
            row.append(my_list)
        return row
