import os #para usar las funciones del sistema operativo
import os.path as path
import shutil #para eliminar

import manejador_csv #para crear archivos csv para almancenar los datos

import datetime #para manejar fechas

import pandas #para sobreescribir csv

import time #medir el tiempo

from tabulate import tabulate

def procesar_comando(lista_comando):
    if lista_comando[0] == "CREATE":
        ruta = os.getcwd() + "/" #obteniendo la ruta actual
        comando_aux = lista_comando[1]
        comando_aux = comando_aux.split(maxsplit=1)
        if comando_aux[0] == "DATABASE":
            #Crea una carpeta para la base de datos que se crea
            nombre_db = comando_aux[1]
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
            comando_aux2 = comando_aux[1]
            comando_aux2 = comando_aux2.split(maxsplit=3)
            if (comando_aux2[0]== "IN"):
                #Crea una carpeta para la tabla
                nombre_db = comando_aux2[1]
                nombre_tabla = comando_aux2[2]
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
                        tam_campo = "4"
                    header_metadata.append(nombre_campo)
                    dato = [1,nombre_campo,tipo_campo,tam_campo]
                    datos.append(dato)

                manejador_csv.crear_archivo(direccion,nombre_tabla,header_metadata)
                manejador_csv.escribir_csv(direccion,nombre_tabla+"_info",datos)
                print("Tabla creada")
            else:
                print("Para crear tablas: CREATE TABLE IN nombre_db nombre_tabla")
        else:
            print("Error, comando no valido")
            return 0

    elif lista_comando[0] == "DROP":
        comando_aux = lista_comando[1]
        comando_aux = comando_aux.split(maxsplit=1)
        if comando_aux[0] == "DATABASE":
            nombre_db = comando_aux[1]
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
                nombre_tabla = comando_aux2[2]
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
        if it2 - it1 > 1:
            header_in = lista_comando[1][it1 + 1:it2]  # capturar las columnas a ingresar
            header_in = header_in.split(",")
            datos_completos = False
        comando_aux1 = lista_comando[1][it2 + 1:]
        comando_aux1 = comando_aux1.split(maxsplit=4)
        if (comando_aux1[0] == "FROM"):
            nombre_db = comando_aux1[1]
            nombre_tabla = comando_aux1[2]
            direccion_select = os.getcwd() + "/" + nombre_db + "/" + nombre_tabla + "/"
            header_tabla = manejador_csv.leer_csv(direccion_select, nombre_tabla, "header")  # Header de la tabla
            datos = pandas.read_csv(direccion_select + nombre_tabla + ".csv",index_col=False)
            if (len(comando_aux1) > 3): #hay WHERE
                if(comando_aux1[3]=="WHERE"):
                    #Solo valido 1 criterio
                    datos_where = comando_aux1[4].split("=")
                    filtro_columna = datos_where[0]
                    filtro_criterio = datos_where[1]
                    datos = datos [(datos[filtro_columna] == filtro_criterio)]
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
        print (datos)
        print(tabulate(datos, headers=header_tabla, tablefmt='psql'))
        print("Datos mostrados")
        return

    elif lista_comando[0] == "INSERT":
        comando_aux = lista_comando[1]
        comando_aux = comando_aux.split(maxsplit=3)
        if (comando_aux[0] == "INTO"):
            nombre_db = comando_aux[1]
            nombre_tabla = comando_aux[2]
            direccion_insert = os.getcwd()+"/"+nombre_db+"/"+nombre_tabla+"/"
            #Capturar columnas a ingresar y datos
            it1 = comando_aux[3].find("(")
            it2 = comando_aux[3].find(")")
            datos_completos = True #para saber si insertera en todos los campos o solo en algunos
            if it2-it1>1:
                header_in = comando_aux[3][it1+1:it2] #capturar las columnas a ingresar
                datos_completos = False

            comando_aux2 = comando_aux[3][it2+1:]
            comando_aux2 = comando_aux2.split(maxsplit=1)
            if comando_aux2[0]=="VALUES":
                it11 = comando_aux2[1].find("(")
                it22 = comando_aux2[1].find(")")
                data = comando_aux2[1][it11+1:it22] #capturo los datos a ingresar
                data = data.split(",")
            else:
                print("Error de sintaxis, falta VALUES")
                return

            #Comprobar con los campos de la tabla
            if datos_completos == False:
                header_tabla = manejador_csv.leer_csv(direccion_insert,nombre_tabla,"header") #Header de la tabla
                faltantes = []
                for head in header_tabla:
                    if header_in.find(head)<0:
                        faltantes.append(header_tabla.index(head))
                for it in faltantes:
                    data.insert(it,"null")
            print(data)
            manejador_csv.escribir_csv(direccion_insert, nombre_tabla, data)
        elif comando_aux[0] == "BLOCK":
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
                header_in = header_in.split(",")
                for criterio in header_in:
                    aux = criterio.split("=")
                    columnas_in.append(aux[0])
                    valores_in.append(aux[1])
            else:
                print("Error al asignar datos")
                return
            comando_aux1 = comando_aux[3][it2 + 1:]
            comando_aux1 = comando_aux1.split(maxsplit=1)
            if (comando_aux1[0]=="WHERE"):
                # Solo valido 1 criterio
                datos_where = comando_aux1[1].split("=")
                filtro_columna = datos_where[0]
                filtro_criterio = datos_where[1]

                df = pandas.read_csv(direccion_update+nombre_tabla+".csv")

                for column,valor in zip(columnas_in,valores_in):
                    if (filtro_columna=="id"):
                        filtro_criterio=int(filtro_criterio)
                    df.loc[(df[filtro_columna] == filtro_criterio), column] = valor

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
            nombre_tabla = comando_aux[2]
            direccion_delete = os.getcwd() + "/" + nombre_db + "/" + nombre_tabla + "/"
            if (comando_aux[3]== "WHERE"):
                datos_where = comando_aux[4].split("=")
                filtro_columna = datos_where[0]
                filtro_criterio = datos_where[1]
                df = pandas.read_csv(direccion_delete + nombre_tabla + ".csv")
                indices_to_delete = df.index[df[filtro_columna]==filtro_criterio].tolist()
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

