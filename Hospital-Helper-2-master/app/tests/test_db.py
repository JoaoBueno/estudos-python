import unittest

from sqlalchemy import exc
from sqlalchemy.orm import exc as orm_exc

from app.model import db


class TestModel(unittest.TestCase):
    user_args = {
        'surname': 'Test',
        'name': 'Test Name',
        'patronymic': 'Test'
    }

    def _clean_db(self):
        for t in db.Base.metadata.tables:
            db.SESSION.execute('delete from "{}";'.format(t))

    def setUp(self):
        self.organization = db.Organization(name='test', header='')
        self.organization.save()

        self.user = db.User(organization=self.organization, **self.user_args)
        self.user.save()

    def test_get(self):
        with self.assertRaises(orm_exc.NoResultFound):
            db.Template.get(id=1)

        user = db.User.get(id=self.user.id)
        self.assertEqual(user, self.user)

        with self.assertRaises(orm_exc.NoResultFound):
            db.User.get(name='garbage')

        db.User(organization=self.organization, **self.user_args).save()
        with self.assertRaises(orm_exc.MultipleResultsFound):
            db.User.get(name=self.user_args['name'])

    def test_get_or_create(self):
        for _ in range(3):
            db.User(organization=self.organization, **self.user_args).save()

        with self.assertRaises(orm_exc.MultipleResultsFound):
            db.User.get_or_create(name=self.user_args['name'])

        args = {
            'organization': self.organization,
            'name': 1,
            'surname': 2,
            'patronymic': 3
        }

        user, created = db.User.get_or_create(instant_flush=True, defaults={'name': 2}, **args)
        self.assertEqual(created, True)
        self.assertEqual(db.User.get(id=user.id).name, 2)

        user, created = db.User.get_or_create(**args)
        self.assertEqual(created, True)

        user, created = db.User.get_or_create(**args)
        self.assertEqual(created, False)

    def test_to_dict(self):
        dict_user = self.user.to_dict()
        expected_dict = {
            'id': 1,
            'organization_id': 1,
            'surname': 'Test',
            'deleted': False,
            'name': 'Test Name',
            'patronymic': 'Test'
        }
        self.assertEqual(dict_user, expected_dict)

        expected_dict['organization'] = self.user.organization.to_dict()
        dict_user = self.user.to_dict(relations={'organization': {}})
        self.assertEqual(dict_user, expected_dict)

        with self.assertRaises(exc.NoForeignKeysError):
            self.user.to_dict(relations={'hello': {}})

        with self.assertRaises(exc.NoForeignKeysError):
            self.user.to_dict(relations={'organization': {'no': {}}})

    def test_update(self):
        args = {
            'name': 'Hello',
            'patronymic': 'There'
        }

        self.user.update(**args)
        for k, v in args.items():
            self.assertEqual(getattr(self.user, k), v)

    def test_save(self):
        name = 'New Name'
        self.user.name = name
        self.user.save()
        self.assertEqual(db.User.get(id=self.user.id).name, name)

    def test_delete(self):
        self.user.delete()
        with self.assertRaises(orm_exc.NoResultFound):
            db.User.get(id=self.user.id)

    def test_create_db(self):
        structure = db.create_db()
        self.assertIsInstance(structure, str)

    def tearDown(self):
        self._clean_db()
