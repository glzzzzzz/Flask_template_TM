from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

pet_bp = Blueprint('pet', __name__, url_prefix='/pet')


@pet_bp.route('/mesanimaux',methods=['GET','POST'])
def home_pet():
    return render_template('pet/mypets.html')



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
    return render_template('pet/dog_bee.html')