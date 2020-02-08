import json

from app import options
from app.model import db, logic, exceptions


class Localization:

    __translation = {}
    __lang = None

    @classmethod
    def install(cls, lang):

        cls.__lang = lang

        if lang not in [c.name for c in db.Translation.__table__.columns]:
            raise exceptions.NoSuchTranslation

        cls.create_init_translation()

        strings = db.SESSION.query(db.Translation).all()

        for s in strings:
            transl = getattr(s, lang)
            cls.__translation[s.sys] = transl

        import builtins
        builtins.__dict__['_'] = cls.get_text

    @classmethod
    def get_translation_map(cls, labels):
        translation = {}
        strings = db.SESSION.query(db.Translation).all()
        for l in labels:
            for s in strings:
                if s.sys == l:
                    translation[l] = getattr(l, cls.__lang)
                    break
        return translation

    @classmethod
    def get_text(cls, text):
        return cls.__translation.get(text, text)

    @staticmethod
    def add_system_label(label):

        t, _ = db.Translation.get_or_create(sys=logic.Parser.unidecode(label),
                                            defaults={
            'ru': label.replace('_', ' ').lstrip(),
            'en': label.replace('_', ' ').lstrip()
        })

        db.SESSION.add(t)

    @classmethod
    def create_init_translation(cls):

        structure = db.SESSION.query(db.KeyValue).filter(
            db.KeyValue.key == options.STRUCTURE_KEY).first()

        try:
            structure = json.loads(structure.value)
        except AttributeError:
            raise exceptions.AppNotReady

        for item in structure:
            for arg in item['args']:
                cls.add_system_label(arg['name'])

            for l in ('group', 'name', 'verbose_name'):
                s = item.get(l)
                if s:
                    cls.add_system_label(s)

        for each in options.TRANSLATION + options.CONTROL_BUTTONS_LABELS:
            db.Translation.get_or_create(**each)
