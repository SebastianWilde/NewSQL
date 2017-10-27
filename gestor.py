import os #para usar las funciones del sistema operativo
import os.path as path
import shutil #para eliminar

import manejador_csv #para crear archivos csv para almancenar los datos

import datetime #para manejar fechas

import pandas #para sobreescribir csv

import time #medir el tiempo

import funciones

from avl_tree import AVLTree

from tabulate import tabulate

lista_indices = []

def procesar_comando(lista_comando):
    if lista_comando[0] == "CREATE":
        ruta = os.getcwd() + "/" #obteniendo la ruta actual
        comando_aux = lista_comando[1]
        comando_aux = comando_aux.split(maxsplit=1)
        if comando_aux[0] == "DATABASE":
            #Crea una carpeta para la base de datos que se crea
            nombre_db = comando_aux[1]
            if (funciones.exist_db(nombre_db) == True):
                print("Esa base de datos ya existe")
                return
            comando_system = "mkdir "+ ruta + nombre_db
            os.system(comando_system)
            #Agrega al archivo general de bases de datos el registro de la creacion
            #de una nueva base de datos
            today = datetime.date.today()
            input = [1,comando_aux[1],today,"null"]
            manejador_csv.escribir_csv(ruta,"database_info",input)
            #Crea el archivo que almacena informacion de las tablas
            header_tables_info = ["id", "name_tabla", "creacion", "eliminacion"]
            direccion = ruta + nombre_db +"/"
            manejador_csv.crear_archivo(direccion, "tables_info", header_tables_info)
            print("Base de datos creada")

        elif (comando_aux[0] == "TABLE"):
            tipos_aceptados = ['int','date','varchar']
            comando_aux2 = comando_aux[1]
            comando_aux2 = comando_aux2.split(maxsplit=3)
            if (comando_aux2[0]== "IN"):
                #Crea una carpeta para la tabla
                nombre_db = comando_aux2[1]
                if (funciones.exist_db(nombre_db) == False):
                    print("Esa base de datos no existe")
                    return
                nombre_tabla = comando_aux2[2]
                if(funciones.exist_tb(nombre_db,nombre_tabla) == True):
                    print("Error, esa base de datos ya existe")
                    return
                comando_system = "mkdir "+ ruta + nombre_db +"/"+nombre_tabla
                os.system(comando_system)
                #Actualizar archivos general de tablas
                today = datetime.date.today()
                input = [1,nombre_tabla,today,"null"]
                manejador_csv.escribir_csv(ruta + nombre_db +"/","tables_info",input)
                #Crea un directorio donde se almacena la informacion de los atributos
                header_table_info = ["id","name_data","type","size"]
                direccion = ruta +  nombre_db+"/"+nombre_tabla+ "/"
                manejador_csv.crear_archivo(direccion,nombre_tabla+"_info",header_table_info)
                #Crear la tabla propiamente dicha
                #Extraer las partes que tengan la metadata
                i = comando_aux2[3].find("(")
                j = comando_aux2[3].find(")")
                metadata = comando_aux2[3][i+1:j]
                metadata = metadata.replace(" ", "") #Quitando espacios
                metadata = metadata.split(",")
                header_metadata = []
                datos = []
                for elem in metadata:
                    aux = elem.split(":")
                    nombre_campo = aux[0]
                    it1 = aux[1].find("[")
                    if (it1 > 0):
                        tipo_campo = aux[1][0:it1]
                        it2 = aux[1].find("]")
                        tam_campo = aux[1][it1+1:it2]
                    else:
                        tipo_campo = aux[1]
                        tam_campo = "null"
                    #Comprobar si el tipo ingresado es valido
                    if ((tipo_campo not in tipos_aceptados ) == True):
                        print("Tipo de dato no aceptado", tipo_campo)
                        return
                    header_metadata.append(nombre_campo)
                    dato = [1,nombre_campo,tipo_campo,tam_campo]
                    datos.append(dato)

                manejador_csv.crear_archivo(direccion,nombre_tabla,header_metadata)
                manejador_csv.escribir_csv(direccion,nombre_tabla+"_info",datos)
                print("Tabla creada")
            else:
                print("Para crear tablas: CREATE TABLE IN nombre_db nombre_tabla")

        elif (comando_aux[0] == "INDEX"):
            comando_aux2 = comando_aux[1]
            #nombre ON tb1 db1 (col1,col2...)
            comando_aux2 = comando_aux2.split(maxsplit=4)
            nombre_indice = comando_aux2[0]
            if (comando_aux2[1] != "ON"):
                print("Error de sintaxis, debe ser CREATE INDEX name ON db1 tb1 (...)")
                return
            nombre_db = comando_aux2[2]
            if (funciones.exist_db(nombre_db) == False):
                print("Esa base de datos no existe")
                return
            nombre_tabla = comando_aux2[3]
            if (funciones.exist_tb(nombre_db, nombre_tabla) == False):
                print("Error, no existe esa tabla")
                return
            if (len(comando_aux2)<5):
                print("Faltan argumentos")
                return
            it1 = comando_aux2[4].find("(")
            it2 = comando_aux2[4].find(")")
            argumentos = comando_aux2[4][it1+1:it2]
            argumentos = argumentos.replace(" ","")
            argumentos = argumentos.split(",")
            for campo in argumentos:
                if (funciones.exist_campo(nombre_db, nombre_tabla, campo) == False):
                    print("Error, no existe ", campo)
                    return
            #print(argumentos)
            #Extraer indices y juntar columnas y subir el arbol
            test = [1,2,3,4]
            test2 = [9,8,7,5]
            temporal = AVLTree(test,test2,nombre_indice)
            lista_indices.append(temporal)
            print(funciones.iterador_avl(lista_indices,nombre_indice))
            print(funciones.iterador_avl(lista_indices,"balbla"))

        else:
            print("Error, comando no valido")
            return 0

    elif lista_comando[0] == "DROP":
        comando_aux = lista_comando[1]
        comando_aux = comando_aux.split(maxsplit=1)
        if comando_aux[0] == "DATABASE":
            nombre_db = comando_aux[1]
            if (funciones.exist_db(nombre_db) == False):
                print("Error, no existe base de datos")
                return
            shutil.rmtree(nombre_db)
            # Actulizar informacion general tabla
            df = pandas.read_csv("database_info.csv")
            df.loc[df["name_db"] == nombre_db, "eliminacion"] = datetime.date.today()
            df.to_csv("database_info.csv", index=False)
            #Print
            print("Base de datos eliminada")
        elif comando_aux[0] == "TABLE":
            comando_aux2 = comando_aux[1].split(maxsplit=3)
            if comando_aux2[0] == "IN":
                nombre_db = comando_aux2[1]
                if (funciones.exist_db(nombre_db) == False):
                    print("Error, no existe base de datos")
                    return
                nombre_tabla = comando_aux2[2]
                if(funciones.exist_tb(nombre_db,nombre_tabla) == False):
                    print("Error, no existe la table")
                    return
                ruta_delete = os.getcwd() + "/"+nombre_db+"/"+nombre_tabla
                shutil.rmtree(ruta_delete)
                #Actulizar informacion general tabla
                update_tabla_info_ruta = os.getcwd() + "/"+nombre_db+"/"+"tables_info.csv"
                df = pandas.read_csv(update_tabla_info_ruta)
                df.loc[df["name_tabla"] == nombre_tabla, "eliminacion"] = datetime.date.today()
                df.to_csv(update_tabla_info_ruta, index=False)
                #Print
                print("Tabla eliminada")
            else:
                print("La sintaxis correcta es DROP TABLE IN nombre_db nombre_tabla")
        else:
            print("Error, comando no valido")
            return 0

    elif lista_comando[0] == "SELECT":
        it1 = lista_comando[1].find("(")
        it2 = lista_comando[1].find(")")
        datos_completos = True  # para saber si busca en todos los campos o solo en algunos
        header_in = []
        if it2 - it1 > 1:
            header_in = lista_comando[1][it1 + 1:it2]  # capturar las columnas a ingresar
            header_in = header_in.replace(" ","")
            header_in = header_in.split(",")
            datos_completos = False
        comando_aux1 = lista_comando[1][it2 + 1:]
        comando_aux1 = comando_aux1.split(maxsplit=4)
        if (comando_aux1[0] == "FROM"):
            nombre_db = comando_aux1[1]
            if (funciones.exist_db(nombre_db) == False):
                print("Error, no existe base de datos")
                return
            nombre_tabla = comando_aux1[2]
            if (funciones.exist_tb(nombre_db,nombre_tabla) == False):
                print("Error, no existe tabla")
                return
            if (datos_completos ==  False):
                for campo in header_in:
                    if (funciones.exist_campo(nombre_db,nombre_tabla,campo) == False):
                        print("Error, no existe ",campo)
                        return
            direccion_select = os.getcwd() + "/" + nombre_db + "/" + nombre_tabla + "/"
            header_tabla = manejador_csv.leer_csv(direccion_select, nombre_tabla, "header")  # Header de la tabla
            datos = pandas.read_csv(direccion_select + nombre_tabla + ".csv",index_col=False)
            if (len(comando_aux1) > 3): #hay WHERE
                if(comando_aux1[3]=="WHERE"):
                    #Solo valido 1 criterio
                    datos_where = []
                    comando_aux1[4] = comando_aux1[4].replace(" ", "")
                    if (comando_aux1[4].find("=") > 0):
                        datos_where = comando_aux1[4].split("=")
                        tipo_where = "="
                    elif (comando_aux1[4].find("<") > 0):
                        datos_where = comando_aux1[4].split("<")
                        tipo_where = "<"
                    elif (comando_aux1[4].find(">") > 0):
                        datos_where = comando_aux1[4].split(">")
                        tipo_where = ">"
                    else:
                        print("Error, comparacion no valida")
                        return
                    filtro_columna = datos_where[0]
                    filtro_criterio = datos_where[1]
                    if (funciones.exist_campo(nombre_db, nombre_tabla, filtro_columna) == False):
                        print("Error, no existe el campo")
                        return

                    if (filtro_columna=="id"):
                        filtro_criterio=int(filtro_criterio)
                    if (tipo_where == "="):
                        datos = datos[(datos[filtro_columna] == filtro_criterio)]
                    elif (tipo_where == "<"):
                        datos = datos[(datos[filtro_columna] < filtro_criterio)]
                    else:
                        datos = datos[(datos[filtro_columna] > filtro_criterio)]

                else:
                    print("Sintaxis invalida")
                    return
            if (datos_completos==False):
                #for columna in header_in:
                print(header_in)
                    #header_tabla.remove(columna)
                datos = datos.filter(items=header_in)


        else:
            print("Sintaxis invalida")
            return
        #datos.drop(datos.index, axis=1, inplace=True)
        #datos = datos.drop([''],axis=1)a
        #datos.set_index('id', inplace=True)

        #print (datos)

        print(tabulate(datos, headers=header_tabla, tablefmt='psql'))
        print("Datos mostrados")
        return

    elif lista_comando[0] == "INSERT":
        comando_aux = lista_comando[1]
        comando_aux = comando_aux.split(maxsplit=3)
        if (comando_aux[0] == "INTO"):
            nombre_db = comando_aux[1]
            #Comprobar si existe la base de datos
            if (funciones.exist_db(nombre_db) == False):
                print("Error, no existe base de datos")
                return
            nombre_tabla = comando_aux[2]
            #Comprobar si existe la tabla
            if (funciones.exist_tb(nombre_db,nombre_tabla) == False):
                print("Error, no existe base de datos")
                return
            direccion_insert = os.getcwd()+"/"+nombre_db+"/"+nombre_tabla+"/"
            #Capturar columnas a ingresar y datos
            it1 = comando_aux[3].find("(")
            it2 = comando_aux[3].find(")")
            datos_completos = True #para saber si insertera en todos los campos o solo en algunos
            header_in = []
            if it2-it1>1:
                header_in = comando_aux[3][it1+1:it2] #capturar las columnas a ingresar
                header_in = header_in.replace(" ","") #Quitando el espacio
                header_in = header_in.split(",")
                for campos in header_in:
                    if (funciones.exist_campo(nombre_db,nombre_tabla,campos) == False):
                        print ("No existe el campo,",campos)
                        return
                datos_completos = False

            comando_aux2 = comando_aux[3][it2+1:]
            comando_aux2 = comando_aux2.split(maxsplit=1)
            if comando_aux2[0]=="VALUES":
                it11 = comando_aux2[1].find("(")
                it22 = comando_aux2[1].find(")")
                data = comando_aux2[1][it11+1:it22] #capturo los datos a ingresar
                data = data.replace(" ","")
                data = data.split(",")
                for col,val in zip(header_in,data):
                    if (funciones.correct_type(nombre_db,nombre_tabla,col,val) == False):
                        print("Error, tipo de dato no valido",col,val)
                        return

            else:
                print("Error de sintaxis, falta VALUES")
                return

            #Comprobar con los campos de la tabla
            if datos_completos == False:
                header_tabla = manejador_csv.leer_csv(direccion_insert,nombre_tabla,"header") #Header de la tabla
                faltantes = [] #Guarda los indices de los campos que no se inserten
                newdata = []  #Reacomodar los datos en caso hayan sido ingresados en desorden
                for head in header_tabla:
                    if (head not in header_in) == True:
                        faltantes.append(header_tabla.index(head))
                for it in faltantes:
                    data.insert(it,"null")
            print(data)
            manejador_csv.escribir_csv(direccion_insert, nombre_tabla, data)
        elif comando_aux[0] == "BLOCK":
            nombre_db = comando_aux[1]
            nombre_tabla = comando_aux[2]
            file = comando_aux[3]
            print("JHe",file)
            data = manejador_csv.leer_csv(os.getcwd(),file)
            direccion_insert = os.getcwd()+"/"+nombre_db+"/"+nombre_tabla+"/"
            manejador_csv.escribir_csv(direccion_insert, nombre_tabla, data)
            print (nombre_db,nombre_tabla,file)
            print("pendiente, insertado por bloques")

        else:
            print("Error de sintexis, falta INTO")
            return
        print("Datos insertados")

    elif lista_comando[0] == "UPDATE":
        comando_aux = lista_comando[1].split(maxsplit=3)
        print(comando_aux)
        nombre_db = comando_aux[0]
        nombre_tabla = comando_aux[1]
        direccion_update = os.getcwd() + "/" + nombre_db + "/" + nombre_tabla + "/"
        header_tabla = manejador_csv.leer_csv(direccion_update, nombre_tabla, "header")  # Header de la tabla
        tam_header = len(header_tabla)
        if (comando_aux[2]=="SET"):
            it1 = comando_aux[3].find("(")
            it2 = comando_aux[3].find(")")
            columnas_in = []
            valores_in = []
            if it2 - it1 > 1:
                header_in = comando_aux[3][it1 + 1:it2]  # capturar las columnas a ingresar
                header_in = header_in.replace(" ","")
                header_in = header_in.split(",")
                for criterio in header_in:
                    aux = criterio.split("=")
                    if (funciones.correct_type(nombre_db,nombre_tabla,aux[0],aux[1]) == False):
                        print("Error, tipo incorrecto")
                        return
                    columnas_in.append(aux[0])
                    valores_in.append(aux[1])
            else:
                print("Error al asignar datos")
                return
            comando_aux1 = comando_aux[3][it2 + 1:]
            comando_aux1 = comando_aux1.split(maxsplit=1)
            tipo_where = ""
            if (comando_aux1[0]=="WHERE"):
                # Solo valido 1 criterio
                comando_aux1[1] = comando_aux1[1].replace(" ", "")
                if (comando_aux1[1].find("=")>0):
                    datos_where = comando_aux1[1].split("=")
                    tipo_where = "="
                elif (comando_aux1[1].find("<") > 0):
                    datos_where = comando_aux1[1].split("<")
                    tipo_where = ">"
                elif (comando_aux1[1].find(">")>0):
                    datos_where = comando_aux1[1].split(">")
                    tipo_where = ">"
                else:
                    print("Error, comparacion no valida")
                    return

                filtro_columna = datos_where[0]
                filtro_criterio = datos_where[1]
                if (funciones.exist_campo(nombre_db, nombre_tabla, filtro_columna) == False):
                    print("Error, no existe el campo",filtro_columna)
                    return
                df = pandas.read_csv(direccion_update+nombre_tabla+".csv")

                for column,valor in zip(columnas_in,valores_in):
                    if (funciones.correct_type(nombre_db,nombre_tabla,column,valor) == False):
                        print("La columna tiene diferente tipo que el valor",column,valor)
                        return
                    if (filtro_columna=="id"):
                        filtro_criterio=int(filtro_criterio)
                    if (tipo_where == "="):
                        print ("here",df.loc[(df[filtro_columna] == filtro_criterio)])
                        df.loc[(df[filtro_columna] == filtro_criterio), column] = valor
                    elif (tipo_where == "<"):
                        df.loc[(df[filtro_columna] < filtro_criterio), column] = valor
                    else:
                        df.loc[(df[filtro_columna] > filtro_criterio), column] = valor

                #print(df)
                df.to_csv(direccion_update+nombre_tabla+".csv", index=False)

            else:
                print("Falta WHERE, error de sintaxis")
                return


        else:
            print("Falta SET")
            return
        print("Actualizado")
        return

    elif lista_comando[0] == "DELETE":
        comando_aux = lista_comando[1].split(maxsplit=4)
        if (comando_aux[0]== "FROM"):
            nombre_db = comando_aux[1]
            if (funciones.exist_db(nombre_db) == False):
                print("Error, no existe base de datos")
                return
            nombre_tabla = comando_aux[2]
            if (funciones.exist_tb(nombre_db,nombre_tabla) == False):
                print("Error, no existe la tabla o ha sido eliminada")
                return
            direccion_delete = os.getcwd() + "/" + nombre_db + "/" + nombre_tabla + "/"
            if (comando_aux[3]== "WHERE"):
                comando_aux[4] = comando_aux[4].replace(" ","")
                datos_where = []
                tipo_where = ""
                if (comando_aux[4].find("=") > 0):
                    datos_where = comando_aux[4].split("=")
                    tipo_where = "="
                elif (comando_aux[4].find("<") > 0):
                    datos_where = comando_aux[4].split("<")
                    tipo_where = ">"
                elif (comando_aux[4].find(">") > 0):
                    datos_where = comando_aux[4].split(">")
                    tipo_where = ">"
                else:
                    print("Error, comparacion no valida")
                    return
                filtro_columna = datos_where[0]
                if (funciones.exist_campo(nombre_db,nombre_tabla,filtro_columna) == False):
                    print("Error, no existe el campo")
                    return
                filtro_criterio = datos_where[1]
                df = pandas.read_csv(direccion_delete + nombre_tabla + ".csv")
                if(funciones.correct_type(nombre_db,nombre_tabla,filtro_columna,filtro_criterio) == False):
                    print("No son el mismo tipo",filtro_criterio,filtro_columna)
                    return
                else:
                    filtro_criterio = funciones.toType(nombre_db,nombre_tabla,filtro_columna,filtro_criterio)
