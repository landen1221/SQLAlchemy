from models import db, connect_db, Users, Post, PostTag, Tag
from app import app
import datetime

db.drop_all()
db.create_all()


Users.query.delete()
Post.query.delete()
PostTag.query.delete()
Tag.query.delete()

# Add sample employees and departments
u1 = Users(first_name='Matthew', last_name='Landen', image_url='https://scontent-lax3-1.xx.fbcdn.net/v/t1.0-9/121128669_3319691564774959_4657080899566604286_o.jpg?_nc_cat=105&ccb=2&_nc_sid=730e14&_nc_ohc=HETS4WJ5CeIAX9app7l&_nc_ht=scontent-lax3-1.xx&oh=2e7819cb540e412d770f7e30903d294c&oe=5FE306D0')
u2 = Users(first_name='Cara', last_name='Rimel', image_url='https://scontent-lax3-1.xx.fbcdn.net/v/t1.0-9/39594023_1807883552622442_6248511820303171584_o.jpg?_nc_cat=102&ccb=2&_nc_sid=09cbfe&_nc_ohc=i-75Dm-SHyIAX-rrmAN&_nc_ht=scontent-lax3-1.xx&oh=94244aef1661bc5e304fd92370a4b4af&oe=5FE1F8CC')
u3 = Users(first_name='Bella', last_name='Landen', image_url='https://scontent-lax3-1.xx.fbcdn.net/v/t1.0-9/11425470_10207173074669051_3655061201054671140_n.jpg?_nc_cat=101&ccb=2&_nc_sid=cdbe9c&_nc_ohc=yv2jfWG__usAX9LGYEc&_nc_ht=scontent-lax3-1.xx&oh=b5f9fc8019efe2eeaf9e2758171c44f6&oe=5FE1F1DD')

p1 = Post(title='Ruff', content='Bark Bark!', created_at=datetime.datetime.now(), user_id=1)
p2 = Post(title='First post is best', content='I love blogging', created_at=datetime.datetime.now(), user_id=1)


db.session.add_all([df, dl, dm, leonard, liz, maggie, nadine])
db.session.commit()

pc = Project(proj_code='car', proj_name='Design Car',
             assignments=[Employees_projects(emp_id=liz.id, role='Chair'),
                          Employees_projects(emp_id=maggie.id)])
ps = Project(proj_code='server', proj_name='Deploy Server',
             assignments=[Employees_projects(emp_id=liz.id),
                          Employees_projects(emp_id=leonard.id, role='Auditor')])

db.session.add_all([ps, pc])
db.session.commit()