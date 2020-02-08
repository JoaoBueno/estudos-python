import sys
import re
import json
import math
import builtins
import collections
from collections import defaultdict

import unidecode

from app import options
from app.model import exceptions, db


class AllowedModule(list):

    excluded_attr = ('exec', 'eval')

    def __init__(self, module):
        self.name = module.__name__
        super().__init__(
            [attr for attr in dir(module) if attr not in self.excluded_attr])


MODULES = math, builtins
ALLOWED_MODULES = [AllowedModule(module) for module in MODULES]


class Parser:

    """
    Used to parse structure and calculation strings
    """

    property_re = re.compile(r'[^\W\d]+\.?[\w\_\'"]*', re.UNICODE)
    module_str = '{}.{}'
    get_str = 'self._get("{}")'
    self_str = 'self.set("{}", {})'

    @staticmethod
    def _escape_value(value):
        return value.lower().replace(' ', '')

    @classmethod
    def unidecode(cls, value):
        return unidecode.unidecode(cls._escape_value(value)).replace('\'', '')

    @classmethod
    def parse_calculation_string(cls, name, string):
        out = []
        i = 0

        for match in cls.property_re.finditer(string):
            begin, end = match.span()
            group = match.group()

            for module in ALLOWED_MODULES:
                if group in module:
                    group = cls.module_str.format(module.name, group)
                    break
            else:
                group = cls.get_str.format(group)

            out.append(''.join((string[i:begin], group)))
            i = end
        else:
            out.append(string[i:])

        expr = ''.join([chunk for chunk in out])
        return cls.self_str.format(name, expr)

    @classmethod
    def parse_structure(cls, structure):

        structure = cls.unidecode(structure)

        try:
            structure = json.loads(structure)
        except ValueError:
            raise exceptions.BadStructure()
            sys.exit()

        return structure


class Mediator:

    """
    Sort of implementation of 'Mediator' pattern.
    Provides access to other objects attributes.
    Also its Singleton and i'm not sure if you're ok with that.
    """

    __instance = None

    def __new__(cls, obj=None):
        if cls.__instance is None:
            cls.__instance = super(cls, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):

        if self.__initialized:
            return

        self.objects = {}
        self.__initialized = True

    def __call__(self, obj):
        self.objects[obj.name] = obj
        return self

    def __str__(self):
        return 'Mediator. Watch objects: [{}]'.format(', '.join(self.objects.keys()))

    def _get_value(self, name):
        for obj in self.objects:
            try:
                return obj[name]
            except KeyError:
                continue

        raise AttributeError('Name {} was not found in objects'.format(name))

    def get(self, key):
        try:
            obj_name, name = key.split('.')
        except IndexError:
            name = key
        else:
            return self.objects[obj_name][name]

        return self._get_value(name)


class CalculableObject(collections.OrderedDict):

    calculation_divider = ';\n'

    def __init__(self, name, verbose_name, group, args, parser, mediator, model=None, item=None):
        super().__init__()

        self.types = self._create_types(args)
        self.name = name
        self.verbose_name = verbose_name
        self.group = group
        self.mediator = mediator(self)
        self.model = model
        self.calculations = []
        self.template = None
        if item:
            self.id = item.id

        for each in args:
            self[each['name']] = self.types[each['name']]()
            calculation = each.get('calculation')
            if calculation:
                self.calculations.append(
                    parser.parse_calculation_string(each['name'], calculation))

        self.calculations = self.calculation_divider.join(self.calculations)

    def __str__(self):
        return '{}: [{}]'.format(self.name, ', '.join(self.keys()))

    def _get(self, name):
        try:
            value = self[name]
        except KeyError:
            value = self.mediator.get(name)

        return value

    def _create_types(self, args):
        types = options.TYPES

        return {each['name']: types.get(each.get('type', 'float'), float)
                for each in args}

    def _add_calculation(self, name, calculation):
        pass

    def set(self, name, value):
        """
        If value is fucked up it will be set to default for it's type.
        float -> 0.0
        str -> ''
        """
        if self.get(name) is None:
            raise AttributeError('No such attribute: {}'.format(name))

        type_ = self.types[name]

        try:
            value = type_(value)
        except ValueError:
            value = type_()

        if type_ is float:
            if value == int(value):
                value = int(value)
            else:
                value = round(value, 2)

        self[name] = value

    def clean(self):
        for k in self.keys():
            self.set(k, '')
        self.template = None

    def get_verbose_name(self):
        return _(self.verbose_name)

    def calculate(self):
        for calc in self.calculations.split(self.calculation_divider):
            try:
                exec(calc)
            except ZeroDivisionError:
                pass

    def for_template(self):
        out = {
            self.name: defaultdict(str)
        }

        for key, value in self.items():
            out[self.name][key] = value
        return out


class ObjectFactory:

    model_factory = db.ModelFactory()

    @classmethod
    def get_object(cls, info):

        model = None
        group, _ = db.Group.get_or_create(name=info.get('group', info['name']), instant_flush=True)
        item, _ = db.Item.get_or_create(name=info['name'], group=group, instant_flush=True)

        if info.get('db'):
            model = cls.model_factory.get_model(info)

        return CalculableObject(name=info['name'],
                                verbose_name=info.get('verbose_name', info['name']),
                                args=info['args'],
                                group=info.get('group', info['name']),
                                parser=Parser(),
                                mediator=Mediator(),
                                model=model,
                                item=item)
