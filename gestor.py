import os #para usar las funciones del sistema operativo

import shutil #para eliminar

import manejador_csv #para crear archivos csv para almancenar los datos

import datetime #para manejar fechas

import pandas #para sobreescribir csv

import time #medir el tiempo

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
        print("Buscando")

    elif lista_comando[0] == "INSERT":
        comando_aux = lista_comando[1]
        comando_aux = comando_aux.split(maxsplit=3)
        if comando_aux[0] == "INTO":
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
        else:
            print("Error de sintexis, falta INTO")
            return
        print("Datos insertados")

    elif lista_comando[0] == "UPDATE":
        print("Actualizando")

    elif lista_comando[0] == "DELETE" and lista_comando[1] == "FROM":
        print("Borrando")

    else:
        print("Error, comando no valido")
        return 0


#Al iniciar se crea una archivo donde se almacene informacion de todas las bases
#de datos que se creen
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

