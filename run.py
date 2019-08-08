from app import create_app

app = create_app()

if __name__ == '__main__':
    print('Hosteando app en {}:{}'.format(app.config['SERVER_HOST'], app.config['SERVER_PORT']))
    app.run(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'])
