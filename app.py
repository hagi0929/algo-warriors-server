import os
import argparse
from gunicorn.app.base import BaseApplication
from src import create_app
from dotenv import load_dotenv


class GunicornApp(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Flask app.')
    parser.add_argument('--env', type=str, default='dev', help='Set the environment: development or production')
    parser.add_argument('--gunicorn', action='store_true', help='Run with Gunicorn')
    args = parser.parse_args()
    load_dotenv()
    print()
    app = create_app(args.env)

    if args.gunicorn:
        bind = f"{app.config['HOST']}:{app.config['PORT']}"
        options = {
            'bind': bind,
            'workers': 4,
        }
        GunicornApp(app, options).run()
    else:
        app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
