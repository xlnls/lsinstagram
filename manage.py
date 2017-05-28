# -*- encoding: utf-8 -*-

from lsinstagram import app,db
from flask_script import Manager
import random
from lsinstagram.models import User,Image,Comment
manager = Manager(app)

def get_image_url():
    return 'http://images.nowcoder.com/head/'+str(random.randint(0,1000))+'m.png'

@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    for i in range(0, 100):
        db.session.add(User('胡歌' + str(i), 'a' + str(i)))
        for j in range(0, 3):
            db.session.add(Image(get_image_url(),i+1))
            for k in range(0, 3):
                db.session.add(Comment('胡歌真帅 '+str(k), 1 + 3 * i + j, 1 + j))
    db.session.commit()

if __name__=='__main__':
    manager.run()
