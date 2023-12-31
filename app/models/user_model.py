from database_service import db



class User(db.Model):
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.id}>'

