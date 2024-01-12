from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import UniqueConstraint

db = SQLAlchemy()



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    favorites = db.relationship('Favorites', back_populates='user')

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, it's a security breach
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)

    favorites = db.relationship('Favorites', back_populates='planet')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "population": self.population
            # Add other fields as needed
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    hair_color = db.Column(db.String(250), nullable=False)

    favorites = db.relationship('Favorites', back_populates='character')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "mass": self.mass,
            "height": self.height,
            "hair_color": self.hair_color
            # Add other fields as needed
        }


class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=True)

    user = db.relationship('User', back_populates='favorites')
    planet = db.relationship('Planets', back_populates='favorites')
    character = db.relationship('Characters', back_populates='favorites')

    __table_args__ = (
        UniqueConstraint('user_id', 'planet_id'),
        UniqueConstraint('user_id', 'character_id'),
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.user_id,
            "mass": self.planet_id,
            "height": self.character_id,
            # Add other fields as needed
        }

        # No funciona el añadir favoritos porque devuelve un error 
        #ntegrity error. (psycopg2.errors.NotNullViolation) null value in column "id" of relation "favorites" violates not-null constraint DETAIL: Failing row contains (1, 1, null, null). 
        #[SQL: INSERT INTO favorites          (user_id, planet_id, character_id) 
        # y debería ser
        #[SQL: INSERT INTO favorites (***id***,user_id, planet_id, character_id) 
