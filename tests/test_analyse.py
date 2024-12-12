import pytest
from habit import Habit
from datetime import date
from database import get_db
from analyse import hyper_streak_daily, hyper_streak_weekly


@pytest.fixture
def db_connection():
    """Fixture for setting up and tearing down an in-memory SQLite database."""
    db = get_db(":memory:")  # Use an in-memory database for tests
    cur = db.cursor()

    db.commit()
    yield db
    db.close()


def test_hyper_streak_daily_empty_db(db_connection):
    """Test hyper_streak_daily when the database is empty."""
    db = db_connection
    result = hyper_streak_daily(db)
    assert result is None


def test_hyper_streak_daily_single_habit(db_connection):
    """Test hyper_streak_daily with a single record streak."""
    db = db_connection

    habit_1 = Habit("Daily Habit 1","a description","daily")
    habit_1.store(db)
    habit_1.check_off(db,date.fromisoformat("2024-11-20"))
    habit_1.check_off(db, date.fromisoformat("2024-11-21"))
    habit_1.check_off(db, date.fromisoformat("2024-11-22"))
    habit_1.check_off(db, date.fromisoformat("2024-11-23"))

    habit_2 = Habit("Daily Habit 2", "another description", "daily")
    habit_2.store(db)
    # generate a 3 day streak for Habit 2 that should not appear
    habit_2.check_off(db, date.fromisoformat("2024-11-10"))
    habit_2.check_off(db, date.fromisoformat("2024-11-11"))
    habit_2.check_off(db, date.fromisoformat("2024-11-12"))




    result = hyper_streak_daily(db)
    expected = [{"habit": "Daily Habit 1", "streak": 4, "last_date": "2024-11-23"}]
    assert result == expected


def test_hyper_streak_daily_multiple_habits(db_connection):
    """Test hyper_streak_daily with multiple longest streaks."""
    db = db_connection

    habit_1 = Habit("Daily Habit 1", "a description", "daily")
    habit_1.store(db)
    # generate a 5 day streak for Habit 1
    habit_1.check_off(db, date.fromisoformat("2024-11-20"))
    habit_1.check_off(db, date.fromisoformat("2024-11-21"))
    habit_1.check_off(db, date.fromisoformat("2024-11-22"))
    habit_1.check_off(db, date.fromisoformat("2024-11-23"))
    habit_1.check_off(db, date.fromisoformat("2024-11-24"))

    habit_2 = Habit("Daily Habit 2", "another description", "daily")
    habit_2.store(db)
    # generate a 5 day streak for Habit 2
    habit_2.check_off(db, date.fromisoformat("2024-11-10"))
    habit_2.check_off(db, date.fromisoformat("2024-11-11"))
    habit_2.check_off(db, date.fromisoformat("2024-11-12"))
    habit_2.check_off(db, date.fromisoformat("2024-11-13"))
    habit_2.check_off(db, date.fromisoformat("2024-11-14"))
    # another 5 day streak for Habit 2
    habit_2.check_off(db, date.fromisoformat("2024-11-25"))
    habit_2.check_off(db, date.fromisoformat("2024-11-26"))
    habit_2.check_off(db, date.fromisoformat("2024-11-27"))
    habit_2.check_off(db, date.fromisoformat("2024-11-28"))
    habit_2.check_off(db, date.fromisoformat("2024-11-29"))

    habit_3 = Habit("Daily Habit 3", "yet another description", "daily")
    habit_3.store(db)
    # generate a 4 day streak for Habit 3, that shouldn't appear as record streak
    habit_3.check_off(db, date.fromisoformat("2024-11-20"))
    habit_3.check_off(db, date.fromisoformat("2024-11-19"))
    habit_3.check_off(db, date.fromisoformat("2024-11-18"))
    habit_3.check_off(db, date.fromisoformat("2024-11-17"))


    result = hyper_streak_daily(db)
    # result should include all three longest daily streaks. Habit 2 has two separate 5 day streaks. Streaks are ordered by check_off_date
    expected = [
        {"habit": "Daily Habit 2", "streak": 5, "last_date": "2024-11-14"},
        {"habit": "Daily Habit 1", "streak": 5, "last_date": "2024-11-24"},
        {"habit": "Daily Habit 2", "streak": 5, "last_date": "2024-11-29"}]
    assert result == expected

    # reassure it returns single hyper streak after additional check-off for Habit 2
    habit_2.check_off(db, date.fromisoformat("2024-11-30"))
    result = hyper_streak_daily(db)

    expected = [{"habit": "Daily Habit 2", "streak": 6, "last_date": "2024-11-30"}]
    assert result == expected



