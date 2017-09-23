import pandas
import os

def exist_db(db):
    df = pandas.read_csv("database_info.csv")
    dbs = df["name_db"].tolist()
    return  db in dbs

def exist_tb(db,tb):
    df = pandas.read_csv(os.getcwd()+"/"+db+"/tables_info.csv")
    tbs = df["name_tabla"].tolist()
    return  tb in tbs

def exist_campo(db,tb,campo):
    df = pandas.read_csv(os.getcwd()+"/"+db+"/"+tb+"/tb2_info.csv")
    campos = df["name_data"].tolis()
    return campo in campos