# app.py
from flask import Flask, render_template, render_template_string
import markdown
import os
import glob # Necesitamos glob para encontrar archivos que terminen en .md

app = Flask(__name__)
# Asegúrate de que el directorio 'markdown' exista
MARKDOWN_DIR = 'markdown'
if not os.path.exists(MARKDOWN_DIR):
    os.makedirs(MARKDOWN_DIR)

@app.route('/')
def inicio():
    # 1. Obtener la lista de rutas completas de todos los archivos .md
    rutas_archivos = glob.glob(os.path.join(MARKDOWN_DIR, '*.md'))
    
    # 2. Crear una lista de diccionarios, incluyendo la fecha de modificación
    # os.path.getmtime(ruta) devuelve la fecha de modificación (timestamp numérico)
    posts_con_fechas = []
    for ruta in rutas_archivos:
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido_md = f.read()
        
        # Convertimos el MD a HTML aquí mismo para simplificar la plantilla
        contenido_html = markdown.markdown(contenido_md)
        
        posts_con_fechas.append({
            'fecha_modificacion': os.path.getmtime(ruta),
            'contenido_html': contenido_html,
            'nombre_archivo': os.path.basename(ruta).replace('.md', '')
        })

    # 3. Ordenar la lista por 'fecha_modificacion' de forma descendente (más reciente primero)
    # reverse=True hace que sea de mayor a menor (más nuevo a más antiguo)
    posts_ordenados = sorted(posts_con_fechas, key=lambda post: post['fecha_modificacion'], reverse=True)
    
    # 4. Pasar la lista ordenada a la plantilla
    return render_template('index.html', posts=posts_ordenados)

# ... (El resto de tus rutas: contacto, proyectos, mostrar_post) ...
@app.route('/contacto')
def contacto():
    # ...
    return render_template('contacto.html')

@app.route('/proyectos')
def proyectos():
    # ...
    return render_template('proyectos.html')

@app.route('/post/<nombre>')
def mostrar_post(nombre):
    # Esta ruta ya estaba bien para mostrar posts individuales
    ruta_md = os.path.join('markdown', f'{nombre}.md')
    # ... (resto de la lógica de mostrar_post) ...
    if not os.path.exists(ruta_md):
        return "Post no encontrado", 404
    with open(ruta_md, 'r', encoding='utf-8') as f:
        contenido_md = f.read()
    contenido_html = markdown.markdown(contenido_md)
    return render_template_string("""
        <html>
        <head>
            <title>{{ nombre }}</title>
            <style>
                body {
                    background-color: #ffffff;
                    color: #1f2937;
                    font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
                    line-height: 1.6;
                    max-width: 700px;
                    margin: 0 auto;
                    padding: 2rem 1rem;
                }
                a { color: #2563eb; text-decoration: none; font-weight: 500; }
                a:hover { text-decoration: underline; color: #1d4ed8; }
                h1, h2, h3, h4, h5, h6 { color: #111827; margin-top: 2em; margin-bottom: 0.75em; font-weight: 700; line-height: 1.2; }
                h1 { font-size: 2.25rem; margin-top: 0.5em; }
                hr { border: 0; border-top: 1px solid #e5e7eb; margin: 3rem 0; }
                img { max-width: 100%; height: auto; border-radius: 0.5rem; }
                pre { background: #1f2937; color: #f9fafb; padding: 1.25rem; border-radius: 0.5rem; overflow-x: auto; }
                code { background: #f3f4f6; padding: 0.2em 0.4em; border-radius: 0.25rem; font-family: monospace; font-size: 0.9em; }
                pre code { background: transparent; padding: 0; color: inherit; }
                blockquote { border-left: 4px solid #e5e7eb; padding-left: 1rem; color: #4b5563; font-style: italic; }
            </style>
        </head>
        <body>
            {{ contenido|safe }}
        </body>
        </html>
    """, contenido=contenido_html, nombre=nombre)

if __name__ == '__main__':
    app.run(debug=True)
