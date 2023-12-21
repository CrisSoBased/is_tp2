import csv
import xml.dom.minidom as md
import xml.etree.ElementTree as ET
import urllib3
import requests
from utils.reader import CSVReader
from entities.nation import Nation
from entities.club import Club
from entities.player import Player


class CSVtoXMLConverter:

    def __init__(self, path):
        self._reader = CSVReader(path)

    def get_data(self, nation):

        address = nation
        url = 'https://nominatim.openstreetmap.org/search/' + urllib3.parse.quote(address) + '?format=json'

        coordinates = requests.get(url).json()

        return [
            coordinates[0]["lat"],
            coordinates[0]["lon"]
        ]


    def to_xml(self):
        # read countries
        nations = self._reader.read_entities(
            attr="Nation",
            builder=lambda row: Nation(row["Nation"])
        )

        # read teams
        clubs = self._reader.read_entities(
            attr="Club",
            builder=lambda row: Club(row["Club"])
        )

        # read players

        def after_creating_player(player, row):
            # add the player to the appropriate team
            club = clubs[row["Club"]]
            nation = nations[row["Nation"]]

            if nation not in club.players_by_nation:
                club.players_by_nation[nation] = []

            club.players_by_nation[nation].append(player)

        self._reader.read_entities(
            attr="Name",
            builder=lambda row: Player(
                name=row["Name"],
                age=row["Age"],
                country=nations[row["Nation"]],
                club=clubs[row["Club"]],
                position=row["Position"],
                overall=row["Overall"],
                pace=row["Pace"],
                shooting=row["Shooting"],
                passing=row["Passing"],
                dribbling=row["Dribbling"],
                defending=row["Defending"],
                physicality=row["Physicality"],
                acceleration=row["Acceleration"],
                sprint=row["Sprint"],
                positioning=row["Positioning"],
                finishing=row["Finishing"],
                shot=row["Shot"],
                long=row["Long"],
                volleys=row["Volleys"],
                penalties=row["Penalties"],
                vision=row["Vision"],
                crossing=row["Crossing"],
                free=row["Free"],
                curve=row["Curve"],
                agility=row["Agility"],
                balance=row["Balance"],
                reactions=row["Reactions"],
                ball=row["Ball"],
                composure=row["Composure"],
                interceptions=row["Interceptions"],
                heading=row["Heading"],
                defense=row["Def"],
                standing=row["Standing"],
                sliding=row["Sliding"],
                jumping=row["Jumping"],
                stamina=row["Stamina"],
                strength=row["Strength"],
                aggression=row["Aggression"],
                att_work_rate=row["Att work rate"],
                def_work_rate=row["Def work rate"],
                preferred_foot=row["Preferred foot"],
                weak_foot=row["Weak foot"],
                skill_moves=row["Skill moves"],
                url=row["URL"],
                gender=row["Gender"],
                gk=row["GK"]
            ),
            after_create=after_creating_player
        )

        # generate the final xml
        for nation in nations.values():
            coordinates = self.get_data(nation.get_name())

        root_el = ET.Element("Football")

        clubs_el = ET.Element("Clubs")
        for club in clubs.values():
            club_el = ET.SubElement(clubs_el, "Club", name=club._name)
            nation_el = ET.SubElement(club_el, "Nations")

            for nation, players in club.players_by_country.items():
                nation_el = ET.SubElement(nation_el, "Nation", name=nation.get_name(), Coordenadas=f"{coordinates[0]}, {coordinates[1]}")
                players_el = ET.SubElement(nation_el, "Players")

                for player in players:
                    players_el.append(player.to_xml())
        
        root_el.append(clubs_el)

        # Crie uma instância ElementTree para lidar com a serialização
        tree = ET.ElementTree(root_el)

        return tree

    def to_xml_str(self):
        xml_str = ET.tostring(self.to_xml(), encoding='utf8', method='xml').decode()
        dom = md.parseString(xml_str)
        return dom.toprettyxml()

