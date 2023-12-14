import xml.etree.ElementTree as ET

class Player:
    counter = 0

    def __init__(self, name, age, country, club, position, overall, pace, shooting, passing, dribbling, defending,
                 physicality, acceleration, sprint, positioning, finishing, shot, long, volleys, penalties, vision,
                 crossing, free, curve, agility, balance, reactions, ball, composure, interceptions, heading, defense,
                 standing, sliding, jumping, stamina, strength, aggression, att_work_rate, def_work_rate, preferred_foot,
                 weak_foot, skill_moves, url, gender, gk):
        Player.counter += 1
        self._id = Player.counter
        self._name = name
        self._age = age
        self._country = country
        self._club = club
        self._position = position
        self._overall = overall
        self._pace = pace
        self._shooting = shooting
        self._passing = passing
        self._dribbling = dribbling
        self._defending = defending
        self._physicality = physicality
        self._acceleration = acceleration
        self._sprint = sprint
        self._positioning = positioning
        self._finishing = finishing
        self._shot = shot
        self._long = long
        self._volleys = volleys
        self._penalties = penalties
        self._vision = vision
        self._crossing = crossing
        self._free = free
        self._curve = curve
        self._agility = agility
        self._balance = balance
        self._reactions = reactions
        self._ball = ball
        self._composure = composure
        self._interceptions = interceptions
        self._heading = heading
        self._defense = defense
        self._standing = standing
        self._sliding = sliding
        self._jumping = jumping
        self._stamina = stamina
        self._strength = strength
        self._aggression = aggression
        self._att_work_rate = att_work_rate
        self._def_work_rate = def_work_rate
        self._preferred_foot = preferred_foot
        self._weak_foot = weak_foot
        self._skill_moves = skill_moves
        self._url = url
        self._gender = gender
        self._gk = gk

    def to_xml(self):
        el = ET.Element("Player")
        el.set("id", str(self._id))
        el.set("name", self._name)
        el.set("age", str(self._age))
        el.set("country_ref", str(self._country.get_id()))  # Assuming get_id returns the country ID
        el.set("club", str(self._club))  # Convert club to string if necessary
        el.set("position", str(self._position))  # Convert position to string if necessary

        el.set("overall", str(self._overall))
        el.set("pace", str(self._pace))
        el.set("shooting", str(self._shooting))
        el.set("passing", str(self._passing))
        el.set("dribbling", str(self._dribbling))
        el.set("defending", str(self._defending))
        el.set("physicality", str(self._physicality))
        el.set("acceleration", str(self._acceleration))
        el.set("sprint", str(self._sprint))
        el.set("positioning", str(self._positioning))
        el.set("finishing", str(self._finishing))
        el.set("shot", str(self._shot))
        el.set("long", str(self._long))
        el.set("volleys", str(self._volleys))
        el.set("penalties", str(self._penalties))
        el.set("vision", str(self._vision))
        el.set("crossing", str(self._crossing))
        el.set("free", str(self._free))
        el.set("curve", str(self._curve))
        el.set("agility", str(self._agility))
        el.set("balance", str(self._balance))
        el.set("reactions", str(self._reactions))
        el.set("ball", str(self._ball))
        el.set("composure", str(self._composure))
        el.set("interceptions", str(self._interceptions))
        el.set("heading", str(self._heading))
        el.set("defense", str(self._defense))
        el.set("standing", str(self._standing))
        el.set("sliding", str(self._sliding))
        el.set("jumping", str(self._jumping))
        el.set("stamina", str(self._stamina))
        el.set("strength", str(self._strength))
        el.set("aggression", str(self._aggression))
        el.set("att_work_rate", str(self._att_work_rate))
        el.set("def_work_rate", str(self._def_work_rate))
        el.set("preferred_foot", str(self._preferred_foot))
        el.set("weak_foot", str(self._weak_foot))
        el.set("skill_moves", str(self._skill_moves))
        el.set("url", str(self._url))
        el.set("gender", str(self._gender))
        el.set("gk", str(self._gk))

        return el

    def __str__(self):
        return (
            f"Name: {self._name}, Age: {self._age}, Country: {self._country}, "
            f"Club: {self._club}, Position: {self._position}, "
            f"Overall: {self._overall}, Pace: {self._pace}, "
            f"Shooting: {self._shooting}, Passing: {self._passing}, "
            f"Dribbling: {self._dribbling}, Defending: {self._defending}, "
            f"Physicality: {self._physicality}, Acceleration: {self._acceleration}, "
            f"Sprint: {self._sprint}, Positioning: {self._positioning}, "
            f"Finishing: {self._finishing}, Shot: {self._shot}, "
            f"Long: {self._long}, Volleys: {self._volleys}, "
            f"Penalties: {self._penalties}, Vision: {self._vision}, "
            f"Crossing: {self._crossing}, Free: {self._free}, "
            f"Curve: {self._curve}, Agility: {self._agility}, "
            f"Balance: {self._balance}, Reactions: {self._reactions}, "
            f"Ball: {self._ball}, Composure: {self._composure}, "
            f"Interceptions: {self._interceptions}, Heading: {self._heading}, "
            f"Defense: {self._defense}, Standing: {self._standing}, "
            f"Sliding: {self._sliding}, Jumping: {self._jumping}, "
            f"Stamina: {self._stamina}, Strength: {self._strength}, "
            f"Aggression: {self._aggression}, Attacking Work Rate: {self._att_work_rate}, "
            f"Defensive Work Rate: {self._def_work_rate}, Preferred Foot: {self._preferred_foot}, "
            f"Weak Foot: {self._weak_foot}, Skill Moves: {self._skill_moves}, "
            f"URL: {self._url}, Gender: {self._gender}, GK: {self._gk}"
        )

