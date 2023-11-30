import ast
from collections import defaultdict
from multiprocessing import Pool
import json

# Lista de palabras comunes (stop words)
stop_words = ["a", "the", "and", "in", "of", "to", "for", "on", "with"]

def main():
    with open('url.txt', 'r', encoding='utf-8') as urls_file:
        urls = urls_file.read().splitlines()

    inverted_index = {}

    # Paraleliza el procesamiento de las URL
    with Pool() as pool:
        results = pool.map(process_url, urls)

    # Combina los resultados de los procesos paralelos
    for result in results:
        for word, (url, frequency) in result:
            # Verifica que la palabra sea alfabética y no esté en la lista de stop words antes de procesarla
            if word.isalpha() and word.lower() not in stop_words:
                if word in inverted_index:
                    inverted_index[word]["Frecuencia de URL"][url] = frequency
                else:
                    inverted_index[word] = {"Palabra": word, "Frecuencia de URL": {url: frequency}}

    with open('index2.txt', 'w', encoding='utf-8') as index_file:
        for word, data in inverted_index.items():
            index_file.write(json.dumps(data, indent=2) + '\n')

    print("Índice invertido guardado en 'index2.txt'")

def process_url(url):
    # Obtén la URL y el contenido asociado
    url, data = url.split(': ')
    # Evalúa la cadena para convertirla en una lista de Python
    data = ast.literal_eval(data)

    word_data = []

    for word, frequency in data:
        word_data.append((word, (url, frequency)))

    return word_data

if __name__ == "__main__":
    main()