def test_hyper_streak_weekly_empty_db(db_connection):
    """Test hyper_streak_weekly when the database is empty."""
    db = db_connection
    result = hyper_streak_weekly(db)
    assert result is None


def test_hyper_streak_weekly_single_habit(db_connection):
    """Test hyper_streak_weekly with a single longest streak."""
    db = db_connection

    habit_1 = Habit("Weekly Habit 1", "a description", "weekly")
    habit_1.store(db)
    habit_1.check_off(db, date.fromisoformat("2024-11-06"))
    habit_1.check_off(db, date.fromisoformat("2024-11-13"))
    habit_1.check_off(db, date.fromisoformat("2024-11-20"))


    result = hyper_streak_weekly(db)
    expected = [{"habit": "Weekly Habit 1", "streak": 3, "last_week": "47-2024", "last_date": "2024-11-20"}]
    assert result == expected


def test_hyper_streak_weekly_multiple_habits(db_connection):
    """Test hyper_streak_weekly with multiple longest streaks."""
    db = db_connection

    habit_1 = Habit("Weekly Habit 1", "a description", "weekly")
    habit_1.store(db)
    habit_1.check_off(db, date.fromisoformat("2024-11-06"))
    habit_1.check_off(db, date.fromisoformat("2024-11-13"))
    habit_1.check_off(db, date.fromisoformat("2024-11-20")) # calendar week 47
    habit_2 = Habit("Weekly Habit 2", "another description", "weekly")
    habit_2.store(db)
    habit_2.check_off(db, date.fromisoformat("2024-10-06"))
    habit_2.check_off(db, date.fromisoformat("2024-10-13"))
    habit_2.check_off(db, date.fromisoformat("2024-10-20")) # calendar week 42
    habit_3 = Habit("Weekly Habit 3", "yet another description", "weekly")
    habit_3.store(db)
    habit_3.check_off(db, date.fromisoformat("2024-09-06"))
    habit_3.check_off(db, date.fromisoformat("2024-09-13"))
    habit_3.check_off(db, date.fromisoformat("2024-09-20")) # calendar week 38
    habit_4 = Habit("Weekly Habit 4", "a fourth description", "weekly")
    habit_4.store(db)
    habit_4.check_off(db, date.fromisoformat("2024-08-06"))
    habit_4.check_off(db, date.fromisoformat("2024-08-13"))
    habit_4.check_off(db, date.fromisoformat("2024-08-20")) # calendar week 34

    result = hyper_streak_weekly(db)
    expected = [
        {"habit": "Weekly Habit 4", "streak": 3, "last_week": "34-2024", "last_date": "2024-08-20"},
        {"habit": "Weekly Habit 3", "streak": 3, "last_week": "38-2024", "last_date": "2024-09-20"},
        {"habit": "Weekly Habit 2", "streak": 3, "last_week": "42-2024", "last_date": "2024-10-20"},
        {"habit": "Weekly Habit 1", "streak": 3, "last_week": "47-2024", "last_date": "2024-11-20"},]

    assert result == expected

# reassure it returns single hyper streak after additional check-off
    habit_4.check_off(db, date.fromisoformat("2024-08-27"))
    result = hyper_streak_weekly(db)

    expected = [{"habit": "Weekly Habit 4", "streak": 4,  "last_week": "35-2024", "last_date": "2024-08-27"}]
    assert result == expected