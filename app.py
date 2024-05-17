import logging
from waitress import serve
from src import create_app


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    app = create_app()
    # app.run(host='0.0.0.0', port=9000)
    serve(app, host='0.0.0.0', port=9000)