from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
    def get_user(email, password):
        user = User.query.filter_by(email=email, password=password).first()
        return user

class People(db.Model):
    __tablename__= 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable = False)
    birth_year = db.Column(db.String(40), nullable = False)
    gender = db.Column(db.String(200), nullable = False)
    height = db. Column(db.String(200), nullable = False)
    mass = db.Column(db.String(200), nullable = False)
    hair_color = db.Column(db.String(200), nullable = False)
    skin_color = db.Column(db.String(200), nullable = False)
    eye_color = db.Column(db.String(200), nullable = False)
    
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
        }
    def create_people(name, birth_year, gender, height, mass, hair_color, skin_color, eye_color):
        people = People(name=name, birth_year=birth_year, gender=gender, height=height, mass=mass, hair_color=hair_color, skin_color=skin_color, eye_color=eye_color)
        db.session.add(people)
        db.session.commit()

    def get_people(id):
        people = People.query.filter_by(id=id).first()
        return People.serialize(people)

    def get_all_people():
        all_people = People.query.all()
        all_people = list(map(lambda people: people.serialize(), all_people))
        return all_people

    def delete_people(id):
        people = People.query.get(id)
        db.session.delete(people)
        db.session.commit()


class Planet(db.Model):
    __tablename__= 'planet'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    rotation_period = db.Column(db.String(200), nullable = False)
    orbital_period = db.Column(db.String(200), nullable = False)
    diameter = db.Column(db.Integer, nullable = False)
    climate = db.Column(db.String(200), nullable = False)
    gravity = db.Column(db.String(200), nullable = False)
    terrain = db.Column(db.String(200), nullable = False)
    surface_water = db.Column(db.String(200), nullable = False)
    population = db.Column(db.String(200), nullable = False)
    

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "population": self.population,
            }

    def create_planet(name, rotation_period, orbital_period, diameter, climate, terrain, surface_water, population):
        planet = Planet(name=name, rotation_period=rotation_period, orbital_period=orbital_period, diameter=diameter, climate=climate, terrain=terrain, surface_water=surface_water, population=population)
        db.session.add(planet)
        db.session.commit()

    def get_planet(id):
        planet = Planet.query.filter_by(id=id)
        return Planet.serialize(planet)

    def get_all_planets():
        planets = Planet.query.all()
        planets = list(map(lambda planet: planet.serialize(), planets))
        return planets
    
    def delete_planet(id):
        planet = Planet.query.get(id)
        db.session.delete(planet)
        db.session.commit()


class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('my_favorite_list', lazy='dynamic'))
    people_id = db.Column(db.ForeignKey('people.id'))
    people = db.relationship('People', backref=db.backref('my_favorite_list', lazy='dynamic'))
    planet_id = db.Column(db.ForeignKey('planet.id'))
    planet = db.relationship('Planet', backref=db.backref('my_favorite_list', lazy='dynamic'))

    def serialize(self):
        return {
            "id": self.id,
            "user_add_favorite": User.serialize(self.user),
            "people_data": People.serialize(self.people),
            "planet_data": Planet.serialize(self.planet)
        }

    def create_favorite_people(people_id):
        favorite = Favorite(people_id=people_id)
        db.session.add(favorite)
        db.session.commit()

    def create_favorite_planet(planet_id):
        favorite = Favorite(planet_id=planet_id)
        db.session.add(favorite)
        db.session.commit()

    def get_all_favorites():
        favorites = Favorite.query.all()
        favorites = list(map(lambda favorite: favorite.serialize(), favorites))
        return favorites
    
    def get_favorite_people(people_id):
        favorite_people = People.query.filter_by(peopler_id=people_id)
        return favorite_people

    def get_favorite_planet(planet_id):
        favorite_planet = Planet.query.filter_by(planet_id=planet_id)
        return favorite_planet

    def delete_favorite_people(favorite_id, people_id):
        favorite = Favorite.query.get(favorite_id, people_id)
        db.session.delete(favorite)
        db.session.commit()

    def delete_favorite_planet(favorite_id, planet_id):
        favorite = Favorite.query.get(favorite_id, planet_id)
        db.session.delete(favorite)
        db.session.commit()
    