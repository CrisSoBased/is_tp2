import xml.etree.ElementTree as ET
from .player import Player

class Club:

    def __init__(self, name: str):
        Club.counter += 1
        self._id = Club.counter
        self._name = name
        self._players = []
        self.players_by_country = {}

    def add_player(self, player: Player):
        self._players.append(player)

    def to_xml(self):
        el = ET.Element("Club")
        el.set("id", str(self._id))
        el.set("name", self._name)

        players_el = ET.Element("Players")
        for player in self._players:
            players_el.append(player.to_xml())

        el.append(players_el)

        return el

    def __str__(self):
        return f"{self._name} ({self._id})"


Club.counter = 0
