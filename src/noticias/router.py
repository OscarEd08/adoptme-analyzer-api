from fastapi import APIRouter
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

router = APIRouter()

@router.get("/noticias_completas/")
def noticias_completas():

    url = "https://elcomercio.pe/noticias/mascotas/"
    # Enviar una solicitud GET a la URL
    response = requests.get(url)

    # consistencias que el servidor nos responda con un código 200
    if response.status_code != 200:
        return { 'message': 'Error al obtener las noticias' }
    else:
        
        # Crear un objeto BeautifulSoup y parsear el contenido HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        
        lista_fechas_horas = []
        fechas = soup.find_all('span', class_="story-item__date-time")
        for fecha in fechas:
            lista_fechas_horas.append(fecha.text)
        
        # Inicializar las listas de fechas y horas
        lista_fechas = []
        lista_horas = []

        # Recorrer la lista y separar en fechas (pares) y horas (impares)
        for i in range(len(lista_fechas_horas)):
            if i % 2 == 0:  # Elementos en posición par (índice 0, 2, 4, ...)
                lista_fechas.append(lista_fechas_horas[i])
            else:  # Elementos en posición impar (índice 1, 3, 5, ...)
                lista_horas.append(lista_fechas_horas[i])

        lista_fechas = lista_fechas
        lista_horas = lista_horas

        lista_titulos = []        
        titulos = soup.find_all('a', class_="story-item__title block overflow-hidden primary-font line-h-xs mt-10")
        for titulo in titulos:
            lista_titulos.append(titulo.text)

        lista_titulos = lista_titulos

        links = []
        for titulo in titulos:
            href = titulo.get('href')  # Obtener el valor del atributo 'href'
            if href:  # Verificar que no sea None
                link = 'https://elcomercio.pe' + href
                links.append(link)
        links = links


        imagenes = soup.find_all('img', class_="lazy story-item__img object-cover object-center w-full h-full")
        # Crear una lista para almacenar los enlaces
        enlaces_imagenes = []
        # Iterar sobre las imágenes y extraer el atributo 'data-src' o 'src'
        for img in imagenes:
            data_src = img.get('data-src')  # Intentar obtener el 'data-src'
            src = img.get('src')  # Intentar obtener el 'src'
            if data_src:  # Si 'data-src' existe, agregarlo a la lista
                enlaces_imagenes.append(data_src)
            elif src:  # Si 'src' existe, usarlo como respaldo
                enlaces_imagenes.append(src)
        enlaces_imagenes = enlaces_imagenes
        '''
                

        
        noticias_mascotas = []
        '''

        '''
        for fecha, hora, titulo, imagen, link in zip(lista_fechas, lista_horas, titulos, enlaces_imagenes, links):
            noticias_mascotas.append({
                "fecha": fecha,
                "hora": hora,
                "titulo": titulo,
                "imagen": imagen,
                "link": link,
            })
        '''

        noticias = []

        for i in range(len(lista_fechas)):
            noticia = {
                'id': str(i),  # Asignar un ID único basado en el índice (comenzando desde 1)
                'fecha': lista_fechas[i],
                'hora': lista_horas[i],
                'titulo': lista_titulos[i],
                'link': links[i],
                'imagen': enlaces_imagenes[i]
            }
            noticias.append(noticia)
        noticias = noticias
        
        # Retornar la lista de noticias como JSON
        '''
        return { 'fechas' : lista_fechas[0:5], 
                'horas' : lista_horas[0:5],
                'links' : links[0:5],
                'imagenes' : enlaces_imagenes[0:5],
                'titulos' : lista_titulos[0:5]}
        '''

        resultado = { 'noticias' : noticias }

        return resultado


@router.get("/noticias_facebook/")
def noticias_facebook():
    
    # leer el rarchivo Noticias_Adopme.csv
    # noticias = pd.read_csv('Noticias_Adopme.csv', sep=',')
    noticias_path = os.path.join(os.path.dirname(__file__), "Noticias_Adoptme.xlsx")

    # leer el excel con pandas 
    noticias_df = pd.read_excel(noticias_path)

    # Reemplazar los valores NaN con None o un valor predeterminado
    noticias_df = noticias_df.applymap(lambda x: None if pd.isna(x) else x)

    # O si prefieres otro valor, como una cadena vacía o 0:
    # noticias_df = noticias_df.fillna("")  # O
    # noticias_df = noticias_df.fillna(0)

    # Convertir el DataFrame a una lista de diccionarios
    lista_noticias = noticias_df.to_dict(orient='records')

    dict_noticias = { 'noticias' : lista_noticias }

    # Retornar la lista de noticias
    return dict_noticias