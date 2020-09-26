import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "trivia"
database_path = "postgres://{}/{}".format(':5433', database_name)
#database_path = os.environ.get("DATABASE_URL")

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
Category

'''
class Category(db.Model):  

  id = Column(Integer, primary_key=True)
  type = Column(String)
  questions = db.relationship('Question', backref='category', lazy=True)

  def __init__(self, type):
    self.type = type

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }
    
'''
Question

'''
class Question(db.Model):  

  id = Column(Integer, primary_key=True)
  question = Column(String)
  answer = Column(String)
  difficulty = Column(Integer)
  category_id = Column(Integer, db.ForeignKey('category.id'), nullable=False)

  def __init__(self, question, answer, category, difficulty):
    self.question = question
    self.answer = answer
    self.category = category
    self.difficulty = difficulty

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': int(self.category.format()["id"]),
      'difficulty': self.difficulty
    }
