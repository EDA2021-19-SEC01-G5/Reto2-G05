﻿
"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

#from App.controller import initcatalog
import gc
from tabulate import tabulate
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("Bienvenido")
    print("1- Inicializar Catálogo")
    print("2- Cargar información en el catálogo")
    print("3- Consultar los n videos con más views en una categoria especifica")
    print("4- Realizar pruebas de rendimiento (tiempo y espacio)")
    print("0- Salir")


def initCatalog(tipo_lista,map_type_cat="PROBING", load_factor_cat = 0.5):
    return controller.initcatalog(tipo_lista, map_type_cat, load_factor_cat)


def loadData(catalog):
    return controller.loadData(catalog)


def printCategorias(catalog):
    print("Información sobre las categorias: \n")
    cantidad_categorias = lt.size(catalog["categorias"])
    for i in range(1, cantidad_categorias+1):
        print(lt.getElement(catalog["categorias"], i))


def printPrimervideo(catalog):
    elemento = lt.firstElement(catalog["videos"])
    print("\n Datos del primer video cargado: \n")
    print("Titulo : ", elemento["title"])
    print("Nombre del canal : ", elemento["channel_title"])
    print("Fecha de trending : ", elemento["trending_date"])
    print("Pais : ", elemento["country"])
    print("Likes : ", elemento["likes"])
    print("Dislikes : ", elemento["dislikes"], "\n")
    print(elemento.keys())


def requerimiento1(catalog, categoria, n):
    data = controller.requerimiento1(
        catalog,categoria , n )
    longitud = lt.size(data[0])
    if longitud < n:
        print("La cantidad de videos pedidos excede la cantidad posible. \n A continuación de muestran dos los libros de la categoria deseada y el pais deseado, organizados según la cantidad de likes")
    header = ["", "trending date", "titulo", "nombre del canal",
              "fecha publicacion", "vistas", "likes", "dislikes"]
    mostrar = []
    for i in range(1, longitud + 1):
        elemento = lt.getElement(data[0], i)
        mostrar.append([i, elemento["trending_date"], elemento["title"], elemento["channel_title"],
                       elemento["publish_time"], elemento["views"], elemento["likes"], elemento["dislikes"]])
    print(tabulate(mostrar, headers = header))
    print("Tiempo [ms]: ", f"{data[1]:.3f}", "  ||  ",
            "Memoria [kB]: ", f"{data[2]:.3f}")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        tipo_lista = input(
            "Ingrese el tipo de lista con el que desea cargar la lista de videos. \n0 para ARRAY_LIST o 1 para SINGLE_LINKED: ")
        print("Cargando información de los archivos ....")
        catalog = initCatalog(tipo_lista)
        if catalog:
            print("Catalogo inicializado")
        else:
            print(
                "\nNo ingreso una opcion de tipo de dato valida, por favor intente de nuevo.\n")
    elif int(inputs[0]) == 2:
        answer = loadData(catalog)
        print("información cargada \n")
        print("Total de registros de videos cargados : ",
                  lt.size(catalog["videos"]), "\n")
        printPrimervideo(catalog)
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")


    elif int(inputs[0]) == 3:
        n = int(input(
                "Ingrese el número de videos que desea consultar: "))
        categoria = input("Ingrese la categoria que quiere consultar: ") 
        requerimiento1(catalog, categoria.lower().strip(),n)
        
    elif int(inputs[0]) == 4:
        trials = {"PROBING":[0.30,0.50,0.80], "CHAINING":[2.00,4.00,6.00]}
        f = open("resultados_cambio5.csv","w")
        f.write("tipo, loadfactor, tiempo, espacio\n")
        for type in trials.keys():
            for i in range(3):
                test_catalog = initCatalog(0, type, trials[type][i])
                test_answer =  loadData(test_catalog)
                f.write(type + "," + str(trials[type][i]) + "," + str(test_answer[0]) + "," + str(test_answer[1])+ "\n")
        f.close()
    else:
        sys.exit(0)
sys.exit(0)
