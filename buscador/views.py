# indice_file_path = 'D:/documentos/7moSemestre/RecuperaciónInformación/3erParcial/SearcherDjango/proyecto/buscador/indx_invertido/index_invertido.txt'  # Actualiza la ruta
# en views.py
from django.shortcuts import render
import json
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
import time
import nltk
nltk.download('punkt')
nltk.download('snowball_data')

spanish_stemmer = SnowballStemmer('spanish')

def procesar_consulta(query):
    tokens = word_tokenize(query.lower())
    raices = [spanish_stemmer.stem(token) for token in tokens]
    return raices

def buscar_urls(raices, archivo_path):
    start_time = time.time()
    
    palabras_coincidentes = []
    with open(archivo_path, 'r', encoding='utf-8') as f:
        for linea in f:
            if linea.strip():  # Ignorar líneas vacías
                palabra = json.loads(linea)
                if any(spanish_stemmer.stem(palabra['Palabra']) == raiz for raiz in raices):
                    palabras_coincidentes.append(palabra)

    urls = []
    url_word_counts = {}
    
    for palabra in palabras_coincidentes:
        for url, word_count in palabra['Frecuencia de URL'].items():
            url_stem = url.strip('"')
            if url_stem in url_word_counts:
                url_word_counts[url_stem] += word_count
            else:
                url_word_counts[url_stem] = word_count
                urls.append(url_stem)

    # Calcular tiempo
    tiempo = time.time() - start_time

    resultados = {
        'urls': sorted(urls, key=lambda x: url_word_counts[x], reverse=True),
        'tiempo': tiempo,
        'url_word_counts': url_word_counts
    }

    return resultados

def buscar(request):
    if 'query' in request.GET:
        query = request.GET.get('query', '')
        raices = procesar_consulta(query)

        # Reemplazar con la ruta correcta
        archivo_path = 'D:/20209/Documentos/VisualStudioCode/elquebusca-main/buscador/IndiceInvertido2/Index2.txt'
        resultados = buscar_urls(raices, archivo_path)

        return render(request, 'buscador/resultados.html', {'query': query, 'num_resultados': len(resultados['urls']), 'resultados': resultados})
    
    return render(request, 'buscador/buscar.html')
