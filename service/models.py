"""
Models for Account

All of the models are stored in this module
"""
import logging
from datetime import date

from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for data validation errors when deserializing or updating"""


def init_db(app):
    """Initialize the SQLAlchemy app"""
    Account.init_db(app)


######################################################################
#  P E R S I S T E N T   B A S E   M O D E L
######################################################################
class PersistentBase:
    """Base class adds persistent methods"""

    def __init__(self):
        self.id = None

    def create(self):
        """Creates an Account in the database"""
        logger.info("Creating %s", self.name)
        self.id = None
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates an Account in the database"""
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        logger.info("Updating %s", self.name)
        db.session.commit()

    def delete(self):
        """Deletes an Account from the database"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        logger.info("Initializing database")
        cls.app = app
        db.init_app(app)
        app.app_context().push()
        db.create_all()

    @classmethod
    def all(cls):
        """Returns all records in the database"""
        logger.info("Fetching all records")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a record by ID"""
        logger.info("Looking up id %s ...", by_id)
        return cls.query.get(by_id)


######################################################################
#  A C C O U N T   M O D E L
######################################################################
class Account(db.Model, PersistentBase):
    """Represents an Account in the system"""

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    address = db.Column(db.String(256))
    phone_number = db.Column(db.String(32), nullable=True)
    date_joined = db.Column(db.Date(), nullable=False, default=date.today())

    def __repr__(self):
        return f"<Account {self.name} id=[{self.id}]>"

    def serialize(self):
        """Serializes an Account into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "date_joined": self.date_joined.isoformat(),
        }

    def deserialize(self, data):
        """Deserializes an Account from a dictionary"""
        try:
            if not isinstance(data, dict):
                raise TypeError("data is not a dictionary")
            self.name = data["name"]
            self.email = data["email"]
            self.address = data["address"]
            self.phone_number = data.get("phone_number")
            date_joined = data.get("date_joined")
            if date_joined:
                self.date_joined = date.fromisoformat(date_joined)
            else:
                self.date_joined = date.today()
        except KeyError as error:
            raise DataValidationError(
                f"Invalid Account: missing {error.args[0]}"
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Account: body of request contained bad or no data"
            ) from error
        return self

    @classmethod
    def find_by_name(cls, name):
        """Returns all Accounts with the given name"""
        logger.info("Searching for name: %s", name)
        return cls.query.filter(cls.name == name)


# temp
