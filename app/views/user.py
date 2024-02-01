from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory)
import uuid
import os

from app.utils import *
from app.db.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

# Routes /user/...
user_bp = Blueprint('user', __name__, url_prefix='/user')

# Route /user/profile accessible uniquement à un utilisateur connecté grâce au décorateur @login_required

@user_bp.route('/profile')
@login_required
def show_profile():
    return render_template('user/profile.html')


UPLOAD_FOLDER = 'app/static/image_uploads/'


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
        profil_pic = request.files['profilePic']
    
        
        
        if profil_pic : 
            pic_filename = secure_filename(profil_pic.filename)
            #set uuid
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            #save image
            profil_pic.save(os.path.join(UPLOAD_FOLDER, pic_name))
            profil_pic = pic_name
            try:
                db.execute("UPDATE user SET profil_pic = ? WHERE id_user = ?",(profil_pic, user_id,))
                db.commit()
            except db.IntegrityError:

                error = f"Une erreur a eu lieu, veuillez réessayer !"
                flash(error)
                return render_template('user/profile.html')
        
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
        if new_password != user['password'] and new_password == new_verify_password and len(new_password)>= 8 :
            if not check_password_hash(user['password'], new_password):
                try:
                    db.execute("UPDATE user SET password = ? WHERE id_user = ?",(generate_password_hash(new_password),user_id))
                    db.commit()
                    flash('Changement de mot de passe effectué')
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



