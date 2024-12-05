from database import get_db
from habit import Habit
from datetime import date, timedelta
import random


def dayminus(x):
    dateminusdays = date.today() - timedelta(days=x)
    return dateminusdays


def load_mock_data():
    """
     Loads mock habit data into the database for user-testing.

     Creates and stores mock habits.
     Marks these habits as completed on past dates and random times.

     No return value. Directly modifies the database.
     """
    db = get_db()

    book = Habit("MOCK - Finish Reading One Book", "finish reading any book", "weekly", "predefined")
    book.store(db,dayminus(22))
    book.check_off(db,dayminus(21),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    book.check_off(db,dayminus(14),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    book.check_off(db,dayminus(7),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")

    culture = Habit("MOCK - Culture-Night", "visit theatre, opera, concert,...", "weekly", "predefined")
    culture.store(db,dayminus(14))
    culture.check_off(db,dayminus(14),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    culture.check_off(db,dayminus(7),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")

    toenails = Habit("MOCK - Cut Toenails", "avoid nasty feet", "weekly", "predefined")
    toenails.store(db,dayminus(14))
    toenails.check_off(db,dayminus(14),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    toenails.check_off(db,dayminus(7),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")

    water = Habit("MOCK - Water Your Plants", "don't let them die", "daily", "predefined")
    water.store(db,dayminus(50))
    water.check_off(db,dayminus(14),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(13),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(12),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(11),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(10),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(8),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(7),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(5),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(4),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(3),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(2),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(1),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")

    instrument = Habit("MOCK - Play An Instrument", "play one song on any instrument", "daily", "predefined")
    instrument.store(db,dayminus(18))
    instrument.check_off(db,dayminus(15),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    instrument.check_off(db,dayminus(14),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    instrument.check_off(db,dayminus(13),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    instrument.check_off(db,dayminus(12),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    instrument.check_off(db,dayminus(11),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    instrument.check_off(db,dayminus(9),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    instrument.check_off(db,dayminus(8),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    instrument.check_off(db,dayminus(7),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    instrument.check_off(db,dayminus(1),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")

    meditate = Habit("MOCK - Meditate", "meditate at least 30 minutes", "daily", "predefined")
    meditate.store(db,dayminus(40))
    meditate.check_off(db,dayminus(40),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(39),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(38),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(36),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(35),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(34),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(32),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(31),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(30),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(28),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(27),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(26),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(2),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(1),f"{random.randint(0, 23):02}:{random.randint(0, 59):02}")

    db.commit()
