import pandas
import os
import datetime


def isfloat(x):
    try:
        a = float(x)
    except ValueError:
        return False
    else:
        return True

def isDate(x):
    try:
        x = x.replace("-","")
        y = datetime.datetime.strptime(x, "%Y%m%d").date()
    except ValueError:
        print("Para las fechas es aaaa-mm-dd, ejemplo 2017-08-09")
        return False
    else:
        return y

def exist_db(db):
    df = pandas.read_csv("database_info.csv")
    dbs = df["name_db"].tolist()
    return  db in dbs (df["eliminacion"][df["name_db"] == db].tolist()[0] == "null")

def exist_tb(db,tb):
    df = pandas.read_csv(os.getcwd()+"/"+db+"/tables_info.csv")
    tbs = df["name_tabla"].tolist()
    return  (tb in tbs) and (df["eliminacion"][df["name_tabla"] == tb].tolist()[0] == "null")

def exist_campo(db,tb,campo):
    df = pandas.read_csv(os.getcwd()+"/"+db+"/"+tb+"/"+tb+"_info.csv")
    campos = df["name_data"].tolist()
    return campo in campos

def correct_type(db,tb,nombre_campo,valor):
    df = pandas.read_csv(os.getcwd() + "/" + db + "/" + tb + "/"+tb+"_info.csv")
    campo = df[df["name_data"] == nombre_campo].values.tolist()
    tipo = campo[0][2] #captura el tipo
    if (tipo == "int"):
        return isfloat(valor)
    elif (tipo == "date"):
        return type(isDate(valor)) == datetime.date
    else: #tipo varchar
        size = campo[0][3]
        return len(valor) < int(size)


