from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets
import os



conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)


app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class yye5_pokemonapp(db.Model):
    PokemonId = db.Column(db.Integer, primary_key=True)
    Pokemon_Name = db.Column(db.String(255))
    Type1 = db.Column(db.String(255))
    Type2 = db.Column(db.String(255))
    HP = db.Column(db.String(255))
    Attack = db.Column(db.String(255))
    Defense = db.Column(db.String(255))
    Sp_Atk = db.Column(db.String(255))
    Sp_Def = db.Column(db.String(255))
    Speed = db.Column(db.String(255))

    def __repr__(self):
        return "PokemonId: {0} | Pokemon_Name: {1} | Type1: {2} | Type2: {3} | HP: {4} | Attack: {5} | Defense: {6} | Sp_Atk: {7} | Sp_Def: {8} | Speed: {9}".format(self.PokemonId, self.Pokemon_Name, self.Type1, self.Type2, self.HP, self.Attack, self.Defense, self.Sp_Atk, self.Sp_Def, self.Speed)


class PokemonForm(FlaskForm):
    Pokemon_Name = StringField('Pokemon_Name', validators=[DataRequired()])
    Type1 = StringField('Type1', validators=[DataRequired()])
    Type2 = StringField('Type2', validators=[DataRequired()])
    HP = StringField('HP', validators=[DataRequired()])
    Attack = StringField('Attack', validators=[DataRequired()])
    Defense = StringField('Defense', validators=[DataRequired()])
    Sp_Atk = StringField('Sp_Atk', validators=[DataRequired()])
    Sp_Def = StringField('Sp_Def', validators=[DataRequired()])
    Speed = StringField('Speed', validators=[DataRequired()])



@app.route('/')
def index():
    all_pokemon = yye5_pokemonapp.query.all()
    return render_template('index.html', pokemon=all_pokemon, pageTitle='My Pokemon List')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = yye5_pokemonapp.query.filter(yye5_pokemonapp.Pokemon_Name.like(search)).all()
        return render_template('index.html', pokemon=results, pageTitle='My Pokemon List', legend="Search Results")




@app.route('/pokemon/new', methods=['GET', 'POST'])
def add_pokemon():
    form = PokemonForm()
    if form.validate_on_submit():
        pokemon = yye5_pokemonapp(Pokemon_Name=form.Pokemon_Name.data, Type1=form.Type1.data, Type2=form.Type2.data, HP=form.HP.data, Attack=form.Attack.data, Defense=form.Defense.data, Sp_Atk=form.Sp_Atk.data, Sp_Def=form.Sp_Def.data, Speed=form.Speed.data)
        db.session.add(pokemon)
        db.session.commit()
        return redirect('/')

    return render_template('add_pokemon.html', form=form, pageTitle='Add A New Pokemon',
                            legend="Add A New Pokemon")


@app.route('/pokemon/<int:PokemonId>', methods=['GET','POST'])
def pokemon(PokemonId):
    pokemon = yye5_pokemonapp.query.get_or_404(PokemonId)
    return render_template('pokemon.html', form=pokemon, pageTitle='Pokemon Details')


@app.route('/pokemon/<int:PokemonId>/update', methods=['GET','POST'])
def update_pokemon(PokemonId):
    pokemon = yye5_pokemonapp.query.get_or_404(PokemonId)
    form = PokemonForm()
    if form.validate_on_submit():
        pokemon.Pokemon_Name = form.Pokemon_Name.data
        pokemon.Type1 = form.Type1.data
        pokemon.Type2 = form.Type2.data
        pokemon.HP = form.HP.data
        pokemon.Attack = form.Attack.data
        pokemon.Defense = form.Defense.data
        pokemon.Sp_Atk = form.Sp_Atk.data
        pokemon.Sp_Def = form.Sp_Def.data
        pokemon.Speed = form.Speed.data
        db.session.commit()
        flash('Your Pokemon has been updated.')
        return redirect(url_for('pokemon', PokemonId=pokemon.PokemonId))
    #elif request.method == 'GET':
    form.Pokemon_Name.data = pokemon.Pokemon_Name
    form.Type1.data = pokemon.Type1
    form.Type2.data = pokemon.Type2
    form.HP.data = pokemon.HP
    form.Attack.data = pokemon.Attack
    form.Defense.data = pokemon.Defense
    form.Sp_Atk.data = pokemon.Sp_Atk
    form.Sp_Def.data = pokemon.Sp_Def
    form.Speed.data = pokemon.Speed
    return render_template('add_pokemon.html', form=form, pageTitle='Update Post',
                            legend="Update A Pokemon")



@app.route('/pokemon/<int:PokemonId>/delete', methods=['GET','POST'])
def delete_pokemon(PokemonId):
    if request.method == 'POST': #if it's a POST request, delete the friend from the database
        pokemon = yye5_pokemonapp.query.get_or_404(PokemonId)
        db.session.delete(pokemon)
        db.session.commit()
        flash('Pokemon was successfully deleted!')
        return redirect("/")
    else:
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
