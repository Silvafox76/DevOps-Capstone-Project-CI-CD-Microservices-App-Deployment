"""
Test cases for Account Model
"""
import logging
import unittest
import os
from service import app
from service.models import Account, DataValidationError, db
from tests.factories import AccountFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  Account   M O D E L   T E S T   C A S E S
######################################################################
class TestAccount(unittest.TestCase):
    """Test Cases for Account Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Account.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""

    def setUp(self):
        """This runs before each test"""
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    def test_create_an_account(self):
        """It should Create an Account and assert that it exists"""
        fake_account = AccountFactory()
        account = Account(
            name=fake_account.name,
            email=fake_account.email,
            address=fake_account.address,
            phone_number=fake_account.phone_number,
            date_joined=fake_account.date_joined,
        )
        self.assertIsNotNone(account)
        self.assertEqual(account.id, None)
        self.assertEqual(account.name, fake_account.name)
        self.assertEqual(account.email, fake_account.email)
        self.assertEqual(account.address, fake_account.address)
        self.assertEqual(account.phone_number, fake_account.phone_number)
        self.assertEqual(account.date_joined, fake_account.date_joined)

    def test_add_a_account(self):
        """It should Create an account and add it to the database"""
        accounts = Account.all()
        self.assertEqual(accounts, [])
        account = AccountFactory()
        account.create()
        self.assertIsNotNone(account.id)
        accounts = Account.all()
        self.assertEqual(len(accounts), 1)

    def test_read_account(self):
        """It should Read an account"""
        account = AccountFactory()
        account.create()
        found_account = Account.find(account.id)
        self.assertEqual(found_account.id, account.id)
        self.assertEqual(found_account.name, account.name)

    def test_update_account(self):
        """It should Update an account"""
        account = AccountFactory(email="advent@change.me")
        account.create()
        self.assertEqual(account.email, "advent@change.me")
        account = Account.find(account.id)
        account.email = "XYZZY@plugh.com"
        account.update()
        account = Account.find(account.id)
        self.assertEqual(account.email, "XYZZY@plugh.com")

    def test_delete_an_account(self):
        """It should Delete an account from the database"""
        accounts = Account.all()
        self.assertEqual(accounts, [])
        account = AccountFactory()
        account.create()
        self.assertIsNotNone(account.id)
        accounts = Account.all()
        self.assertEqual(len(accounts), 1)
        account.delete()
        accounts = Account.all()
        self.assertEqual(len(accounts), 0)

    def test_list_all_accounts(self):
        """It should List all Accounts in the database"""
        accounts = Account.all()
        self.assertEqual(accounts, [])
        for account in AccountFactory.create_batch(5):
            account.create()
        accounts = Account.all()
        self.assertEqual(len(accounts), 5)

    def test_find_by_name(self):
        """It should Find an Account by name"""
        account = AccountFactory()
        account.create()
        same_account = Account.find_by_name(account.name)[0]
        self.assertEqual(same_account.id, account.id)
        self.assertEqual(same_account.name, account.name)

    def test_serialize_an_account(self):
        """It should Serialize an account"""
        account = AccountFactory()
        serial_account = account.serialize()
        self.assertEqual(serial_account["id"], account.id)
        self.assertEqual(serial_account["name"], account.name)

    def test_deserialize_an_account(self):
        """It should Deserialize an account"""
        account = AccountFactory()
        account.create()
        serial_account = account.serialize()
        new_account = Account()
        new_account.deserialize(serial_account)
        self.assertEqual(new_account.name, account.name)

    def test_deserialize_with_key_error(self):
        """It should not Deserialize an account with a KeyError"""
        account = Account()
        self.assertRaises(DataValidationError, account.deserialize, {})

    def test_deserialize_with_type_error(self):
        """It should not Deserialize an account with a TypeError"""
        account = Account()
        self.assertRaises(DataValidationError, account.deserialize, [])

    def test_deserialize_with_invalid_type(self):
        """It should raise error for non-dict input in deserialize"""
        account = Account()
        with self.assertRaises(DataValidationError):
            account.deserialize("not-a-dict")

    def test_update_account_without_id(self):
        """It should raise DataValidationError if updating without ID"""
        account = Account(name="No ID", email="noid@example.com", address="Nowhere")
        account.id = None
        with self.assertRaises(DataValidationError):
            account.update()
