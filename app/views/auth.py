from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from itsdangerous import URLSafeTimedSerializer as Serializer
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db
import os
from datetime import *
import random
import string


# Création d'un blueprint contenant les routes ayant le préfixe /auth/...
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Route /auth/register
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    # Si des données de formulaire sont envoyées vers la route /register (ce qui est le cas lorsque le formulaire d'inscription est envoyé)
    if request.method == 'POST':

        # On récupère les champs 'username' et 'password' de la requête HTTP
        first_name = request.form['first_name']
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        verify_password = request.form['verify_password']

        # On récupère la base de donnée
        db = get_db()

        # Si le nom d'utilisateur et le mot de passe ont bien une valeur
        # on essaie d'insérer l'utilisateur dans la base de données
        if first_name and name and email and phone_number and password and verify_password:
            if password != verify_password :
                flash("Mot de passe pas identique")
                return redirect(url_for("auth.register"))
            elif len(password) < 8 :
                flash("Veuillez entrer au minimum 8 charactères")
                return redirect(url_for("auth.register")) 
            
            else:
                try:
                    db.execute("INSERT INTO user (first_name, name, email, phone_number,password) VALUES (?,?,?,?,?)",(first_name, name, email,phone_number, generate_password_hash(password)))
                    # db.commit() permet de valider une modification de la base de données
                    db.commit()
                    db.close()
                    
                except db.IntegrityError:

                    # La fonction flash dans Flask est utilisée pour stocker un message dans la session de l'utilisateur
                    # dans le but de l'afficher ultérieurement, généralement sur la page suivante après une redirection
                    error = f"User {name+email+password} is already registered."
                    flash(error)
                    return redirect(url_for("auth.register"))
            
            
            return redirect(url_for("auth.login"))
            
         
        else:
            error = "Veuillez remplis tous les champs"
            flash(error)
            return redirect(url_for("auth.register"))
    else:
        # Si aucune donnée de formulaire n'est envoyée, on affiche le formulaire d'inscription
        return render_template('auth/register.html')


# Route /auth/login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Si des données de formulaire sont envoyées vers la route /login (ce qui est le cas lorsque le formulaire de login est envoyé)
    if request.method == 'POST':

        # On récupère les champs 'username' et 'password' de la requête HTTP
        email = request.form['email']
        password = request.form['password']

        # On récupère la base de données
        db = get_db()
        
        # On récupère l'utilisateur avec le username spécifié (une contrainte dans la db indique que le nom d'utilisateur est unique)
        # La virgule après username est utilisée pour créer un tuple contenant une valeur unique
        user = db.execute('SELECT * FROM user WHERE email = ?', (email,)).fetchone()
        # Si aucun utilisateur n'est trouve ou si le mot de passe est incorrect
        # on crée une variable error 
        error = None
        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        # S'il n'y pas d'erreur, on ajoute l'id de l'utilisateur dans une variable de session
        # De cette manière, à chaque requête de l'utilisateur, on pourra récupérer l'id dans le cookie session
        if error is None:
            
            session.clear()
            session['user_id'] = user['id_user']
            # On redirige l'utilisateur vers la page principale une fois qu'il s'est connecté
            return redirect("/")
        
        else:
            # En cas d'erreur, on ajoute l'erreur dans la session et on redirige l'utilisateur vers le formulaire de login
            flash(error)
            return redirect(url_for("auth.login"))
    else:
        return render_template('auth/login.html')

# Route /auth/logout
@auth_bp.route('/logout')
def logout():
    # Se déconnecter consiste simplement à supprimer le cookie session
    session.clear()
    # On redirige l'utilisateur vers la page principale une fois qu'il s'est déconnecté
    return redirect("/")

@auth_bp.route('/forgot_password', methods = ['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        db = get_db()
        try :
            id_user = db.execute("SELECT id_user FROM user WHERE email = ?",(email,)).fetchone()[0]
            db.execute("DELETE FROM token WHERE id_user_token = ?",(id_user,))
            token = ''.join(random.choices(string.ascii_letters + string.digits, k = 30))
            #date_exacte d'aujourd'hui + 5 minutes
            time = datetime.utcnow() + timedelta(minutes=5)
            #timestamp() -> time en nb float
            db.execute("INSERT INTO token (token, date_expire,id_user_token) values (?,?,?)",(token,time.timestamp(), id_user))
            db.execute("DELETE FROM token WHERE date_expire > ?", (time.timestamp(),))
            db.commit()
            return render_template('auth/reset_password.html')
        except :
            flash("Cet utilisateur n'existe pas.")
            render_template('auth/forgot_password.html')
        
    else:
        return render_template('auth/forgot_password.html')

@auth_bp.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_password(token):
    db = get_db()
    exist_token = db.execute("SELECT id_user_token, date_expire FROM token WHERE token = ?",(token,)).fetchone()
    if exist_token:
        if datetime.utcnow().timestamp()<int(exist_token['date_expire']):
            if request.method == 'POST':
                new_password = request.form['new_password']
                verify_password = request.form['verify_password']
                if len(new_password)>8:
                    if new_password == verify_password :
                        db.execute("UPDATE user SET password = ? WHERE id_user = ?", (generate_password_hash(new_password), exist_token['id_user_token']))
                        db.execute("DELETE FROM token WHERE id_user_token = ?", (exist_token['id_user_token'],))
                        db.commit()
                        return redirect(url_for('auth.login'))
                    else:
                        flash('Veuillez entrer des mots de passe identiques')
                        return redirect(url_for('auth.reset_password', token=token))
                else:
                    flash('Votre mot de passe doit contenir au moins 8 charactères !')
            else:
                return render_template('auth/reset_password.html')
        else:
            flash('Votre lien de changement a expiré !')
            return redirect(url_for('auth.forgot_password'))
    else:
        flash("La requête n'existe pas")
        return redirect(url_for('auth.forgot_password'))
            

# Fonction automatiquement appelée à chaque requête (avant d'entrer dans la route) sur une route appartenant au blueprint 'auth_bp'
# La fonction permet d'ajouter un attribut 'user' représentant l'utilisateur connecté dans l'objet 'g' 
@auth_bp.before_app_request
def load_logged_in_user():

    # On récupère l'id de l'utilisateur stocké dans le cookie session
    user_id = session.get('user_id')
    

    # Si l'id de l'utilisateur dans le cookie session est nul, cela signifie que l'utilisateur n'est pas connecté
    # On met donc l'attribut 'user' de l'objet 'g' à None
    if user_id is None:
        g.user = None

    # Si l'id de l'utilisateur dans le cookie session n'est pas nul, on récupère l'utilisateur correspondant et on stocke
    # l'utilisateur comme un attribut de l'objet 'g'
    else:
         # On récupère la base de données et on récupère l'utilisateur correspondant à l'id stocké dans le cookie session
        db = get_db()
        g.user = db.execute('SELECT * FROM user WHERE id_user = ?', (user_id,)).fetchone()





