import xmltodict
import pprint
import json

my_xml = """
    <audience>
      <id what="attribute">123</id>
      <name>Shubham</name>
    </audience>
"""
my_dict = xmltodict.parse(my_xml)
print(my_dict)
#OrderedDict([('audience', OrderedDict([('id', OrderedDict([('@what', 'attribute'), ('#text', '123')])), ('name', 'Shubham')]))])
print(my_dict['audience']['id'])
#OrderedDict([('@what', 'attribute'), ('#text', '123')])
print(my_dict['audience']['id']['@what'])
#attribute
print(my_dict)
#OrderedDict([('audience', OrderedDict([('id', OrderedDict([('@what', 'attribute'), ('#text', '123')])), ('name', 'Shubham')]))])