#                if (filtro_columna == "id"):
 #                   filtro_criterio = int(filtro_criterio)
                if (tipo_where == "="):
                    indices_to_delete = df.index[df[filtro_columna] == filtro_criterio].tolist()
                elif (tipo_where == "<"):
                    indices_to_delete = df.index[df[filtro_columna] < filtro_criterio].tolist()
                else:
                    indices_to_delete = df.index[df[filtro_columna] > filtro_criterio].tolist()

                df.drop(df.index[indices_to_delete],inplace=True)
                #df.drop(df.query(filtro_columna+"=="+'"'+filtro_criterio+'"').sample(frac=0.90).index)
                df.to_csv(direccion_delete + nombre_tabla + ".csv", index=False)
            else:
                print("Error, falta WHERE")
                return
        else:
            print("Error, falta WHERE")
            return
        print("Borrado")
        return

    else:
        print("Error, comando no valido")
        return 0


#Al iniciar se crea una archivo donde se almacene informacion de todas las bases
#de datos que se creen
if (path.exists("database_info.csv")==False):
    header_database_info = ["id","name_db","creacion","eliminacion"]
    manejador_csv.crear_archivo(os.getcwd(),"database_info",header_database_info)
#Preguntar comandos
comando = ""
while (comando != "exit"):
    comando = input("comando>>")
    start_time = time.time()
    lista_comando = comando.split(maxsplit=1)#comando.split(maxsplit=2)
   # print(lista_comando)
    procesar_comando(lista_comando)
    print("--- %s seconds ---" % (time.time() - start_time))

