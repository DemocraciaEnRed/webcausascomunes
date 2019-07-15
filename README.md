# webcausascomunes

Página web que trae contenido (imágenes y textos) de Directus.

Para que corra hay que tener python 3.x instalado y acceso a algún Directus.

El Directus debe tener las tablas `textos` e `imagenes` que es de donde reposa la mayor parte del contenido del site. Además, donde sea que haya una estructura de listados en el site, por ejemplo un carousel o un ul, debe haber una respectiva tabla de `items_<concepto>` con la cantidad de columnas que hagan falta para construir un item del listado. Por ej., si en un lugar del site hay una colección de cajas clickeables con título, imagen de fondo y url, se debe hacer la tabla `items_algo_descriptivo` con las columnas `titulo | imagen_fondo | url`.

El sitio utiliza Flask como framework base y Requests para consumir la api de Directus, y opcionalmente Flask-scss para soportar sass. Por ende es necesario hacer `pip3 install flask requests [flask-scss]`.

Para correrlo:
- ubicarse en la carpeta del proyecto
- configurar la variable de entorno `export FLASK_APP=app` y `export DIRECTUS_TOKEN=token_de_la_api`
- ejectuar `flask run`

Para acceder entrar por [http://localhost:5000](http://localhost:5000)

El archivo `config.py` sirve para algunas configuraciones:
- **SERVER_HOST** en qué IP se hosteará la página
- **SERVER_PORT** el puerto
- **USE_SCSS** *\[True|False\]* si se usa Flask-Scss para compilar en vivo los `.scss` a `.css` o no
- **DIRECTUS_URL_INTERNAL** la dirección a la que se irá a buscar la api
- **DIRECTUS_URL_EXTERNAL** la dirección pública de Directus (se usa en las urls de la imágenes en los htmls)

Ojo con la configuraciones *\[True|False\]* que deben tener la primer letra mayúscula, tal cual como se lee

Cuidado al utilizar Flask-scss ya que cada vez que editen un `.scss` va a generar su `.css` en tiempo real **pisando el que ya estaba**.
