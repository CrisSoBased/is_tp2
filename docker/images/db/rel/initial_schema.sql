-- Criar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS postgis;

-- Tabela para as Nações
CREATE TABLE public.Nation (
    id          uuid PRIMARY KEY DEFAULT uuid_generate_v5(uuid_ns_dns(), 'nation'),
    name        VARCHAR(255) NOT NULL UNIQUE,
    coordinates GEOMETRY(Point, 4326), -- Coordenadas geográficas (latitude e longitude)
    created_on  TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_on  TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Tabela para os Clubes
CREATE TABLE public.Club (
    id          uuid PRIMARY KEY DEFAULT uuid_generate_v5(uuid_ns_dns(), 'club'),
    name        VARCHAR(255) NOT NULL UNIQUE,
    created_on  TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_on  TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Tabela para os Jogadores
CREATE TABLE public.Player (
    id              uuid PRIMARY KEY DEFAULT uuid_generate_v5(uuid_ns_dns(), 'player'),
    name            VARCHAR(255) NOT NULL UNIQUE,
    age             INTEGER NOT NULL,
    overall         INTEGER NOT NULL,
    position        VARCHAR(50) NOT NULL,
    pace            INTEGER NOT NULL,
    shooting        INTEGER NOT NULL,
    passing         INTEGER NOT NULL,
    dribbling       INTEGER NOT NULL,
    defending       INTEGER NOT NULL,
    physicality     INTEGER NOT NULL,
    acceleration    INTEGER NOT NULL,
    sprint          INTEGER NOT NULL,
    positioning     INTEGER NOT NULL,
    finishing       INTEGER NOT NULL,
    shot            INTEGER NOT NULL,
    long            INTEGER NOT NULL,
    volleys         INTEGER NOT NULL,
    penalties       INTEGER NOT NULL,
    vision          INTEGER NOT NULL,
    crossing        INTEGER NOT NULL,
    free            INTEGER NOT NULL,
    curve           INTEGER NOT NULL,
    agility         INTEGER NOT NULL,
    balance         INTEGER NOT NULL,
    reactions       INTEGER NOT NULL,
    ball            INTEGER NOT NULL,
    composure       INTEGER NOT NULL,
    interceptions   INTEGER NOT NULL,
    heading         INTEGER NOT NULL,
    def             INTEGER NOT NULL,
    standing        INTEGER NOT NULL,
    sliding         INTEGER NOT NULL,
    jumping         INTEGER NOT NULL,
    stamina         INTEGER NOT NULL,
    strength        INTEGER NOT NULL,
    aggression      INTEGER NOT NULL,
    att_work_rate   VARCHAR(50) NOT NULL,
    def_work_rate   VARCHAR(50) NOT NULL,
    preferred_foot  VARCHAR(10) NOT NULL,
    weak_foot       INTEGER NOT NULL,
    skill_moves     INTEGER NOT NULL,
    url             VARCHAR(255) NOT NULL,
    gender          VARCHAR(10) NOT NULL,
    gk              INTEGER,
    id_nation       uuid REFERENCES Nation(id) ON DELETE CASCADE,
    id_club         uuid REFERENCES Club(id) ON DELETE CASCADE,
    nation_coordinates GEOMETRY(Point, 4326), -- Coordenadas geográficas da nação do jogador
    created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);


