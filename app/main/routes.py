from flask import Blueprint, render_template, redirect, url_for, flash, session

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
def dashboard():
    if not session.get('user_id'):
        flash('Vous devez être connecté pour accéder au tableau de bord.', 'error')
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')
