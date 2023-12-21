import xml.etree.ElementTree as ET

class Nation:
    counter = 0

    def __init__(self, name):
        Nation.counter += 1
        self._id = Nation.counter
        self._name = name

    def to_xml(self):
        
        el = ET.Element("Nation")
        el.set("id", str(self._id))
        el.set("name", self._name)
        return el
    
    def get_name(self):
        return self._name

    def get_id(self):
        return self._id

    def __str__(self):
        return f"name: {self._name}, id: {self._id}"
