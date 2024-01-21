import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import magql
from flask_magql import MagqlExtension
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func
from geoalchemy2 import Geometry
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://is:is@db-rel/is'  # Configuração para PostgreSQL
db = SQLAlchemy(app)

# Defina suas classes de modelo (Nation, Club, Player)
class Nation(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v5(func.uuid_ns_dns(), 'nation'))
    name = db.Column(db.String(255), nullable=False)
    coordinates = db.Column(Geometry('POINT', srid=4326))
    created_on = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())
    updated_on = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())

class Club(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v5(func.uuid_ns_dns(), 'club'))
    name = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())
    updated_on = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())

class Player(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v5(func.uuid_ns_dns(), 'player'))
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(INTEGER, nullable=False)
    overall = db.Column(INTEGER, nullable=False)
    position = db.Column(db.String(50), nullable=False)
    pace = db.Column(INTEGER, nullable=False)
    shooting = db.Column(INTEGER, nullable=False)
    passing = db.Column(INTEGER, nullable=False)
    dribbling = db.Column(INTEGER, nullable=False)
    defending = db.Column(INTEGER, nullable=False)
    physicality = db.Column(INTEGER, nullable=False)
    acceleration = db.Column(INTEGER, nullable=False)
    sprint = db.Column(INTEGER, nullable=False)
    positioning = db.Column(INTEGER, nullable=False)
    finishing = db.Column(INTEGER, nullable=False)
    shot = db.Column(INTEGER, nullable=False)
    long = db.Column(INTEGER, nullable=False)
    volleys = db.Column(INTEGER, nullable=False)
    penalties = db.Column(INTEGER, nullable=False)
    vision = db.Column(INTEGER, nullable=False)
    crossing = db.Column(INTEGER, nullable=False)
    free = db.Column(INTEGER, nullable=False)
    curve = db.Column(INTEGER, nullable=False)
    agility = db.Column(INTEGER, nullable=False)
    balance = db.Column(INTEGER, nullable=False)
    reactions = db.Column(INTEGER, nullable=False)
    ball = db.Column(INTEGER, nullable=False)
    composure = db.Column(INTEGER, nullable=False)
    interceptions = db.Column(INTEGER, nullable=False)
    heading = db.Column(INTEGER, nullable=False)
    defense = db.Column(INTEGER, nullable=False)
    standing = db.Column(INTEGER, nullable=False)
    sliding = db.Column(INTEGER, nullable=False)
    jumping = db.Column(INTEGER, nullable=False)
    stamina = db.Column(INTEGER, nullable=False)
    strength = db.Column(INTEGER, nullable=False)
    aggression = db.Column(INTEGER, nullable=False)
    att_work_rate = db.Column(db.String(50), nullable=False)
    def_work_rate = db.Column(db.String(50), nullable=False)
    preferred_foot = db.Column(db.String(10), nullable=False)
    weak_foot = db.Column(INTEGER, nullable=False)
    skill_moves = db.Column(INTEGER, nullable=False)
    url = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    gk = db.Column(INTEGER)
    id_nation = db.Column(UUID(as_uuid=True), db.ForeignKey('nation.id', ondelete='CASCADE'), nullable=False)
    id_club = db.Column(UUID(as_uuid=True), db.ForeignKey('club.id', ondelete='CASCADE'), nullable=False)
    nation_coordinates = db.Column(Geometry('POINT', srid=4326))
    created_on = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())
    updated_on = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())

# Crie o esquema GraphQL depois de definir as classes de modelo
schema = magql.Schema()

# Adicione os tipos 'Club', 'Nation', e 'Player' ao esquema
schema.add_type(Nation)
schema.add_type(Club)
schema.add_type(Player)

@schema.query.field(
    "greet", "String!", args={"name": magql.Argument("String!", default="World")}
)
def resolve_greet(parent, info, **kwargs):
    name = kwargs.pop("name")
    return f"Hello, {name}!"

@schema.query.field("get_nations", "[Nation]")
def resolve_get_nations(parent, info):
    return Nation.query.all()

@schema.query.field("get_clubs", "[Club]")
def resolve_get_clubs(parent, info):
    return Club.query.all()

@schema.query.field("get_players", "[Player]")
def resolve_get_players(parent, info):
    return Player.query.all()

magql_ext = MagqlExtension(schema)
app.config["DEBUG"] = True
magql_ext.init_app(app)
app.run(host="0.0.0.0", port=sys.argv[1])