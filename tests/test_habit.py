import pytest
from datetime import date, timedelta, datetime
from habit import Habit
from database import get_db


@pytest.fixture
def db_connection():
    """Fixture for setting up and tearing down an in-memory SQLite database."""
    db = get_db(":memory:")  # Use an in-memory database for tests
    yield db # return db and execute anything under this after a test is run
    db.close()

@pytest.fixture
def setup_daily_habit(db_connection):
    """Fixture for setting up a daily habit."""
    db = db_connection
    habit = Habit(name="Exercise", description="Daily workout", periodicity="daily")
    habit.store(db)  # Store the habit in the database
    return db, habit

@pytest.fixture
def setup_weekly_habit(db_connection):
    """Fixture for setting up a weekly habit."""
    db = db_connection
    habit = Habit(name="Study", description="Weekly study session", periodicity="weekly")
    habit.store(db)  # Store the habit in the database
    return db, habit

#date.today() - timedelta(days=x)
def test_habit_creation():
    """Test creation of Habit objects."""
    habit = Habit("Test Habit", "Description", "daily",date.today())
    assert habit.name == "Test Habit"
    assert habit.description == "Description"
    assert habit.periodicity == "daily"
    assert habit.create_date == date.today()

    # test non default create_date
    habit2 = Habit("Test Habit2", "Description2", "daily2",date.today() - timedelta(days=5))
    assert habit2.create_date == date.today() - timedelta(days=5)

def test_store_habit(db_connection):
    """Test storing a habit in the database via the store-method."""
    db = db_connection
    habit = Habit("Test Habit", "Description", "daily")
    habit.store(db)

    # Verify the habit exists in the database
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE name=?", (habit.name,))
    result = cur.fetchone()
    assert result is not None
    assert result[0] == "Test Habit"
    assert result[1] == "Description"
    assert result[2] == "daily"
    assert result[3] == str(date.today()) # create_date is today per default, dates are stored as text/string

    # verify that habit_name must be unique to be stored
    habit_dupe = Habit("Test Habit", "even when description and periodicity differs", "weekly")
    habit_dupe.store(db)
    cur.execute("SELECT * FROM habits WHERE name=?", ("Test Habit",))
    result = cur.fetchall()
    assert len(result) == 1 # still only one entry




def test_check_off_daily_habit_default_date(setup_daily_habit):
    """Test check_off method by checking off a daily habit with the default date and time."""
    db, habit = setup_daily_habit
    habit.check_off(db)

    now = datetime.now()
    check_off_time = now.strftime("%H:%M")
    cur = db.cursor()
    cur.execute("SELECT * FROM check_offs WHERE habit_name=?", (habit.name,))
    result = cur.fetchone()

    assert result is not None
    assert result[2] == str(date.today())  # Check-off date is today
    assert result[3] == check_off_time  # Check-off time matches
    assert result[4] == 1  # Start of a new daily streak


def test_streak_day_increment(setup_daily_habit):
    """Test streak_day_count incrementation for a daily habit via check_off method."""
    db, habit = setup_daily_habit
    dates = [
        date.fromisoformat("2024-11-11"),
        date.fromisoformat("2024-11-12"),
        date.fromisoformat("2024-11-13"),
        date.fromisoformat("2024-11-14"),]

    for check_off_date in dates:
        habit.check_off(db, check_off_date)

    cur = db.cursor()
    cur.execute(
        "SELECT streak_day_count FROM check_offs WHERE habit_name=? AND check_off_date=?",
        (habit.name, "2024-11-14"),
    )
    result = cur.fetchone()
    assert result[0] == 4


def test_streak_day_reset(setup_daily_habit):
    """Test streak_day_count reset after skipping a day via check_off method."""
    db, habit = setup_daily_habit
    habit.check_off(db, date.fromisoformat("2024-11-11"))
    habit.check_off(db, date.fromisoformat("2024-11-12"))
    habit.check_off(db, date.fromisoformat("2024-11-14"))  # Skip one day

    cur = db.cursor()
    cur.execute("SELECT streak_day_count FROM check_offs WHERE habit_name=? AND check_off_date=?",
        (habit.name, "2024-11-14"),)
    result = cur.fetchone()
    assert result[0] == 1  # Streak reset


