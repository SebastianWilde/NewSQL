import time
import numpy as np
import csv
import fileinput
import datetime
import time
#import sqlparse
import collections
import json
import ast
import pandas as pd
import sys
#import chilkat
from collections import OrderedDict
from tabulate import tabulate

M = 1000000
number_registers = 20*M # 100000 # 200000 # 20000 # 1000000 # 100000000
career = ["profesor","ingeniero","policia","abogado","medico","economista","politico","conserje","rector","asistente",
          "estudiante","tecnico","chofer","dentista","pintor","escultor","filosofo","psicologo","alcalde","cantante"]
max_size = 17

def creator_csv(pathfile, header):
    with open(pathfile, 'w') as csvfile: # only for create a .csv with header
            fieldnames = header
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

def fill_csv(pathfile, content, header):
    with open(pathfile, 'a') as csvfile:
            list_reader = header

            data_header = list_reader # we only extract the header -> first line
            writer = csv.DictWriter(csvfile, fieldnames=data_header) # indicate the order and Dictionary
            
            line_contain=OrderedDict() # create line_contain dictionary and order by default with OrderedDict

            for i in range(len(content)): # fill the dictionary with header values and fieldcontain values
                line_contain.__setitem__(data_header[i], content[i])
            writer.writerow(line_contain)

def main():
    start_time = time.time()

    header = ["ID_ALUMNO        ","NOMBRE           ","APELLIDO         ","EDAD             ","PROFESION        "]
    creator_csv('Alumno'+str(number_registers)+'.csv',header)
    
    for i in range(number_registers):
        id_inicio = str(i)
        largo_id = len(id_inicio)
        id = id_inicio + ' '*(max_size-largo_id)


        nombre = 'NOMBRE'+id_inicio
        largo_nombre = len(nombre)
        nombre = nombre + ' '*(max_size-largo_nombre)

        apellido = 'APELLIDO'+id_inicio
        largo_apellido = len(apellido)
        apellido = apellido + ' '*(max_size-largo_apellido)

        edad = np.random.randint(16, 25)
        largo_edad = len(str(edad))
        edad_string = str(edad) + ' '*(max_size-largo_edad)

        indice = np.random.randint(0, 20)
        profesion = str(career[indice])
        largo_profesion = len(str(profesion))
        profesion_string = (profesion + ' '*(max_size-largo_profesion)).upper()

        list_contain = []
        list_contain.append(id)
        list_contain.append(nombre)
        list_contain.append(apellido)
        list_contain.append(edad_string)
        list_contain.append(profesion_string)
        
        fill_csv('Alumno'+str(number_registers)+'.csv',list_contain, header)
        
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
