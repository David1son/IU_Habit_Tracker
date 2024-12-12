import pytest
from prettytable import PrettyTable
from database import get_db, display_habits_table, display_check_offs_table, fetch_habit_from_db
from habit import Habit
from datetime import date

@pytest.fixture
def db_connection():
    """Fixture to set up and tear down an in-memory SQLite database."""
    db = get_db(":memory:")

    habit_1 = Habit("Habit 1","Daily Habit 1", "daily", "2024-12-01")
    habit_2 = Habit("Habit 2","Weekly Habit 1", "weekly", "2024-11-19")
    habit_3 = Habit("Habit 3","Daily Habit 2", "daily", "2024-12-05")
    habit_1.store(db)
    habit_2.store(db)
    habit_3.store(db)

    habit_1.check_off(db,date.fromisoformat("2024-12-01"),"08:00")
    habit_1.check_off(db,date.fromisoformat("2024-12-02"),"10:00")
    habit_2.check_off(db,date.fromisoformat("2024-11-11"),"09:00")

    db.commit()
    yield db # return db and execute anything under this after a test is run
    db.close()

def test_display_habits_table_all(db_connection):
    """Test display_habits_table function."""
    db = db_connection
    table = display_habits_table(db)

    # should be ordered by 1) periodicity and 2) create date
    expected_table = PrettyTable()
    expected_table.field_names = ["name", "description", "periodicity", "create_date"]
    expected_table.add_row(["Habit 1", "Daily Habit 1", "daily", "2024-12-01"])
    expected_table.add_row(["Habit 3", "Daily Habit 2", "daily", "2024-12-05"])
    expected_table.add_row(["Habit 2", "Weekly Habit 1", "weekly", "2024-11-19"])

    assert table.get_string() == expected_table.get_string()


def test_display_habits_table_daily(db_connection):
    """Test displaying daily habits."""
    db = db_connection
    table = display_habits_table(db, periodicity="daily")

    # Define expected output
    expected_table = PrettyTable()
    expected_table.field_names = ["name", "description", "periodicity", "create_date"]
    expected_table.add_row(["Habit 1", "Daily Habit 1", "daily", "2024-12-01"])
    expected_table.add_row(["Habit 3", "Daily Habit 2", "daily", "2024-12-05"])

    # Compare table output as string
    assert table.get_string() == expected_table.get_string()


def test_display_habits_table_weekly(db_connection):
    """Test displaying weekly habits."""
    db = db_connection
    table = display_habits_table(db, "weekly")

    # Define expected output
    expected_table = PrettyTable()
    expected_table.field_names = ["name", "description", "periodicity", "create_date"]
    expected_table.add_row(["Habit 2", "Weekly Habit 1", "weekly", "2024-11-19"])

    assert table.get_string() == expected_table.get_string()

def test_display_check_offs_table(db_connection):
    """Test display_check_offs_table function."""
    db = db_connection

    # Test for daily habit
    daily_table = display_check_offs_table(db, "Habit 1", "daily")
    expected_daily_table = PrettyTable()
    expected_daily_table.field_names = ["Check-Off-Dates", "Check-Off-Time", "Streak-Count"]
    expected_daily_table.add_row(["2024-12-01", "08:00", 1])
    expected_daily_table.add_row(["2024-12-02", "10:00", 2])

    assert daily_table.get_string() == expected_daily_table.get_string()

    # Test for weekly habit
    weekly_table = display_check_offs_table(db, "Habit 2", "weekly")
    expected_weekly_table = PrettyTable()
    expected_weekly_table.field_names = ["Check-Off-Dates", "Check-Off-Time", "Check-Off-Week", "Streak-Count"]
    expected_weekly_table.add_row(["2024-11-11", "09:00", "46-2024", 1])

    assert weekly_table.get_string() == expected_weekly_table.get_string()

def test_fetch_habit_from_db(db_connection):
    """Test fetch_habit_from_db function."""
    db = db_connection

    # Test fetching Habit 1
    fetched_habit_data = fetch_habit_from_db(db, "Habit 1") # see test fixture
    assert fetched_habit_data == ("Habit 1", "Daily Habit 1", "daily", "2024-12-01")

    # Test fetching Habit 2
    fetched_habit_data = fetch_habit_from_db(db, "Habit 2")
    assert fetched_habit_data == ("Habit 2", "Weekly Habit 1", "weekly", "2024-11-19")
