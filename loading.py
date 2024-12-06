from database import get_db
from habit import Habit
from datetime import date, timedelta
import random


def dayminus(x):
    dateminusdays = date.today() - timedelta(days=x)
    return dateminusdays

def load_predefined_habits():
    """
    Loads predefined habits.
    Stores upload flag in database, to make sure they are only loaded once at very first app usage.

    No return value. Directly modifies the database.
    """
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM upload_flag")
    row = cur.fetchone()
    if row is None or row[0] != "True":
        cur.execute("INSERT INTO upload_flag (bool) VALUES ('True')")
        db.commit()

        daily_1 = Habit("do a good deed", "be a decent human", "daily", "predefined")
        daily_2 = Habit("stretching", "10 minutes minimum - stay flexible", "daily", "predefined")
        daily_3 = Habit("use python", "improve those skills", "daily", "predefined")
        weekly_1 = Habit("cook a new dish", "cook something you never cooked before", "weekly", "predefined")
        weekly_2 = Habit("deep clean one room", "a clean space is a clear mind", "weekly", "predefined")
        weekly_3 = Habit("meaningful conversation", "deep, uninterrupted conversation with someone close to you.", "weekly", "predefined")
        daily_1.store(db)
        daily_2.store(db)
        daily_3.store(db)
        weekly_1.store(db)
        weekly_2.store(db)
        weekly_3.store(db)


def load_mock_data():
    """
     Loads mock habit data into the database for user-testing.
     Creates and stores mock habits.
     Marks these habits as completed on past dates and random times.

     No return value. Directly modifies the database.
     """
    db = get_db()

    book = Habit("MOCK - Finish Reading One Book", "finish reading any book", "weekly", dayminus(23))
    book.store(db)
    book.check_off(db,dayminus(28),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    book.check_off(db,dayminus(21),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    book.check_off(db,dayminus(14),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    book.check_off(db,dayminus(7),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")

    culture = Habit("MOCK - Culture-Night", "visit theatre, opera, concert,...", "weekly", dayminus(22))
    culture.store(db)
    culture.check_off(db,dayminus(21),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    culture.check_off(db,dayminus(14),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    culture.check_off(db,dayminus(7),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")

    toenails = Habit("MOCK - Cut Toenails", "avoid nasty feet", "weekly", dayminus(18))
    toenails.store(db)
    toenails.check_off(db,dayminus(21),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    toenails.check_off(db,dayminus(14),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    toenails.check_off(db,dayminus(7),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")

    water = Habit("MOCK - Water Your Plants", "don't let them die", "daily", dayminus(50))
    water.store(db)
    water.check_off(db,dayminus(14),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(13),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(12),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(11),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(10),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(8),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(7),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(5),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(4),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(3),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(2),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    water.check_off(db,dayminus(1),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")

    instrument = Habit("MOCK - Play An Instrument", "play one song on any instrument", "daily", dayminus(15))
    instrument.store(db)
    instrument.check_off(db,dayminus(15),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    instrument.check_off(db,dayminus(14),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    instrument.check_off(db,dayminus(13),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    instrument.check_off(db,dayminus(12),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    instrument.check_off(db,dayminus(11),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    instrument.check_off(db,dayminus(9),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    instrument.check_off(db,dayminus(8),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    instrument.check_off(db,dayminus(7),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    instrument.check_off(db,dayminus(1),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")

    meditate = Habit("MOCK - Meditate", "meditate at least 30 minutes", "daily", dayminus(40))
    meditate.store(db)
    meditate.check_off(db,dayminus(40),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(39),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(38),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(36),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(35),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(34),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(32),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(31),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(30),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(28),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(27),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(26),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(2),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")
    meditate.check_off(db,dayminus(1),f"{random.randint(7, 23):02}:{random.randint(0, 59):02}")

    db.commit()
