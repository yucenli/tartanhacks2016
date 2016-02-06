from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), index=True)
    lastname = db.Column(db.String(64), index=True)
    andrewid = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index=True)

    def __init__(self, firstname, lastname, andrewid, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.andrewid = andrewid.lower()
        self.password = password.title()

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)

