from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

pet_bp = Blueprint('pet', __name__, url_prefix='/pet')


@pet_bp.route('/mesanimaux',methods=['GET','POST'])
def home_pet():
    return render_template('pet/mypets.html')
