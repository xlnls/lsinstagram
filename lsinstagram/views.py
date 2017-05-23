# coding=utf-8
from lsinstagram import app,db
from flask import render_template,redirect,request,flash,get_flashed_messages
from models import Image,User
import random,hashlib
from flask_login import logout_user,login_user,current_user,login_required
@app.route('/')
def index():
    images = Image.query.order_by('id desc').limit(10).all()
    return render_template('index.html', images=images)

@app.route('/image/<int:image_id>')
def image(image_id):
    image = Image.query.get(image_id)
    if image ==None:
        return redirect('/')
    return render_template( 'pageDetail.html ',image=image)

@app.route('/profile/<int:user_id>/')
def profile(user_id):
     user = User.query.get(user_id)
     if user==None:
         return redirect('/')
     return render_template('profile.html',user=user)

@app.route('/regloginpage/')
def regloginpage():
    return render_template('login.html')

def redirect_with_msg(target,msg,category):
    if msg!=None:
        flash(msg,category=category)
    return redirect(target)


@app.route('/reg/')
def reg():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    user = User.query.filter_by(username=username).first()
    if user!=None:
       return  redirect_with_msg('/regloginpage/',u'用户名已经存在','relogin')

    salt = '.'.join(random.sample('0123456780asjjshfjkgakgjhgtvvgAFGYEVTCKHREE'))
    m=hashlib.md5()
    m.update(password+salt)
    password = m.hexdigest()

    user = User(username,password,salt)
    db.session.add(user)
    db.session.commit()



    return redirect('/')