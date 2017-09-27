import time
import numpy as np
import csv
import datetime
import time
from collections import OrderedDict

number_registers = 100  # 100000 # 200000 # 20000 # 1000000 # 100000000
career = ["profesor", "ingeniero", "policia", "abogado", "medico", "economista", "politico",
          "conserje", "rector","asistente","estudiante", "tecnico", "chofer", "dentista",
          "pintor", "escultor", "filosofo", "psicologo", "alcalde", "cantante"]
max_size = 17
datos = []

for i in range(number_registers):
    id_inicio = str(i)
    nombre = 'nombre' + id_inicio
    apellido = 'apellido' + id_inicio
    edad = str(np.random.randint(16, 25))
    indice = np.random.randint(0, 20)
    profesion = str(career[indice])
    lista = []
    lista.append(id_inicio)
    lista.append(nombre)
    lista.append(apellido)
    lista.append(edad)
    lista.append(profesion)
    datos.append(lista)

nombre_file = "lote" + str(number_registers)
with open(nombre_file+".csv", "w") as f:
  writer = csv.writer(f)
  writer.writerows(datos)

print("Escrito los datos")