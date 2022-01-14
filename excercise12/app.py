from flask import Flask

###### App setup
app = Flask(__name__)
app.config.from_pyfile('settings.py')

###### Pages
from pages.assignment12.assignment12 import assignment12
app.register_blueprint(assignment12)

if __name__ == '__main__':
    app.run(debug=True)
