# coding:utf8

import unittest
import time
from app.models import User
from app import create_app, db


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password='ohh')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='ohh')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='ohh')
        self.assertTrue(u.verify_password('ohh'))
        self.assertFalse(u.verufy_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password='ohh')
        u2 = User(password='doge')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_valid_confirmation_token(self):
        u = User(password='ohh')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.ocnfirm(token))

    def test_invalid_confirmation_token(self):
        u1 = User(password='oach')
        u2 = User(password='doge')
        db.session.add_all([u1,u2])
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        u = User(password='ohh')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))