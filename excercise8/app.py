from flask import Flask, redirect, render_template

app = Flask(__name__)


@app.route('/cv')
def cv():
    return render_template('cv.html')


@app.route('/')
def home():
    return redirect('/cv')


@app.route('/assignment8')
def assignment8():
    return render_template('assignment8.html', firstName='Yaniv', lastName='Lipovitsky',
                           hobbies=('Training in Triathlon', 'Netflix', 'Food'),
                           music=('Queen', 'Pearl Jam', 'Janis Joplin'))


if __name__ == '__main__':
    app.run(debug=True)
