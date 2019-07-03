# webcausascomunes

Para que corra hay que tener python 3.x instalado.

Una vez instalado solo hay que instalar Flask haciendo `pip3 install flask`.

Para correrlo:
- ubicarse en la carpeta del proyecto
- configurar la variable de entorno `export FLASK_APP=app`
- ejectuar `flask run`

Para acceder entrar por [http://localhost:5000](http://localhost:5000)

El archivo `config.py` sirve para algunas configuraciones:
- **SERVER_HOST** en qué IP se hosteará la página
- **SERVER_PORT** el puerto
- **USE_DIRECTUS** *\[True|False\]* si el site busca los textos e imágenes en el servidor Directus o en `directus_fake.py`
- **USE_EXTENSIONS** *\[True|False\]* si el site carga las extensiones de bases de datos y login o no
- **USE_SCSS** *\[True|False\]* si se usa Flask-Scss para compilar en vivo los `.scss` a `.css` o no

Ojo con la configuraciones *\[True|False\]* que deben tener la primer letra mayúscula, tal cual como se lee

Si desean usar Flask-Scss hay que instalarlo haciendo `pip3 install flask-scss` y habilitar la configuración **USE_SCSS**. A partir de ese momento, cada vez que editen un `.scss` va a generar su `.css` en tiempo real **pisando el que ya estaba**.
