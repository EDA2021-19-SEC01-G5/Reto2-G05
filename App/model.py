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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import time
from DISClib.DataStructures.arraylist import addLast, getElement, newList
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort
from DISClib.Algorithms.Sorting import insertionsort
from DISClib.Algorithms.Sorting import selectionsort
from DISClib.Algorithms.Sorting import mergesort, quicksort
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

# Funciones para agregar informacion al catalogo


def newCatalog(tipo_lista, map_type_cat="PROBING", load_factor_cat = 0.5):
    """
    Crea el catalogo con la información de videos y de categorias
    """
    if int(tipo_lista) == 0:
        ED = "ARRAY_LIST"
    elif int(tipo_lista) == 1:
        ED = "SINGLE_LINKED"
    else:
        return None
    catalog = {"videos": None, "categorias": None}
    catalog["videos"] = lt.newList(ED)
    """
    """
    catalog["videoIds"] = mp.newMap(10000, maptype= 'PROBING', loadfactor = 0.5, comparefunction = compareCategorias)


    """
    """
    catalog["categorias"] = mp.newMap(100, maptype = map_type_cat, loadfactor = load_factor_cat , comparefunction = compareCategorias)


    """
    """
    catalog["categorias_id"] = mp.newMap(100, maptype = 'PROBING', loadfactor = 0.5, comparefunction = compareCategorias)


    return catalog

def newCategoria(name, id):
    category = {'name':'',
        'category_id': '',
        'total_categorias': 0,
        'videos': None,
        }
    category['name'] = name
    category['category_id'] = id
    category['videos'] = lt.newList()
    return category


def addCategoria(catalog, categoria):
    name = categoria['name'].strip().lower()
    id = categoria['id'].strip()
    new_category = newCategoria(name, id)
    mp.put(catalog['categorias'], name ,new_category)
    mp.put(catalog['categorias_id'], id ,new_category)

def category_id_name(catalog, category_id):
    '''
    Recibe como parámetro el nombre de una
    categoria y retorna el id correspondiente
    '''
    id = None
    catalog = catalog['categorias']
    length = lt.size(catalog)
    i = 1
    while i <= length:
        element = lt.getElement(catalog, i)
        id1 = str(category_id)
        id2 = str(element['id'])
        if id1 == id2:
            id = element['name']
            break
        i += 1

    return id


def addVideo(catalog, video):
    """
    Adiciona la información de un video al catalogo
    """
    lt.addLast(catalog["videos"], video)
    mp.put(catalog["videoIds"],video['video_id'], video)
    addVideoCategoria(catalog, video)
    


def addVideoCategoria(catalog, categoria):
    """
    adiciona a informacion de una categoria
    """
    videoid = categoria['video_id'] 
    categoryid = categoria['category_id'].strip()
    entry = mp.get(catalog['categorias_id'], categoryid)
    if entry:
        cat_video = mp.get(catalog['categorias'],me.getValue(entry)['name'])
        cat_video['value']['total_categorias'] += 1
        video = mp.get(catalog['videoIds'],videoid)
        if video: 
            lt.addLast(cat_video['value']['videos'],video['value'])

# Requerimiento 1

def requerimiento1(catalog,category_name, n):
    '''
    Retorna los n videos con más likes en un país y 
    categoria determinados
    '''
    lista = getVideosByCategory(catalog, category_name) 
    organizada = mergesort.sort(lista, cmpByViews)
    lista_final = lt.newList()
    for j in range(1, n+1):
        if j <= lt.size(organizada):
            lt.addLast(lista_final, lt.getElement(organizada, j))
        else:
            pass
    return lista_final

def getVideosByCategory(catalog, category_name):
    categories = catalog["categorias"]
    entry = mp.get(categories,category_name.strip())
    return entry['value']['videos']


def cmpByViews(elemento1, elemento2):
    '''
    Función de comparación de views utilizada
    para ordenar de manera descendente
    la lista ingresada.
    '''
    if int(elemento1["views"]) > int(elemento2["views"]):
        return True
    else:
        return False



