from cards import db, login_manager,bcrypt 
from flask_login import UserMixin
from datetime import datetime, timezone

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    user_role = db.Column(db.Integer(), db.ForeignKey('roles.id'))
    topics = db.relationship('Topic', backref='author', lazy=True)
    role = db.relationship('Roles', backref='role', lazy=True)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    # check if a provided plain-text password matches the hashed password stored in the "password_hash" column
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Roles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    role_name = db.Column(db.String(length=30), nullable=False, unique=True)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category =db.Column(db.String(60), unique=False)
    difficulty = db.Column(db.String(60), unique=False)    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    cards = db.relationship('Card', backref='topic', lazy=True ,cascade='all, delete-orphan')

    def delete_topic(self):
        db.session.delete(self)
        db.session.commit()

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    last_reviewed = db.Column(db.DateTime)
    next_review = db.Column(db.DateTime)    

class ReviewSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_time = db.Column(db.DateTime)
    cards_studied = db.Column(db.Integer)
    user = db.relationship('User', backref='sessions')

class PerformanceStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    streak = db.Column(db.Integer, default=0)  # Correct answer streak
    ease_factor = db.Column(db.Float, default=2.5)  # For advanced spaced repetition

    user = db.relationship('User', backref='stats')
    card = db.relationship('Card', backref='stats')

class Chart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_details = db.Column(db.Text(), nullable= False)