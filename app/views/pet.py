from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

pet_bp = Blueprint('pet', __name__, url_prefix='/pet')


@pet_bp.route('/mesanimaux',methods=['GET','POST'])
def home_pet():
    return render_template('pet/mypets.html')



@pet_bp.route('/calculateur_de_ration')
def calculateur_de_ration():
    return render_template('home/calculateur.html')

@pet_bp.route('/calculateur_de_ration/cat_bee', methods=['GET','POST'])
def cat_bee():
    return render_template('pet/cat_bee.html')

@pet_bp.route('/calculateur_de_ration/dog_bee', methods=['GET','POST'])
def dog_bee():
    return render_template('pet/dog_bee.html')