def test_weekly_streak_increment(setup_weekly_habit):
    """Test streak_week_count incrementation for a weekly habit via check_off method."""
    db, habit = setup_weekly_habit
    check_off_dates = [
        date.fromisoformat("2024-11-11"),  # Week 46
        date.fromisoformat("2024-11-20"),  # Week 47
        date.fromisoformat("2024-11-29"),  # Week 48
    ]

    for check_off_date in check_off_dates:
        habit.check_off(db, check_off_date)

    cur = db.cursor()
    cur.execute(
        "SELECT streak_week_count FROM check_offs WHERE habit_name=? AND calendar_week=?",
        (habit.name, "48-2024"),
    )
    result = cur.fetchone()
    assert result[0] == 3  # Third week in a row


def test_weekly_streak_reset(setup_weekly_habit):
    """Test streak_week_count reset after skipping a week via check_off method."""
    db, habit = setup_weekly_habit
    habit.check_off(db, date.fromisoformat("2024-11-11"))  # Week 46
    habit.check_off(db, date.fromisoformat("2024-11-20"))  # Week 47
    habit.check_off(db, date.fromisoformat("2024-12-10"))  # Skip two weeks (Week 50)

    cur = db.cursor()
    cur.execute(
        "SELECT streak_week_count FROM check_offs WHERE habit_name=? AND calendar_week=?",
        (habit.name, "50-2024"),
    )
    result = cur.fetchone()
    assert result[0] == 1  # Streak reset


def test_prevent_double_check_off(setup_daily_habit):
    """Test that double entries for the same check-off day are not allowed via check_off method."""
    db, habit = setup_daily_habit
    habit.check_off(db, date.fromisoformat("2024-11-14"))
    habit.check_off(db, date.fromisoformat("2024-11-14"))  # Attempt to check off the same day again

    cur = db.cursor()
    cur.execute(
        "SELECT * FROM check_offs WHERE habit_name=? AND check_off_date=?",
        (habit.name, "2024-11-14"),
    )
    result = cur.fetchall()
    assert len(result) == 1  # Only one entry exists


def test_prevent_double_week_check_off(setup_weekly_habit):
    """Test that double entries for the same week are not allowed."""
    db, habit = setup_weekly_habit
    habit.check_off(db, date.fromisoformat("2024-12-10"))  # Week 50
    habit.check_off(db, date.fromisoformat("2024-12-12"))  # Same week

    cur = db.cursor()
    cur.execute(
        "SELECT * FROM check_offs WHERE habit_name=? AND calendar_week=?",
        (habit.name, "50-2024"))
    result = cur.fetchall()
    assert len(result) == 1  # Only one entry exists for the week


# Current streak tests
def test_current_streak_no_check_off_daily(setup_daily_habit):
    """Test current streak method for a daily habit with no check-offs."""
    db, habit = setup_daily_habit
    result = habit.current_streak(db)
    assert result["current_streak"] == 0
    assert "Check \"Exercise\" off today to continue or start a streak." in result["message"]


def test_current_streak_started_daily(setup_daily_habit):
    """Test current streak method for a daily habit with a single check-off."""
    db, habit = setup_daily_habit
    habit.check_off(db)  # Check off the habit today
    result = habit.current_streak(db)
    assert result["current_streak"] == 1
    assert "You just started your \"Exercise\"-streak today. Keep going!" in result["message"]


def test_current_streak_ongoing_daily(setup_daily_habit):
    """Test current streak method for a daily habit with multiple consecutive check-offs."""
    db, habit = setup_daily_habit
    habit.check_off(db, date.today() - timedelta(days=2))
    habit.check_off(db, date.today() - timedelta(days=1))
    habit.check_off(db, date.today())
    result = habit.current_streak(db)
    assert result["current_streak"] == 3
    assert "Well done! You've kept your \"Exercise\"-streak alive for 3 consecutive days already." in result["message"]


def test_current_streak_no_check_off_weekly(setup_weekly_habit):
    """Test current streak method for a weekly habit with no check-offs."""
    db, habit = setup_weekly_habit
    result = habit.current_streak(db)
    assert result["current_streak"] == 0
    assert "Check \"Study\" off this week to continue or start a streak." in result["message"]


