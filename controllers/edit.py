import os
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

con = sqlite3.connect(os.getcwd() + '/database.db')
cur = con.cursor()


class Edit():

    def __init__(self):
        self.x = []
        self.y = []

    def OpenProtocolData(self, protocol_name):
        query = "SELECT * FROM protocols"
        protocols = cur.execute(query).fetchall()
        for protocol in protocols:
            if protocol[1] == protocol_name:
                data = pd.read_csv(protocol[3], usecols=['x', 'y'])
                for index, row in data.iterrows():
                    self.x.append(row.x)
                    self.y.append(row.y)
                return self.x, self.y, protocol

    def CreateNewData(self, check, protocol_data):
        data = {
            "x": self.x,
            "y": self.y,
            "check": check
        }
        i = 0
        for n in data["check"]:
            if n == "0":
                data['x'][i] = "NaN"
                data['y'][i] = "NaN"
            i += 1
        df = pd.DataFrame(data)
        df.loc[df.x == "NaN", :] = np.nan
        border_csv = pd.read_csv(protocol_data[4], usecols=['x', 'y'])
        border = {
            "xmin": (border_csv.mean()[0] - (border_csv.max()[0] - border_csv.min()[0]) * 1),
            "xmax": (border_csv.mean()[0] + (border_csv.max()[0] - border_csv.min()[0]) * 1),
            "ymin": (border_csv.mean()[1] - (border_csv.max()[1] - border_csv.min()[1]) * 1),
            "ymax": (border_csv.mean()[1] + (border_csv.max()[1] - border_csv.min()[1]) * 1)
        }
        average = []
        od = 0
        do = protocol_data[5]
        for i in range(0, (int(len(df) / protocol_data[5]))):
            average.append({
                "id": i + 1,
                "x": df[od:do].mean()[0],
                "y": df[od:do].mean()[1],
            })
            od += protocol_data[5]
            do += protocol_data[5]
        for ave in average:
            if ave["x"] < border["xmax"] and ave["x"] > border["xmin"] and ave["y"] < border["ymax"] and ave["y"] > \
                    border["ymin"]:
                if np.isnan(ave["x"]) == False and np.isnan(ave["y"]) == False:
                    ave["valid"] = "OK"
                else:
                    ave["valid"] = "KO"
                    ave.pop("x")
                    ave.pop("y")
            else:
                if np.isnan(ave["x"]) == False and np.isnan(ave["y"]) == False:
                    ave["valid"] = "KO"
                else:
                    ave["valid"] = "KO"
                    ave.pop("x")
                    ave.pop("y")
        id = 0
        i = 0
        row = []
        data_all = []
        for index, rows in df.iterrows():
            id += 1
            if rows.x < border["xmax"] and rows.x > border["xmin"] and rows.y < border["ymax"] and rows.y > border[
                "ymin"]:
                if np.isnan(rows.x) == False and np.isnan(rows.y) == False:
                    my_list = {
                        'id': id,
                        'x': rows.x,
                        'y': rows.y,
                        'valid': "OK",
                    }
                else:
                    my_list = {
                        'id': id,
                        'valid': "KO"
                    }
            else:
                if np.isnan(rows.x) == False and np.isnan(rows.y) == False:
                    my_list = {
                        'id': id,
                        'x': rows.x,
                        'y': rows.y,
                        'valid': "KO",
                    }
                else:
                    my_list = {
                        'id': id,
                        'valid': "KO"
                    }

            row.append(my_list)
            if id == protocol_data[5]:
                i += 1
                data_all.append([i, row])
                id = 0
                row = []
        now = datetime.now()
        date = now.strftime("%d.%m.%Y" + " " + "%H:%M:%S")
        name = "EDIT-" + now.strftime("%d-%m-%Y-%H-%M-%S") + " - " + protocol_data[1]
        data_name = "EDIT-" + now.strftime("%d-%m-%Y-%H-%M-%S") + " - " + protocol_data[3].split("/")[1]
        protocol_link = "protocols/" + name + ".html"
        data_link = "data/" + data_name
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('template.html')
        template_vars = {"protocol_name": name,
                         "batch": protocol_data[7],
                         "grid": protocol_data[8],
                         "number": protocol_data[9],
                         "melt": protocol_data[10],
                         "material": protocol_data[11],
                         "num": protocol_data[5],
                         "furnance": protocol_data[12],
                         "note": protocol_data[13],
                         "user_name": protocol_data[14],
                         "user_surname": protocol_data[15],
                         "id": protocol_data[16],
                         "date": date,
                         "data_ave": average,
                         "measuringAll": data_all}
        html_out = template.render(template_vars)
        with open("protocols/" + name + ".html", "wb") as file_:
            file_.write(html_out.encode("utf-8"))
        data_all = pd.DataFrame(data_all)
        data_all.to_csv("data/" + data_name)

        query = "INSERT INTO protocols (protocol_name, protocol_link, data_link, border_link, num, tag," \
                "batch, grid, number, melt, material, furnance, note, user_name, user_surname, user_id, date)" \
                " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        cur.execute(query, (name, protocol_link, data_link, protocol_data[4], protocol_data[5], protocol_data[6],
                            protocol_data[7], protocol_data[8], protocol_data[9], protocol_data[10], protocol_data[11],
                            protocol_data[12], protocol_data[13], protocol_data[14], protocol_data[15],
                            protocol_data[16], date))
        con.commit()

    def ClearList(self):
        self.x.clear()
        self.y.clear()
