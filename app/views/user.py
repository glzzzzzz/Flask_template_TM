from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.utils import *
from app.db.db import get_db

# Routes /user/...
user_bp = Blueprint('user', __name__, url_prefix='/user')

# Route /user/profile accessible uniquement à un utilisateur connecté grâce au décorateur @login_required

@user_bp.route('/profile', methods=('GET', 'POST'))
@login_required
def show_profile():
    
    if request.method == 'POST':
        
        db = get_db()
        
        user_id = session['user_id']
        user = db.execute('SELECT * FROM user WHERE id_user = ?', (user_id,)).fetchone()
        
        new_first_name = request.form['first_name']
        new_name = request.form['name']
        new_email = request.form['email']
        new_phone_number = request.form['phone_number']
        new_password = request.form['password']
        new_verify_password = request.form['verify_password']
        
        flash(user_id)
        flash(user['first_name'])
        
        if new_first_name != user['first_name'] :
            db.execute("UPDATE user SET first_name = ? WHERE id_user = ?",(new_first_name,user_id,))
            flash("La modification a été effectuée !")
            test= db.execute('SELECT first_name FROM user WHERE id_user = ?',(user_id,))
            
    # Affichage de la page principale de l'application
    return render_template('user/profile.html')




