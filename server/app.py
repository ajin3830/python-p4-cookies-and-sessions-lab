#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    return make_response([article.to_dict() for article in articles], 200)

@app.route('/articles/<int:id>')
def show_article(id):
    # This line creates a new entry in a user's session, 
    # which is a way of storing data for each user 
    # who visits the website. If the user already 
    # has a session with a page_views key, 
    # its value is retrieved. Otherwise, the value is set to 0.
    session['page_views'] = session.get('page_views') or 0
    # increments the value of page_views for the current user's session by 1.
    session['page_views'] += 1

    if session['page_views'] <= 3:
        article = Article.query.filter_by(id=id).first()
        return make_response(article.to_dict(), 200)
    return make_response ({'message': 'Maximum pageview limit reached'}, 401)
    # 401 request not authorized

    # make_response is optional, it makes code look cleaner 
    # and easier to replicate (even automate!) in other views.
    # if session['page_views'] <= 3:
    #     return Article.query.filter(Article.id == id).first().to_dict(), 200
    # return {'message': 'Maximum pageview limit reached'}, 401

if __name__ == '__main__':
    app.run(port=5555)
