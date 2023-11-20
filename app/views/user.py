from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.utils import *
from app.db.db import get_db

# Routes /user/...
user_bp = Blueprint('user', __name__, url_prefix='/user')

# Route /user/profile accessible uniquement à un utilisateur connecté grâce au décorateur @login_required

@user_bp.route('/profile')
@login_required
def show_profile():
    
    return render_template('user/profile.html')



@user_bp.route('/profile_update', methods=('GET', 'POST'))
@login_required
def update_profile():
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
        
        if new_first_name != user['first_name'] :
            try:
                db.execute("UPDATE user SET first_name = ? WHERE id_user = ?",(new_first_name,user_id,))
                db.commit()
                
            except db.IntegrityError:

                    error = f"Une erreur a eu lieu, veuillez réessayer !"
                    flash(error)
                    return render_template('user/profile.html')
        
        if new_name != user['name'] :
            try:
                db.execute("UPDATE user SET name = ? WHERE id_user = ?",(new_name,user_id,))
                db.commit()
                flash("La modification a été effectuée !")
                
            except db.IntegrityError:

                    error = f"Une erreur a eu lieu, veuillez réessayer !"
                    flash(error)
                    return render_template('user/profile.html')
        
        if new_email != user['email'] :
            try:
                db.execute("UPDATE user SET email = ? WHERE id_user = ?",(new_email,user_id,))
                db.commit()
                
            except db.IntegrityError:

                    error = f"Une erreur a eu lieu, veuillez réessayer !"
                    flash(error)
                    return render_template('user/profile.html')
        
        if new_phone_number != user['phone_number'] :
            try:
                db.execute("UPDATE user SET phone_number = ? WHERE id_user = ?",(new_phone_number,user_id,))
                db.commit()
                
            except db.IntegrityError:

                    error = f"Une erreur a eu lieu, veuillez réessayer !"
                    flash(error)
                    return render_template('user/profile.html')
       
        db = get_db()
        g.user = db.execute('SELECT * FROM user WHERE id_user = ?', (user_id,)).fetchone()
      

        return render_template('user/profile.html')


        
@user_bp.before_app_request
def load_logged_in_user():

    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None

    else:
        db = get_db()
        g.user = db.execute('SELECT * FROM user WHERE id_user = ?', (user_id,)).fetchone()



