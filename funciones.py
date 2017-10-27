import pandas
import os
import datetime
import avl_tree

def isfloat(x):
    try:
        a = float(x)
    except ValueError:
        return False
    else:
        return a

def toDate(x):
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
    return  db in dbs and (df["eliminacion"][df["name_db"] == db].tolist()[0] == "null")

def exist_tb(db,tb):
    df = pandas.read_csv(os.getcwd()+"/"+db+"/tables_info.csv")
    tbs = df["name_tabla"].tolist()
    return  (tb in tbs) and (df["eliminacion"][df["name_tabla"] == tb].tolist()[0] == "null")

def exist_campo(db,tb,campo):
    df = pandas.read_csv(os.getcwd()+"/"+db+"/"+tb+"/"+tb+"_info.csv")
    campos = df["name_data"].tolist()
    #print("Los campos son",campos)
    return campo in campos

def correct_type(db,tb,nombre_campo,valor):
    df = pandas.read_csv(os.getcwd() + "/" + db + "/" + tb + "/"+tb+"_info.csv")
    campo = df[df["name_data"] == nombre_campo].values.tolist()
    tipo = campo[0][2] #captura el tipo
    if (tipo == "int"):
        return isfloat(valor)
    elif (tipo == "date"):
        return type(toDate(valor)) == datetime.date
    else: #tipo varchar
        size = campo[0][3]
        return len(valor) < int(size)

def getType(db,tb,nombre_campo):
    df = pandas.read_csv(os.getcwd() + "/" + db + "/" + tb + "/"+tb+"_info.csv")
    campo = df[df["name_data"] == nombre_campo].values.tolist()
    tipo = campo[0][2] #captura el tipo
    return tipo

def toType(db,tb,nombre_campo,valor):
    tipo = getType(db,tb,nombre_campo)
    if (tipo == "int"):
        return isfloat(valor)
    # elif (tipo == "date"):
    #     return toDate(valor)
    else: #tipo varchar
        return valor

def iterador_avl(lista_indices,nombre_indice):
    it = 0
    for i in lista_indices:
        if i.name == nombre_indice:
            return it
        it += 1
    if it==len(lista_indices):
        return -1
