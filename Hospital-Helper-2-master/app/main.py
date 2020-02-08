import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.gui import main as gui
from app.model import db, logic, exceptions, localization


def convert_structure_to_items(structure):
    parser = logic.Parser()
    object_factory = logic.ObjectFactory

    parsed_structure = parser.parse_structure(structure)

    items = []
    names = set()
    for i, item in enumerate(parsed_structure, 1):

        names.add(item['name'])
        items.append(object_factory.get_object(item))
        if i != len(names):
            raise exceptions.NonUniqueObjectNames(item['name'])

    return items


def init():

    structure = db.create_db()
    items = convert_structure_to_items(structure)
    # localization.Localization.install('ru')
    localization.Localization.install('en')

    return items


if __name__ == '__main__':
    gui.init(init)
