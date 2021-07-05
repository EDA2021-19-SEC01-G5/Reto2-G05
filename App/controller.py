"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros


def initcatalog(tipo_lista):
    catalog = model.newCatalog(tipo_lista)
    return catalog


# Funciones para la carga de datos

def loadData(catalog):
    loadCategorias(catalog)
    loadVideos(catalog)


def loadVideos(catalog):
    direccion = cf.data_dir + "videos-large.csv"
    input_file = csv.DictReader(open(direccion,  encoding='utf-8'))
    for video in input_file:
        model.addVideo(catalog, video)


def loadCategorias(catalog):
    direccion = cf.data_dir + "category-id.csv"
    input_file = csv.DictReader(
        open(direccion,  encoding='utf-8'), delimiter="\t")
    for categoria in input_file:
        model.addCategoria(catalog, categoria)


# Funciones de ordenamiento


# Funciones de consulta sobre el catálogo
def requerimiento1(catalog,categoria,n):
    data = model.requerimiento1(
        catalog,categoria , n)
    return data 


def requerimiento2(catalog, country):
    datos = model.requerimiento2(catalog, country)
    return datos


def requerimiento3(catalog, category_name):
    datos = model.requerimiento3(catalog, category_name)
    return datos


def requerimiento4(catalog, country, tag, n):
    lista = model.requerimiento4(catalog, country, tag, n)
    return lista
