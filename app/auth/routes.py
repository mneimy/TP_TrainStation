from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User
from app.forms import UserForm, LoginForm
from app.database.queries import DatabaseQueries

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_queries = DatabaseQueries()
        user_data = db_queries.get_user_by_credentials(
            form.nom.data, 
            form.prenom.data, 
            form.age.data
        )
        
        if user_data:
            session['user_id'] = user_data['id_user']
            session['user_name'] = f"{user_data['prenom']} {user_data['nom']}"
            flash(f'Bienvenue {user_data["prenom"]} {user_data["nom"]}!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Utilisateur non trouvé. Vérifiez vos informations ou inscrivez-vous.', 'error')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        db_queries = DatabaseQueries()
        
        # Vérifier si l'utilisateur existe déjà
        if db_queries.user_exists(form.nom.data, form.prenom.data, form.age.data):
            flash('Cet utilisateur existe déjà!', 'error')
            return render_template('auth/register.html', form=form)
        
        # Créer l'utilisateur
        user_id = db_queries.create_user(
            form.nom.data,
            form.prenom.data,
            form.age.data
        )
        
        if user_id:
            session['user_id'] = user_id
            session['user_name'] = f"{form.prenom.data} {form.nom.data}"
            flash(f'Compte créé avec succès! Bienvenue {form.prenom.data} {form.nom.data}!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Erreur lors de la création du compte. Veuillez réessayer.', 'error')
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('main.index'))