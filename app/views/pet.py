from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db
pet_bp = Blueprint('pet', __name__, url_prefix='/pet')


@pet_bp.route('/mesanimaux',methods=['GET','POST'])
def home_pet():
    if g.user :
        db = get_db()
        list_pet = db.execute('SELECT * FROM pet WHERE owner_id = ?',(g.user['id_user'],)).fetchall()
        return render_template('pet/mypets.html', list_pet = list_pet)
        
    else:
        return render_template('auth/login.html')


@pet_bp.route('/mesanimaux/<chip_number>', methods=['GET','POST'])
def pet_details(chip_number):
    db = get_db()
    list_pet = db.execute('SELECT * FROM pet WHERE owner_id = ?',(g.user['id_user'],)).fetchall()
    pet_details = db.execute('SELECT * FROM pet WHERE chip_number = ?',(chip_number,)).fetchone()
    if request.method == 'POST':
        flash('atteint')
        user_id = session['user_id']
        new_name = request.form['name_pet']
        new_breed = request. form['breed']
        new_chip_number = request.form['chip_number']
        new_date_birth = request.form['date_birth']
        
        if new_name != pet_details['name']:
            try:
                
                db.execute('UPDATE pet SET name = ? WHERE chip_number = ?',(new_name, chip_number,))
                db.commit()
                list_pet = db.execute('SELECT * FROM pet WHERE owner_id = ?',(g.user['id_user'],)).fetchall()
                pet_details = db.execute('SELECT * FROM pet WHERE chip_number = ?',(chip_number,)).fetchone()
                db.close()
                return render_template('pet/pet_info.html', pet_details=pet_details, list_pet = list_pet)
            except db.IntegrityError:

                    error = f"Une erreur a eu lieu, veuillez réessayer !"
                    flash(error)
                    return render_template('pet/pet_info.html', pet_details=pet_details, list_pet = list_pet)

    return render_template('pet/pet_info.html', pet_details=pet_details, list_pet = list_pet)

@pet_bp.route('/mesanimaux/nouvel_animal', methods=['GET','POST'])
def new_pet():
    db = get_db()
    list_pet = db.execute('SELECT * FROM pet WHERE owner_id = ?',(g.user['id_user'],)).fetchall()
    if request.method == 'POST':
        name_pet = request.form['name_pet']
        chip_number = request.form['chip_number']
        breed = request.form['breed']
        date_birth = request.form['date_birth']
        user_id = session['user_id']
        try:
            db.execute("INSERT INTO pet (chip_number,owner_id, name, breed, date_birth) VALUES (?,?,?,?,?)",(chip_number,user_id, name_pet,breed, date_birth,))
            db.commit()
            db.close()
            flash('Vous avez ajouté un nouvel animal.')
            return redirect(url_for('pet.home_pet', list_pet = list_pet))
        except db.IntegrityError:
            flash('Une erreur à eu lieu, veuillez réessayer.')
            return render_template('pet/add_new_pet.html', list_pet = list_pet)
        
    else:
        return render_template('pet/add_new_pet.html', list_pet = list_pet)
















@pet_bp.route('/calculateur_de_ration')
def calculateur_de_ration():
    return render_template('home/calculateur.html')

@pet_bp.route('/calculateur_de_ration/cat_ration', methods=['GET','POST'])
def cat_bee():
    cat_bee=None
    if request.method =="POST":
        physical_activity =request.form.get('physical_activity')
        status_cat=request.form.get('status_cat')
        weight = request.form.get('weight')
        if physical_activity and status_cat :
            if physical_activity == "inactive":
                physical_activity = 0.7
            elif physical_activity == "not_very_active":
                physical_activity = 0.9
            elif physical_activity == "normal":
                physical_activity = 1
            elif physical_activity == "active":
                physical_activity = 1.1
            elif physical_activity == "very_active":
                physical_activity = 1.2
                flash(physical_activity)
            else:
                flash("Veuillez selectionner une situation physique pour votre chat !")
                return render_template('pet/cat_bee.html', cat_bee=None)

            
            if status_cat == "sterilized":
                status_cat = 0.8
            elif status_cat == "not_sterilized":
                status_cat = 1
            else:
                flash("Veuillez sélectionner un statut sexuel pour votre chat !")
                return render_template('pet/cat_bee.html',cat_bee=None)
            
        if not weight :
            flash("Veuillez entrer le poids de votre animal !")
            return render_template('pet/cat_bee.html',cat_bee=None)
        else:
            
            cat_bee = round((60*float(weight)*physical_activity*status_cat), 2)
            
    
    return render_template('pet/cat_bee.html', cat_bee=cat_bee)

@pet_bp.route('/calculateur_de_ration/dog_ration', methods=['GET','POST'])
def dog_bee():
    dog_bee=None
    if request.method =="POST":
        race = request.form.get('race')
        physical_activity =request.form.get('physical_activity')
        status_dog=request.form.get('status_dog')
        weight = request.form.get('weight')
        if physical_activity and status_dog and race :
            if physical_activity == "inactive":
                physical_activity = 0.7
            elif physical_activity == "not_very_active":
                physical_activity = 0.9
            elif physical_activity == "normal":
                physical_activity = 1
            elif physical_activity == "active":
                physical_activity = 1.1
            elif physical_activity == "very_active":
                physical_activity = 1.2
                flash(physical_activity)
            else:
                flash("Veuillez selectionner une situation physique pour votre chien !")
                return render_template('pet/dog_bee.html', dog_bee=None)
            
            if race =="nordics_races_1":
                race == 0.8
            elif race =="races_2":
                race == 0.9
            elif race=="other_3":
                race == 1 
            elif race == "races_4":
                race == 1.1
            else:
                flash("Veuillez selectionner un groupe de races pour votre chien !")
                return render_template('pet/dog_bee.html', dog_bee=None)
                
                
            
            if status_dog == "sterilized":
                status_dog = 0.8
            elif status_dog == "not_sterilized":
                status_dog = 1
            else:
                flash("Veuillez sélectionner un statut sexuel pour votre chien !")
                return render_template('pet/dog_bee.html',dog_bee=None)
            
        if not weight :
            flash("Veuillez entrer le poids de votre animal !")
            return render_template('pet/dog_bee.html',dog_bee=None)
        else:
            
            dog_bee = round((130*float(weight)*physical_activity*status_dog*race), 2)
            
    
    return render_template('pet/dog_bee.html', dog_bee=dog_bee)
    