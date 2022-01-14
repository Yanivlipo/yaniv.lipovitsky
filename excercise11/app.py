from flask import Flask

###### App setup
app = Flask(__name__)
app.config.from_pyfile('settings.py')

###### Pages
from pages.assignment11.assignment11 import assignment11
app.register_blueprint(assignment11)

if __name__ == '__main__':
    app.run(debug=True)
