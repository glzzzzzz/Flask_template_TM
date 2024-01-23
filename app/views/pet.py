from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db
from flask_wtf import FlaskForm
from datetime import datetime


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
    session.pop('chip_number', None)
    session['chip_number'] = chip_number
    
    list_pet = db.execute('SELECT * FROM pet WHERE owner_id = ?',(g.user['id_user'],)).fetchall()
    pet_details = db.execute('SELECT * FROM pet WHERE chip_number = ?',(chip_number,)).fetchone()
    list_vaccine = db.execute('SELECT * FROM vaccine WHERE pet_chip_number = ?',(chip_number,)).fetchall()
    list_meeting = db.execute('SELECT * FROM vet_meeting WHERE pet_chip_number = ?',(chip_number,)).fetchall()
    if request.method == 'POST':
        user_id = session['user_id']
        new_name = request.form['name_pet']
        new_breed = request. form['breed']
        new_chip_number = request.form['chip_number']
        new_date_birth = request.form['date_birth']
        
        try:
            if new_chip_number and new_chip_number != pet_details['chip_number']:
                db.execute('UPDATE pet SET chip_number = ? WHERE  chip_number = ?', (new_chip_number, chip_number,))
                db.commit()
            if new_name and new_name != pet_details['name']:
                db.execute('UPDATE pet SET name = ? WHERE chip_number = ?', (new_name, chip_number,))
                db.commit()
            if new_breed and new_breed != pet_details['breed']:
                db.execute('UPDATE pet SET breed = ? WHERE chip_number = ?', (new_breed, chip_number,))
                db.commit()
            if new_date_birth and new_date_birth != pet_details['date_birth']:
                db.execute('UPDATE pet SET date_birth = ? WHERE chip_number = ?', (new_date_birth, chip_number,))
                db.commit()
        except db.IntegrityError:
                error = f"Une erreur a eu lieu, veuillez réessayer !"
                flash(error)
                return render_template('pet/pet_info.html', pet_details=pet_details, list_pet = list_pet, list_vaccine = list_vaccine)
        
        list_pet = db.execute('SELECT * FROM pet WHERE owner_id = ?',(g.user['id_user'],)).fetchall()
        pet_details = db.execute('SELECT * FROM pet WHERE chip_number = ?',(chip_number,)).fetchone()
        
    db.close()
    return render_template('pet/pet_info.html', pet_details=pet_details, list_pet = list_pet, list_vaccine = list_vaccine, list_meeting = list_meeting)

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
            flash('Une erreur a eu lieu, veuillez réessayer.')
            return render_template('pet/add_new_pet.html', list_pet = list_pet)
        
    else:
        return render_template('pet/add_new_pet.html', list_pet = list_pet)

@pet_bp.route('/mesanimaux/nouveau_vaccin', methods = ['GET', 'POST'])
def new_vaccine():
    db = get_db()
    chip_number = session['chip_number']
    today_date = datetime.now()
    min_date = today_date.strftime('%Y-%m-%d')
    list_pet = db.execute('SELECT * FROM pet WHERE owner_id = ?',(g.user['id_user'],)).fetchall()
    pet_details = db.execute('SELECT * FROM pet WHERE chip_number = ?',(chip_number,)).fetchone()
    if request.method =='POST':
        date_meeting = request.form['date_meeting']
        reason_vaccine = request.form['reason_vaccine']
        vaccine_reminder = request.form['vaccine_reminder']
        try :
            db.execute("INSERT INTO vaccine(date_meeting,name, date_reminder, pet_chip_number) VALUES (?,?,?,?)", (date_meeting,reason_vaccine,vaccine_reminder,chip_number,))
            db.commit()           
            return redirect(url_for('pet.pet_details', chip_number = chip_number))
        except db.IntegrityError:
            flash('Une erreur à eu lieu, veuillez réessayer.')
            return render_template('pet/new_vaccine.html', list_pet = list_pet, pet_details = pet_details, min_date = min_date)
    else:
        return render_template('pet/new_vaccine.html', list_pet = list_pet, pet_details = pet_details, min_date = min_date)
    
@pet_bp.route('/mesanimaux/nouveau_rendez_vous', methods = ['GET', 'POST'])
def new_meeting():
    db = get_db()
    chip_number = session['chip_number']
    today_date = datetime.now()
    min_date = today_date.strftime('%Y-%m-%d')
    list_pet = db.execute('SELECT * FROM pet WHERE owner_id = ?',(g.user['id_user'],)).fetchall()
    pet_details = db.execute('SELECT * FROM pet WHERE chip_number = ?',(chip_number,)).fetchone()
    if request.method =='POST':
        date_meeting = request.form['date_meeting']
        reason_meeting = request.form['reason_meeting']
        try :
            db.execute("INSERT INTO vet_meeting(reason, date_of_meeting, pet_chip_number) VALUES (?,?,?)", (reason_meeting,date_meeting,chip_number,))
            db.commit()           
            return redirect(url_for('pet.pet_details', chip_number = chip_number))
        except db.IntegrityError:
            flash('Une erreur à eu lieu, veuillez réessayer.')
            return render_template('pet/new_meeting.html', list_pet = list_pet, pet_details = pet_details, min_date = min_date)
    else:
        return render_template('pet/new_meeting.html', list_pet = list_pet, pet_details = pet_details, min_date = min_date)


@pet_bp.route('/mesanimaux/supprimer_rendez_vous/<id_meeting>')
def delete_meeting(id_meeting):
    db = get_db()
    chip_number = session['chip_number']
    db.execute('DELETE FROM vet_meeting WHERE id_meeting = ?',(id_meeting,))
    db.commit()
    
    return redirect(url_for('pet.pet_details', chip_number = chip_number))

@pet_bp.route('/mesanimaux/supprimer_vaccin/<id_vaccine>')
def delete_vaccine(id_vaccine):
    db = get_db()
    chip_number = session['chip_number']
    db.execute('DELETE FROM vaccine WHERE id_vaccine = ?',(id_vaccine,))
    db.commit()
    
    return redirect(url_for('pet.pet_details', chip_number = chip_number))




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
    