CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS POSTGIS;
CREATE EXTENSION IF NOT EXISTS POSTGIS_TOPOLOGY;

CREATE TABLE public.player (
    
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            VARCHAR(255) NOT NULL,
    nation          VARCHAR(255) NOT NULL,
    club            VARCHAR(255) NOT NULL,
    position        VARCHAR(50) NOT NULL,
    age             INTEGER NOT NULL,
    overall         INTEGER NOT NULL,
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
	id_nation		uuid NOT NULL,
	id_club			uuid NOT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.club (
    id         		uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome       		VARCHAR(255) NOT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.nation (
    id uuid			PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome			VARCHAR(255) NOT NULL,
    geom 			GEOMETRY,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);




ALTER TABLE player
    ADD CONSTRAINT player_nation_id_fk
        FOREIGN KEY (id_nation) REFERENCES nation
            ON DELETE CASCADE;

ALTER TABLE player
    ADD CONSTRAINT player_club_id_fk
        FOREIGN KEY (id_club) REFERENCES club
            ON DELETE SET NULL;


