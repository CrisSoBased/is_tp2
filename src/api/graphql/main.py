from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_magql import MagGraphQLView
from marshmallow_sqlalchemy import ModelSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://is:is@db-rel/is'
db = SQLAlchemy(app)

class Nation(db.Model):
    __tablename__ = 'nation'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    coordinates = db.Column(db.String)
    created_on = db.Column(db.TIMESTAMP, nullable=False)
    updated_on = db.Column(db.TIMESTAMP, nullable=False)

class Club(db.Model):
    __tablename__ = 'club'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.TIMESTAMP, nullable=False)
    updated_on = db.Column(db.TIMESTAMP, nullable=False)

class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    overall = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String(50), nullable=False)
    pace = db.Column(db.Integer, nullable=False)
    shooting = db.Column(db.Integer, nullable=False)
    passing = db.Column(db.Integer, nullable=False)
    dribbling = db.Column(db.Integer, nullable=False)
    defending = db.Column(db.Integer, nullable=False)
    physicality = db.Column(db.Integer, nullable=False)
    acceleration = db.Column(db.Integer, nullable=False)
    sprint = db.Column(db.Integer, nullable=False)
    positioning = db.Column(db.Integer, nullable=False)
    finishing = db.Column(db.Integer, nullable=False)
    shot = db.Column(db.Integer, nullable=False)
    long = db.Column(db.Integer, nullable=False)
    volleys = db.Column(db.Integer, nullable=False)
    penalties = db.Column(db.Integer, nullable=False)
    vision = db.Column(db.Integer, nullable=False)
    crossing = db.Column(db.Integer, nullable=False)
    free = db.Column(db.Integer, nullable=False)
    curve = db.Column(db.Integer, nullable=False)
    agility = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    reactions = db.Column(db.Integer, nullable=False)
    ball = db.Column(db.Integer, nullable=False)
    composure = db.Column(db.Integer, nullable=False)
    interceptions = db.Column(db.Integer, nullable=False)
    heading = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    standing = db.Column(db.Integer, nullable=False)
    sliding = db.Column(db.Integer, nullable=False)
    jumping = db.Column(db.Integer, nullable=False)
    stamina = db.Column(db.Integer, nullable=False)
    strength = db.Column(db.Integer, nullable=False)
    aggression = db.Column(db.Integer, nullable=False)
    att_work_rate = db.Column(db.String(50), nullable=False)
    def_work_rate = db.Column(db.String(50), nullable=False)
    preferred_foot = db.Column(db.String(10), nullable=False)
    weak_foot = db.Column(db.Integer, nullable=False)
    skill_moves = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    gk = db.Column(db.Integer)
    id_nation = db.Column(db.String, db.ForeignKey('nation.id'), nullable=False)
    id_club = db.Column(db.String, db.ForeignKey('club.id'), nullable=False)
    nation_coordinates = db.Column(db.String)
    created_on = db.Column(db.TIMESTAMP, nullable=False)
    updated_on = db.Column(db.TIMESTAMP, nullable=False)

class NationSchema(ModelSchema):
    class Meta:
        model = Nation

class ClubSchema(ModelSchema):
    class Meta:
        model = Club

class PlayerSchema(ModelSchema):
    class Meta:
        model = Player


class Query:
    def fetch_clubs(self):
        return Club.query.all()

    def fetch_all_players_from_portugal(self, nation_name):
        nation = Nation.query.filter_by(name=nation_name).first()
        if nation:
            return Player.query.filter_by(id_nation=nation.id).all()
        else:
            return []

    def fetch_all_players_CM_from_france(self, nation_name):
        nation = Nation.query.filter_by(name=nation_name).first()
        if nation:
            return Player.query.filter_by(position='CM', id_nation=nation.id).all()
        else:
            return []

    def fetch_all_players_by_nation(self, nation_name):
        nation = Nation.query.filter_by(name=nation_name).first()
        if nation:
            return Player.query.filter_by(id_nation=nation.id).all()
        else:
            return []


app.add_url_rule('/graphql', view_func=MagGraphQLView.as_view('graphql', schema=Query, graphiql=True))

if __name__ == '__main__':
    app.run(debug=True)
