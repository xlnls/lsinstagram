#--* encoding=utf-8 --*
from lsinstagram import app,db
from flask import render_template,redirect,request,flash,get_flashed_messages,send_from_directory
from models import Image,User
import random,hashlib,json,uuid,os
from flask_login import logout_user,login_user,current_user,login_required

@app.route('/',methods=['GET', 'POST'])
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
@login_required
def profile(user_id):
     user = User.query.get(user_id)
     if user==None:
         return redirect('/')

     paginate = Image.query.filter_by(user_id=user_id).paginate(page=1,per_page=3,error_out=False)
     return render_template('profile.html',user=user,images=paginate.items,has_next=paginate.has_next)


@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
def user_images(user_id,page,per_page):
    paginate=Image.query.filter_by(user_id=user_id).paginate(page=page,per_page=per_page)
    map = {'has_next':paginate.has_next}
    images=[]
    for image in paginate.items:
        imgvo = {'id':image.id,'url':image.url,'comment_count':len(image.comments)}
        images.append(imgvo)
    map['images']=images
    return json.dumps(map)


@app.route('/regloginpage/')
def regloginpage():
   msg=''
   for m in get_flashed_messages(with_categories=False,category_filter=['relogin']):
       msg = msg + m
   return render_template('login.html',msg=msg,next=request.values.get('next'))


def redirect_with_msg(target,msg,category):
    if msg!=None:
        flash(msg,category=category)
    return redirect(target)

@app.route('/login/',methods={'post','get'})
def login():
    username=request.values.get('username')
    password=request.values.get('password')

    if username ==''or password=='':
        return redirect_with_msg('/reloginpage/',u'用户名和密码不能为空','relogin')
    user = User.query.filter_by(username=username).first()

    if user==None:
        return redirect_with_msg('/reloginpage/', u'用户名不存在', 'relogin')

    m=hashlib.md5()
    m.update(password+user.salt)
    if(m.hexdigest()!=user.password):
        return redirect_with_msg('/reloginpage/', u'密码错误', 'relogin')

    login_user(user)

    next=request.values.get('next')

    if next!=None and next.startswith('/'):
        return redirect(next)
    return redirect('/')


@app.route('/reg/')
def reg():
    username = request.values.get('username')
    password = request.values.get('password')

    user = User.query.filter_by(username=username).first()

    if username ==''or password=='':
        return redirect_with_msg('/reloginpage/',u'用户名和密码不能为空','relogin')
    if user!=None:
       return  redirect_with_msg('/regloginpage/',u'用户名已经存在','relogin')

    salt = '.'.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyz',10))
    m=hashlib.md5()
    m.update(password+salt)
    password = m.hexdigest()

    user = User(username,password,salt)
    db.session.add(user)
    db.session.commit()

    login_user(user)

    next = request.values.get('next')

    if next != None and next.startswith('/'):
        return redirect(next)

    return redirect('/')


@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/')

def save_to_local(file,file_name):
    save_dir=app.config['UPLOAD_DIR']
    file.save(os.path.join(save_dir,file_name))
    return '/image/'+file_name

@app.route('/image/<image_name>')
def view_image(image_name):
    return send_from_directory(app.config['UPLOAD_DIR'],image_name)


@app.route('/upload',methods={"post"})
def upload():
    file=request.files['file']
    file_ext=''
    if file.filename.find('.')>0:
        file_ext=file.filename.rsplit('.',1)[1].strip().lower()
    if file_ext in app.config['ALLOWED_EXT']:
        filename=str(uuid.uuid1()).replace('-','')+'.'+file_ext
        url=save_to_local(file,filename)
        if url!=None:
            db.session.add(Image(url,current_user.id))
            db.session.commit()
    return redirect('/profile/%d' % current_user.id)