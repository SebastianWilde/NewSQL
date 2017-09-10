import csv, os


def crear_archivo(direccion, nombre, header):
    fichero = direccion + "/" + nombre + ".csv"
    # file = open(fichero, "wb")

    with open(fichero, 'w') as csvfile:
        #    fieldnames = ['first_name', 'last_name']
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        print("Escritura completa")
    return 1


def escribir_csv(direccion, nombre_archivo, datos):
    fichero = direccion + "/" + nombre_archivo + ".csv"
    with open(fichero, 'a') as f:  # el flag 'b' es requerido en ciertas plataformas
        writer = csv.writer(f)
        if (all(isinstance(elem, list) for elem in datos)) == True:
            writer.writerows(datos)
        else:
            writer.writerow(datos)

def leer_csv(direccion,nombre_archivo,tag=""):
    with open(direccion + "/" + nombre_archivo+ ".csv") as csvarchivo:
        entrada = csv.reader(csvarchivo)
        linea = [l for l in entrada]
    if (tag=="header"):
        return linea[0]
    elif (tag=="data"):
        return linea[1:]
    return linea
