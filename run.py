from app import create_app
import os

# cofigs = Azure | Mooo | Local | Casa | Remote
config = os.environ.get('FLASK_CONFIG') or 'Remote'

app = create_app(config)

if __name__ == '__main__':
    app.run(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'])
