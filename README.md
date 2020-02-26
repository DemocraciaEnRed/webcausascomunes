# webcausascomunes

Para correrlo primero hay que crear el entorno de python:
- ubicarse en la carpeta del proyecto
- crear el virtual environment `python3 -m venv venv`
- activarlo `source venv/bin/activate`
- instalar dependencias `pip install -r requirements.txt`

Ya que el programa depende del contenido de Directus, debe crear el archivo `.env` en la carpeta `app` con las mismas variables que el `.env.example` que está en esa carpeta. Deberá conseguir el `DIRECTUS_TOKEN` del Directus que use. Una vez definido esto puede correr el servidor de la siguiente forma:
- crear la variable de entorno `export LOAD_ENV=True` para que el servidor busque y cargue el `.env`
- en desarrollo activar modo debug `export FLASK_ENV=development`
- ejectuar `flask run`
- debería haber hosteado en [http://localhost:5000]()

---

### Documentación vieja 

Página web que trae contenido (imágenes y textos) de Directus.

Para que corra hay que tener python 3.x instalado y acceso a algún Directus.

El Directus debe tener las tablas `textos` e `imagenes` que es de donde reposa la mayor parte del contenido del site. Además, donde sea que haya una estructura de listados en el site, por ejemplo un carousel o un ul, debe haber una respectiva tabla de `items_<concepto>` con la cantidad de columnas que hagan falta para construir un item del listado. Por ej., si en un lugar del site hay una colección de cajas clickeables con título, imagen de fondo y url, se debe hacer la tabla `items_algo_descriptivo` con las columnas `titulo | imagen_fondo | url`.

El archivo `config.py` sirve para algunas configuraciones:
- **SERVER_HOST** en qué IP se hosteará la página
- **SERVER_PORT** el puerto
- **USE_SCSS** *\[True|False\]* si se usa Flask-Scss para compilar en vivo los `.scss` a `.css` o no
- **DIRECTUS_URL_INTERNAL** la dirección a la que se irá a buscar la api
- **DIRECTUS_URL_EXTERNAL** la dirección pública de Directus (se usa en las urls de la imágenes en los htmls)

Ojo con la configuraciones *\[True|False\]* que deben tener la primer letra mayúscula, tal cual como se lee

Cuidado al utilizar Flask-scss ya que cada vez que editen un `.scss` va a generar su `.css` en tiempo real **pisando el que ya estaba**.
