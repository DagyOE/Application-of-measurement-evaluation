import os.path
import sqlite3
import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import pandas as pd
import shutil

con = sqlite3.connect(os.getcwd() + '/database.db')
cur = con.cursor()

class Render():

    def __init__(self):
        pass

    def ProtocolRender(self, ave, link, num, userData, border, border_link):
        for value in ave:
            if value["x"] < border["xmax"] and value["x"] > border["xmin"] and value["y"] < border["ymax"] \
                    and value["y"] > border["ymin"]:
                value["valid"] = "OK"
            else:
                value["valid"] = "KO"
        df = pd.read_csv(link, usecols=['x', 'y'])
        id = 0
        i = 0
        row = []
        data_all = []
        for index, rows in df.iterrows():
            id += 1
            if rows.x < border["xmax"] and rows.x > border["xmin"] and rows.y < border["ymax"] and rows.y > border[
                "ymin"]:
                my_list = {
                    'id': id,
                    'x': rows.x,
                    'y': rows.y,
                    'valid': "OK",
                }
            else:
                my_list = {
                    'id': id,
                    'x': rows.x,
                    'y': rows.y,
                    'valid': "KO",
                }
            row.append(my_list)
            if id == num:
                i += 1
                data_all.append([i, row])
                id = 0
                row = []
        now = datetime.now()
        tag = link.split('/')[-1].split('-')[8]
        name = link.split('/')[-1].split('-')[7] + " - " + link.split('/')[-1].split('-')[8] + \
               " - " + link.split('/')[-1].split('-')[9].split('.')[0] + " - " + link.split('/')[-1].split('-')[2] +\
               " - " + link.split('/')[-1].split('-')[1] + " - " + link.split('/')[-1].split('-')[0] + " - " + \
               now.strftime("%d-%m-%Y-%H-%M-%S")
        date = now.strftime("%d.%m.%Y" + " " + "%H:%M:%S")
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('template.html')
        template_vars = {"protocol_name": name,
                         "batch": userData['batch'],
                         "grid": userData['grid'],
                         "number": userData['number'],
                         "melt": userData['melt'],
                         "material": userData['material'],
                         "num": num,
                         "furnance": userData['furnance'],
                         "note": userData['note'],
                         "user_name": userData['name'],
                         "user_surname": userData['surname'],
                         "id": userData['id'],
                         "date": date,
                         "data_ave": ave,
                         "measuringAll": data_all}
        html_out = template.render(template_vars)
        with open("protocols/" + name + ".html", "wb") as file_:
            file_.write(html_out.encode("utf-8"))
        protocol_link = "protocols/" + name + ".html"
        data_link = "data/" + link.split("/")[-1]
        if os.path.exists(link):
            shutil.move(link, data_link)
        query = "INSERT INTO protocols (protocol_name, protocol_link, data_link, border_link, num, tag," \
                "batch, grid, number, melt, material, furnance, note, user_name, user_surname, user_id, date)" \
                " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        cur.execute(query, (name, protocol_link, data_link, border_link, num, tag, userData['batch'], userData['grid'],
                            userData['number'], userData['melt'], userData['material'], userData['furnance'],
                            userData['note'], userData['name'], userData['surname'], userData['id'], date))
        con.commit()
        for f in os.listdir("stamps/"):
            os.remove(os.path.join("stamps/", f))

        ok = True
        return ok, name, protocol_link