# requerimiento 2

def comparaciónTitulo(elemento1, elemento2):
    '''
    Función de comparación de título utilizada
    para ordenar por titulo la lista de videos ingresada.
    '''
    nombre1 = elemento1["title"]
    nombre2 = elemento2["title"]
    if nombre1 < nombre2:
        return True
    else:
        return False


def dividirPais(catalog, pais):
    '''
    Retorna una nueva lista filtrando
    acorde al país ingresado por parámetro
    '''
    lista = lt.newList("ARRAY_LIST")
    longitud = lt.size(catalog["videos"])
    for i in range(1, longitud+1):
        video = lt.getElement(catalog["videos"], i)
        if video["country"] == pais:
            lt.addLast(lista, video)
    return lista


def agregarTrending(lista_videos):
    '''
    Retorna una lista de videos agregando
    el número de días que fue trending.
    '''
    videos = mergesort.sort(lista_videos, comparaciónTitulo)
    nueva_lista = lt.newList("ARRAY_LIST")
    cant_videos = lt.size(videos)
    iguales = 1
    inicial = 2
    actual = lt.getElement(videos, 1)
    while inicial <= cant_videos:
        nuevo = lt.getElement(videos, inicial)
        if nuevo["title"] == actual["title"]:
            iguales += 1
            inicial += 1
        else:
            elemento = nuevo
            elemento["dias_trending"] = iguales
            lt.addLast(nueva_lista, elemento)
            iguales = 1
            inicial += 1
            actual = nuevo
    elemento = nuevo
    elemento["dias_trending"] = iguales
    lt.addLast(nueva_lista, elemento)
    return nueva_lista


def obtenerRatio(elemento):
    '''
    Retorna el ratio likes/dislikes del
    video ingresado por parámetro
    '''
    likes = int(elemento["likes"])
    dislikes = int(elemento["dislikes"])
    if dislikes > 0:
        ratio = likes/dislikes
    else:
        ratio = likes
    return ratio


def comparacionDiasRatioPais(elemento1, elemento2):
    '''
    Función de comparación para organizar los videos
    según los dias trending y el ratio likes/dislikes
    que poseen.
    '''
    dias1 = elemento1["dias_trending"]
    dias2 = elemento2["dias_trending"]
    ratio1 = obtenerRatio(elemento1)
    ratio2 = obtenerRatio(elemento2)
    if ratio1 > 10 and ratio2 <= 10:
        return True
    elif ratio1 <= 10 and ratio2 > 10:
        return False
    else:
        if dias1 > dias2:
            return True
        else:
            return False


def requerimiento2(catalog, country):
    '''
    Retorna una lista que contiene los datos del video
    con más dias trending, cuya relación likes/dislikes es positiva
    y acorde a un país determinado.
    '''
    lista_pais = dividirPais(catalog, country)
    lista_por_titulo = agregarTrending(lista_pais)
    nueva_lista = mergesort.sort(lista_por_titulo, comparacionDiasRatioPais)
    elemento = lt.getElement(nueva_lista, 1)
    ratio = str(obtenerRatio(elemento))
    dias = elemento["dias_trending"]
    datos = lt.newList("ARRAY_LIST")
    lt.addLast(datos, elemento["title"])
    lt.addLast(datos, elemento["channel_title"])
    lt.addLast(datos, elemento["country"])
    lt.addLast(datos, ratio)
    lt.addLast(datos, dias)
    return datos


# Requerimiento 3:

def requerimiento3(catalog, category_name):
    '''
    Retorna una tupla con la información del video
    con más dias trending, cuya relación likes/dislikes es positiva
    y acorde a una categoria determinada.
    '''
    id = category_name_id(catalog, category_name)
    filtered_list = filter_by_category_ratio(catalog, id)
    trending_list = agregarTrending(filtered_list)
    ordered_trending = mergesort.sort(trending_list, cmp_by_trending)
    top_video = lt.getElement(ordered_trending, lt.size(ordered_trending))
    data = (top_video['title'], top_video['channel_title'],
            id, obtenerRatio(top_video), top_video['dias_trending'])
    return data


