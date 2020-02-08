import os
import datetime
import re
import json
from collections import defaultdict

from app.model import db, exceptions


class Template:

    def __init__(self, pk=None, item=None, items=None, name=None, body=None, conclusion=None):

        """
        Parameter items is needed
        because template for one particular item
        can contain keywords from another items.
        And parameter item is needed too,
        because template needs to know for what item it is saved.
        """

        self.pk = pk
        self.item = item
        self.items = items
        self.name = name
        self.body = body
        self.conclusion = conclusion

    def __str__(self):
        return 'Template "{}"'.format(self.name)

    def save(self):

        if not (self.item and self.name):
            raise exceptions.CannotSaveTemplate

        if not (self.body or self.conclusion):
            raise exceptions.NeedBodyOrConclusion

        if self.pk:
            template = db.SESSION.query(db.Template).get(self.pk)
        else:
            template = db.Template()

        template.item_id = self.item.id
        template.name = self.name
        template.body = self.body
        template.conclusion = self.conclusion
        template.save()
        self.pk = template.id

    def get_translated_body(self, reverse=False):
        """
        This is bad function.
        """
        
        regex = {}
        translation = {}

        if reverse:
            for each in self.items:
                for k in each.keys():
                    regex[r'{%s.%s}' % (_(each.name), _(k))] = r'{%s[%s]}' % (each.name, k)
                    translation = regex
        else:
            for each in self.items:
                for k in each.keys():
                    regex[r'{%s\[%s\]}' % (each.name, k)] = r'{%s.%s}' % (_(each.name), _(k))
                    translation[r'{%s[%s]}' % (each.name, k)] = r'{%s.%s}' % (_(each.name), _(k))

        pattern = re.compile(r'(' + '|'.join(regex.keys()) + r')')
        return pattern.sub(lambda x: translation[x.group()], self.body)

    def render_and_save(self):
        self.body = self.get_translated_body(reverse=True)
        self.save()

    @classmethod
    def get_from_db(cls, item, items, name):

        template = db.SESSION.query(db.Template).filter(
            db.Template.item_id == item.id, db.Template.name == name).first()

        return cls(pk=template.id,
                   item=item,
                   items=items,
                   name=name,
                   body=template.body,
                   conclusion=template.conclusion)

    @classmethod
    def get_all(cls):

        result = defaultdict(list)
        templates = db.SESSION.query(db.Template).all()

        for each in templates:
            result[each.item.id].append(each)

        return result

    @classmethod
    def export(cls, path):
        """
        Export all templates into JSON.
        :return
        bool status
        dict templates in json or error message
        """

        path = os.path.join(path, 'hh_tmplts_{}.json'.format(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')))

        templates = [t.to_dict(relations={'item': {}})
                     for t in db.SESSION.query(db.Template).join(db.Template.item).all()]

        if not templates:
            return False, {'error': 'No templates to export'}

        try:
            templates = json.dumps(templates, ensure_ascii=False)
        except (ValueError, TypeError) as e:
            return False, {'error': str(e)}

        try:
            with open(path, 'wb') as f:
                f.write(templates.encode('utf8'))
        except IOError as e:
            return False, {'error': str(e)}

        return True, {'result': templates}

    @classmethod
    def import_(cls, path):
        """
        Import templates from JSON file.
        Warning: Existed templates with similar names will be overwritten.
        :return
        bool status
        dict result
        """

        replaced_key = 'replaced'
        created_key = 'created'
        failed_key = 'fail'
        result = {
            replaced_key: defaultdict(list),
            created_key: defaultdict(list),
            failed_key: list()
        }

        templates_to_update = []

        try:
            with open(path, 'rb') as f:
                templates = json.loads(f.read().decode('utf8'))
        except (IOError, TypeError, ValueError) as e:
            return False, {'error': str(e)}

        for each in templates:
            item = db.SESSION.query(db.Item).filter(db.Item.name == each['item']['name']).first()
            if not item:
                result[failed_key].append('Item {} was not found'.format(_(each['item']['name'])))

            result_key = replaced_key
            template = db.SESSION.query(db.Template).filter(db.Template.item_id == item.id,
                                                            db.Template.name == each['name']).first()

            if not template:
                result_key = created_key
                template = db.Template()

            for k, v in each.items():
                if k == 'id' or isinstance(v, dict):
                    continue
                setattr(template, k, v)

            templates_to_update.append(template)
            result[result_key][item.name].append(template.name)

        db.SESSION.bulk_save_objects(templates_to_update)
        db.SESSION.flush()
        return True, result