def test_current_streak_started_weekly(setup_weekly_habit):
    """Test current streak method for a weekly habit with a single check-off."""
    db, habit = setup_weekly_habit
    habit.check_off(db)  # Check off the habit today
    result = habit.current_streak(db)
    assert result["current_streak"] == 1
    assert "You just started your \"Study\"-streak this week. Keep going!" in result["message"]


def test_current_streak_ongoing_weekly(setup_weekly_habit):
    """Test current streak method for a weekly habit with multiple consecutive check-offs."""
    db, habit = setup_weekly_habit
    habit.check_off(db, date.today() - timedelta(weeks=3))
    habit.check_off(db, date.today() - timedelta(weeks=2))
    habit.check_off(db, date.today() - timedelta(weeks=1))
    habit.check_off(db, date.today())
    result = habit.current_streak(db)
    assert result["current_streak"] == 4
    assert "Well done! You've kept your \"Study\"-streak alive for 4 consecutive weeks already." in result["message"]


# Longest streak tests
def test_longest_streak_no_check_off_daily(setup_daily_habit):
    """Test longest streak method for a daily habit with no check-offs."""
    db, habit = setup_daily_habit
    result = habit.longest_streak(db)
    assert result["longest_streak"] == 0
    assert "You haven't started checking off \"Exercise\" yet." in result["message"]

def test_longest_streak_single_streak_daily(setup_daily_habit):
    """
    Test longest streak method for a daily habit with a single streak.
    Check for differentiation between longest = ongoing vs. finished streak.
    """
    # finished streak
    db, habit = setup_daily_habit
    habit.check_off(db, date.today() - timedelta(days=6))
    habit.check_off(db, date.today() - timedelta(days=5))
    habit.check_off(db, date.today() - timedelta(days=4))
    habit.check_off(db, date.today() - timedelta(days=3))

    result = habit.longest_streak(db)
    assert result["longest_streak"] == 4
    assert f"Your longest \"Exercise\"-streak was 4 day(s) and ended on {date.today() - timedelta(days=3)}." in result["message"]


    # ongoing streak
    habit.check_off(db, date.today() - timedelta(days=2))
    habit.check_off(db, date.today() - timedelta(days=1))
    habit.check_off(db, date.today())
    result = habit.longest_streak(db)

    assert result["longest_streak"] == 7
    assert f"Your longest \"Exercise\"-streak is 7 day(s) and is still going. Don't stop here." in result["message"]


def test_longest_streak_multiple_streaks_daily(setup_daily_habit):
    """
    Test longest streak method for a daily habit with multiple longest streaks.
    Check for differentiation between longest = ongoing vs. finished streak
    """
    db, habit = setup_daily_habit
    # Create three separate 2-day streaks. no ongoing one
    habit.check_off(db, date.today() - timedelta(days=10))
    habit.check_off(db, date.today() - timedelta(days=9))
    habit.check_off(db, date.today() - timedelta(days=7))
    habit.check_off(db, date.today() - timedelta(days=6))
    habit.check_off(db, date.today() - timedelta(days=4))
    habit.check_off(db, date.today() - timedelta(days=3))
    result = habit.longest_streak(db)
    assert result["longest_streak"] == 2
    assert f"\nLongest Streak: You've had 3 separate longest streaks of 2 day(s) for \"Exercise\", with the most recent one ending on {date.today() - timedelta(days=3)}." == result["message"]

    # Create a fourth 2-day streak, which is ongoing
    habit.check_off(db, date.today() - timedelta(days=1))
    habit.check_off(db, date.today())
    result = habit.longest_streak(db)
    assert result["longest_streak"] == 2
    expected_message = f"\nLongest Streak: You've had 4 separate longest streaks of 2 day(s) for \"Exercise\". Check it off tomorrow to set a new record."
    assert expected_message == result["message"]



def test_longest_streak_ongoing_weekly(setup_weekly_habit):
    """Test longest streak method for a weekly habit with ongoing streak."""
    db, habit = setup_weekly_habit
    habit.check_off(db, date.today() - timedelta(weeks=2))
    habit.check_off(db, date.today() - timedelta(weeks=1))
    habit.check_off(db, date.today())
    result = habit.longest_streak(db)
    assert result["longest_streak"] == 3
    assert f"Your longest \"Study\"-streak is 3 week(s) and is still going." in result["message"]


