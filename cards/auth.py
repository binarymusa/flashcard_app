from flask import Blueprint, render_template, redirect, url_for, flash, request,session
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db
import re
from sqlalchemy import or_, and_

auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
   if not current_user.is_authenticated:
      return redirect(url_for('auth.login_page'))

   return render_template('index.html')

@auth.route('/login', methods=['GET', 'POST'])
def login_page():
   if request.method == 'POST':
      form = request.form

      try:
         check_user = User.query.filter_by(email=form.get('email','empty').lower()).first()

         if check_user and check_user.check_password_correction(attempted_password=form.get('password', ',empty')):
            login_user(check_user) 

            #  Access the associated role object via the role relationship
            if check_user.role and check_user.role.role_name == 'Admin':
               flash(f'Admin Login successful','success')
               return redirect(url_for('adm.admin_books'))
            else:
               flash(f'Login successful', 'success')
               return redirect(url_for('study.index'))
         else:
            flash(f'Incorrect username or Password', 'danger')
            return redirect(url_for('auth.login_page'))
      except Exception as e:
         print(f'error: {e}')
         flash(f'An error occurred!', 'danger')

   return render_template('login.html')   

@auth.route('/signup' , methods=['GET', 'POST'])
def signup_page():
   if request.method == 'POST':
      form = request.form
      existing_user = User.query.filter(and_(User.username == form.get('username', 'empty') , User.email == form.get('email', 'empty'))).first()
      
      if existing_user:
         flash(f'User already exists. Try different credentials', 'danger')
         return redirect(url_for('auth.signup_page'))
      else: 
         reg_exp = '^\S+(\@gmail\.com$|\@hotmail\.com$|\@yahoo\.com$)$'
         try:
            if (not(re.search(reg_exp, form.get('email')))):
               flash('Invalid email address!', 'danger')
               return redirect(url_for('auth.signup_page'))
            else:           
               new_user = User(username=form.get('username', 'empty'), email=form.get('email', 'empty'), password=form.get('password', 'empty'))
               db.session.add(new_user)
               db.session.commit()

               login_user(new_user)
               flash(f'signup successful', 'success') 
               return redirect(url_for('study.index'))     
         except:
            flash('an error occured', 'danger')

   return render_template('signup.html')
   
@auth.route('/pswdreset', methods=['GET', 'POST'])
def pswd_rst():
   if request.method == 'POST':
      email = request.form['email']

      if current_user.id and email:
         pass
   
@auth.route('/logout')
@login_required
def logout():
   logout_user()
   return redirect(url_for('auth.login_page'))