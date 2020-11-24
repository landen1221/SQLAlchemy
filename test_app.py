from unittest import TestCase

from app import app
from models import db, Users

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
    """Test Users DB functionality on website"""

    def setUp(self):
        """Add sample user."""

        Users.query.delete()

        user1 = Users(first_name = "Test", last_name='User')
        db.session.add(user1)
        db.session.commit()

        self.user = user1
        self.user_id = user1.id
    
    def tearDown(self):
        db.session.rollback()

    def test_adding_user(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f'/user-details/{self.user_id}')
            html = resp.get_data(as_text=True)
        
            self.assertIn('Test', html)
            #Test default image carries
            self.assertEqual(self.user.image_url, 'https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg')
    
    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.get(f'/delete-user/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertNotIn('Test', html)

