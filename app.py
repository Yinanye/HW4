from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'

class PokemonForm(FlaskForm):
    pokemon_name = StringField('Pokemon_Name', validators=[DataRequired()])



@app.route('/')
def index():
    return render_template('index.html', pageTitle='Pokemon')

@app.route('/add_pokemon', methods=['GET', 'POST'])
def add_pokemon():
    form = PokemonForm()
    if form.validate_on_submit():
        return "<h2> Pokemon's name is {0}".format(form.pokemon_name.data)

    return render_template('add_pokemon.html', form=form, pageTitle='Add A New Pokemon')

if __name__ == '__main__':
    app.run(debug=True)
