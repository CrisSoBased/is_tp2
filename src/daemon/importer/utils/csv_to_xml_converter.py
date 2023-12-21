import csv
import xml.dom.minidom as md
import xml.etree.ElementTree as ET

from utils.reader import CSVReader
from entities.nation import Nation
from entities.club import Club
from entities.player import Player
from entities.country import Country
from lxml import etree

class CSVtoXMLConverter:

    def __init__(self, path):
        self._reader = CSVReader(path)

    def to_xml(self):
        # read countries
        countries = self._reader.read_entities(
            attr="Nation",
            builder=lambda row: Nation(row["Nation"])
        )

        # read clubs
        clubs = self._reader.read_entities(
            attr="Club",
            builder=lambda row: Club(row["Club"])
        )

        #read players
        def after_creating_player(player, row):
            # add the player to the appropriate team
            #clubs[row["Club"]].add_player(player)
            club = clubs[row["Club"]]
            country = countries[row["Nation"]]

            if country not in club.players_by_country:
                club.players_by_country[country] = []

            club.players_by_country[country].append(player)

        self._reader.read_entities(
            attr="Name",
            builder=lambda row: Player(
                name=row["Name"],
                age=row["Age"],
                country=countries[row["Nation"]],
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
        for country in countries.values():
            coordinates = country.get_geoloc(country.get_name())
            country.set_geoloc(coordinates[0], coordinates[1])
                        
        root_el = ET.Element("Football")

        clubs_el = ET.Element("Clubs")
        for club in clubs.values():
            club_el = ET.SubElement(clubs_el, "Club", name=club._name)
            countries_el = ET.SubElement(club_el, "Countries")

            for country, players in club.players_by_country.items():
                country_el = ET.SubElement(countries_el, "Country", name=country.get_name(), Coordenadas=f"{country._lat}, {country._lon}")
                players_el = ET.SubElement(country_el, "Players")

                for player in players:
                    players_el.append(player.to_xml())

        root_el.append(clubs_el)

        # Crie uma instância ElementTree para lidar com a serialização
        tree = ET.ElementTree(root_el)

        return tree
    """
    def to_xml_str(self):
        xml_str = ET.tostring(self.to_xml(), encoding='utf-8', method='xml').decode()
        dom = md.parseString(xml_str)
        return dom.toprettyxml()
    """
    def to_xml_str(self, file_path=None, xsd_path=None):
        xml_tree = self.to_xml()

        xml_str = ET.tostring(xml_tree.getroot(), encoding='utf-8', method='xml').decode()
        dom = md.parseString(xml_str)

        if xsd_path:
            try:
                xml_str = dom.toprettyxml()
                if self.validate_xml_with_xsd(xml_str, xsd_path):
                    if file_path:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(xml_str)

                    success_message = f"\n!! Validation successfully made !!"
                    print(success_message)
                    return xml_str
                else:
                    error_message = "\n!! Validation failed. XML won't be generated !!"
                    print(error_message)
                    return None, error_message
            except etree.DocumentInvalid as e:
                print(f"\nError during XSD validation: {e}")
                return None, str(e)
        else:
            return dom.toprettyxml(), None


    def validate_xml_with_xsd(self, xml_str, xsd_file):
        try:
            xsd_tree = etree.parse(xsd_file)
            schema = etree.XMLSchema(xsd_tree)
            xml_doc = etree.fromstring(xml_str)
            schema.assertValid(xml_doc)
            return True
        except etree.DocumentInvalid as e:
            print(f"\nValidation error: {e}!")
            return False