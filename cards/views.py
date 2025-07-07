from cards import *
from flask import Blueprint, render_template, redirect, url_for, flash, request,jsonify, send_from_directory
from flask_login import login_required, current_user
from .models import User, Topic, Card
from . import db
from datetime import datetime, timedelta
from sqlalchemy import or_, and_
import re
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


study = Blueprint('study', __name__)

@study.route('/Dash')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login_page'))

    topics = Topic.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', topics=topics)

@study.route('/create_topic', methods=['GET','POST'])
@login_required
def create_topic():
    if request.method == 'POST':
        try:
            form = request.form
            new_topic = Topic(
                user_id = current_user.id,
                title = form.get('topicTitle','empty'),
                description = form.get('topicDescription','empty'),
                category = form.get('topicCategory','empty'),
                difficulty  = form.get('topicDifficulty'),
            ) 
            db.session.add(new_topic)
            db.session.flush()

            new_card = Card(
                topic_id =new_topic.id,
                question = form.get('card-question')
            )
            db.session.add(new_card)

            db.session.commit()
            flash('Topic and card created successfully!', 'success')
            return redirect(url_for('study.review_topic'))
        
        except Exception as e:
            print(e)
            flash(f'An error has occurred!', 'danger')      
    return render_template('decks.html')

@study.route('/review', methods=['GET', 'POST'])
@login_required
def review_topic():
    if request.method == 'POST':
        topic_to_delete = request.form.get('topic_delete')

        if topic_to_delete:
            try:
                selected_topic = Topic.query.filter_by(id = topic_to_delete, user_id=current_user.id).first()
                if selected_topic:
                    selected_topic.delete_topic()
                    flash('topic deleted from group', 'success')
            except Exception as e:
                flash('an error occurred!', 'danger')
            return redirect(url_for('study.review_topic'))
            
    if request.method == 'GET':   
        try:
            topics_data = {level: Topic.query.filter_by(
                    user_id =current_user.id,
                    difficulty = level 
                ).all()
                for level in ['beginner', 'intermediate', 'advanced']
            }

            cards_data = Card.query.join(Topic).filter(
                Topic.user_id == current_user.id
            ).all()

        except Exception as e:
            flash('an error occurred!', 'danger')
        return  render_template('review.html', topics_data=topics_data, cards_data=cards_data)

@study.route('/Stats', methods=['GET','POST'])
@login_required
def study_stats():
    return render_template('stats.html')

@study.route('/chat', methods=['GET','POST'])
@login_required
def chat_AI():
    if request.method == 'POST':            
        try:
            # api_key = 'sk-3d359b05846d478d9465f2ea9b440359'
            api_key = os.environ.get('DEEPSEEK_API_KEY')
            client = OpenAI(api_key=api_key, base_url='https://api.deepseek.com')

            data = request.get_json()
            topic_id = data.get('topic_id', 'empty')
            topic_title = data.get('topic_title', '')
            print(topic_title)
        
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": f'Create a comprehensive but concise study summary about {topic_title} for a student. Include key concepts and examples.'},
                ],
                temperature=0.7,
                max_tokens = 1000,
                # stream=False
            )

            # Return the AI response
            return jsonify({
                "response": response.choices[0].message.content,
                "topic_id": topic_id,
                "topic": topic_title
            })
        except Exception as e:
            return e
    return render_template('includes/chat.html')