def category_name_id(catalog, category_name):
    '''
    Recibe como parámetro el nombre de una
    categoria y retorna el id correspondiente
    '''
    id = None
    catalog = catalog['categorias']
    length = lt.size(catalog)
    i = 1
    while i <= length:
        element = lt.getElement(catalog, i)
        name1 = category_name.lower().strip()
        name2 = element['name'].lower().strip()
        if name1 in name2:
            id = element['id']
            break
        i += 1

    return id


def filter_by_category_ratio(catalog, category_id):
    '''
    Retorna una nueva lista con los videos que
    pertenecen a la categoria cuyo id es ingresado por parámetro
    y cuyo ratio likes/dislikes es altamente positivo.
    '''
    new_list = lt.newList('ARRAY_LIST')
    catalog = catalog['videos']
    length = lt.size(catalog)
    i = 1
    while i <= length:
        element = lt.getElement(catalog, i)
        ratio = obtenerRatio(element)
        if element['category_id'] == category_id and ratio > 20:
            lt.addLast(new_list, element)
        i += 1

    return new_list


def cmp_by_trending(element1, element2):
    '''
    Función de comparación para ordenar
    la lista acorde al número de días que el video
    ha sido trending
    '''
    compare = None
    trending1 = element1['dias_trending']
    trending2 = element2['dias_trending']
    if trending2 == trending1:
        compare = False
    elif trending2 < trending1:
        compare = False
    else:
        compare = True

    return compare


# requerimiento 4
def separarPaisTags(catalog, country, tag):
    '''
    Retorna una nueva lista que incluye
    únicamente los videos que cumplan con el filtro de 
    país y tag especificados por parámetro
    '''
    videos = catalog["videos"]
    longitud_videos = lt.size(videos)
    nueva_lista = lt.newList("ARRAY_LIST")
    for i in range(1, longitud_videos+1):
        video = lt.getElement(videos, i)
        if tag in video["tags"] and country == video["country"]:
            lt.addLast(nueva_lista, video)
    return nueva_lista


def comparacionComentarios(elemento1, elemento2):
    '''
    Función de comparación para ordenar
    de mayor a menor los videos acorde al número
    de comentarios
    '''
    comentarios1 = int(elemento1["comment_count"])
    comentarios2 = int(elemento2["comment_count"])
    if comentarios1 > comentarios2:
        return True
    else:
        return False


def eliminarRepetidos(videos):
    '''
    Retorna una nueva lista sin videos
    repetidos
    '''
    longitud = lt.size(videos)
    video1 = lt.firstElement(videos)
    lista = lt.newList("ARRAY_LIST")
    for i in range(2, longitud + 1):
        video2 = lt.getElement(videos, i)
        if video1["title"] != video2["title"]:
            lt.addLast(lista, video1)
            video1 = video2
    return lista


def requerimiento4(catalog, country, tag, n):
    '''
    Retorna una lista con los n videos con más comentarios según el país
    y el tag especificados por parámetro.
    '''
    lista_modificada = separarPaisTags(catalog, country, tag)
    organizada = mergesort.sort(lista_modificada, comparacionComentarios)
    organizada = eliminarRepetidos(organizada)
    entregar = lt.newList("ARRAY_LIST")
    i = 1
    while i <= n:
        if lt.size(organizada) >= i:
            lt.addLast(entregar, lt.getElement(organizada, i))
            i += 1
        else:
            i = n+1
    return entregar


#Funciones de comparación

def compareCategorias(categoria, entry):
    cat_entry = me.getKey(entry)
    if (categoria.lower().strip() == cat_entry.strip().lower()):
        return 0
    


def cmpTagId(id1, id2):
    pass

def compareMapBookIds(id1, id2):
    pass



