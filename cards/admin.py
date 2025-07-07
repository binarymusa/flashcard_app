from flask import Blueprint, render_template, redirect, url_for, flash, request,session
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db
import re
from sqlalchemy import or_, and_

admin = Blueprint('adm', __name__,)

@admin.route('/admn_book', methods=['GET', 'POST'])
@login_required
def admin_books():
    try:
        user_data = User.query.filter(or_(User.user_role != 1 , User.user_role == None)).all()
        print(f'user_data: {user_data}')
        return render_template('includes/admin_book.html', user_data=user_data)
    except Exception as e:
        print(f"Error Rendering Template: {e}")
        return f"Template Error: {e}"
        
