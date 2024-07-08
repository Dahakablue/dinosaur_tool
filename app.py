from flask import Flask, render_template, request, send_file
import requests
import os

app = Flask(__name__)

# Lista de dinosaurios famosos (puedes agregar más según sea necesario)
dinosaurios_famosos = {
    'Velociraptor': 'https://es.wikipedia.org/wiki/Velociraptor',
    'Stegosaurus': 'https://es.wikipedia.org/wiki/Stegosaurus'
}

# Ruta principal que muestra la interfaz web
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre_dinosaurio = request.form['dinosaurio']
        url_wikipedia = dinosaurios_famosos.get(nombre_dinosaurio)
        
        if url_wikipedia:
            # Obtener la página de Wikipedia del dinosaurio
            response = requests.get(url_wikipedia)
            if response.status_code == 200:
                # Descargar la imagen del infobox
                imagen_url = obtener_imagen_infobox(response.text)
                if imagen_url:
                    guardar_imagen(imagen_url, nombre_dinosaurio)
                    return f'¡Información y imagen de {nombre_dinosaurio} descargadas!'
                else:
                    return 'No se pudo encontrar una imagen para este dinosaurio.'
            else:
                return 'No se pudo obtener la página de Wikipedia.'
        else:
            return 'Dinosaurio no encontrado en la lista.'

    return render_template('index.html', dinosaurios=list(dinosaurios_famosos.keys()))

def obtener_imagen_infobox(html):
    # Aquí implementarías la lógica para parsear el HTML y obtener la URL de la imagen del infobox
    # Como ejemplo básico, buscamos una imagen con un patrón fijo
    # Implementación real puede requerir usar BeautifulSoup u otra librería para parsear HTML
    # Este es un ejemplo simplificado
    inicio = html.find('<td colspan="2" style="text-align:center;">')
    if inicio == -1:
        return None
    inicio = html.find('src="', inicio) + 5
    fin = html.find('"', inicio)
    return html[inicio:fin]

def guardar_imagen(url, nombre_dinosaurio):
    # Descarga y guarda la imagen en la carpeta 'static/images'
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(f'static/images/{nombre_dinosaurio}.jpg', 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

if __name__ == '__main__':
    app.run(debug=True)
