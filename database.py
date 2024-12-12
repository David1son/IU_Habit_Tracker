import sqlite3
from datetime import date, timedelta, datetime
from prettytable import PrettyTable


def get_db(name="main.db"):
    """
    Get a SQLite database connection and create tables if not existing.

    :param name: The name of the database file, default is "main.db".
    :return: SQLite database connection.
    """
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    """
    Creates the two tables for the actual habit tracking and one table to just store the flag for predefined habits upload.

    param db: SQLite database connection.
    """
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS habits( 
    name TEXT PRIMARY KEY, description TEXT, periodicity TEXT, create_date TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS check_offs( check_off_ID INTEGER PRIMARY KEY AUTOINCREMENT,
         habit_name TEXT, check_off_date TEXT, check_off_time TEXT, streak_day_count INT, calendar_week TEXT, 
         streak_week_count INT, FOREIGN KEY (habit_name) REFERENCES habits(name))""")
    cur.execute("""CREATE TABLE IF NOT EXISTS upload_flag( 
       bool TEXT)""")

    db.commit()


def add_habit(db, name, description, periodicity, create_date=None): #
    """
    Add a new habit to the database, ensuring the habit name is unique.

    :param db: SQLite database connection object.
    :param name: Name of the habit.
    :param description: Description of the habit.
    :param periodicity: Periodicity of the habit ("daily" or "weekly").
    :param create_date: Date the habit was created, defaults to today's date.
    """
    cur = db.cursor()
    if create_date is None:
        create_date = str(date.today())
    # Check if habit already exists in the database
    cur.execute("SELECT 1 FROM habits WHERE name=?", (name,))
    if cur.fetchone():
        print("Habit already exists") # delete
        return
    # Insert new habit into the database if it doesn't exist
    cur.execute("INSERT INTO habits VALUES (?, ?, ?, ?)", (name, description, periodicity, create_date))
    db.commit()


def check_off_habit(db, name, periodicity, check_off_date=None, check_off_time=None):
    """
    Record a habit check-off in the database (check_offs table), ensuring the date is unique.
    Auto-increments the streak-count if it was checked-off in previous period.

    :param db: SQLite database connection object.
    :param name: Name of the habit.
    :param periodicity: Periodicity of the habit ("daily" or "weekly").
    :param check_off_date: Date of check-off, defaults to today's date.
    :param check_off_time: Time of check-off, defaults to current time.
    """
    cur = db.cursor()

    # Assign today's date and time if nothing is provided
    if check_off_date is None:
        check_off_date = date.today()
    if check_off_time is None:
        now = datetime.now()
        check_off_time = now.strftime("%H:%M") # from https://www.geeksforgeeks.org/python-strftime-function/

    if periodicity == "daily":
        # check if habit is already checked off that day
        cur.execute("SELECT 1 FROM check_offs WHERE habit_name = ? AND check_off_date = ?",
            (name, str(check_off_date)))
        if cur.fetchone():  # If a record is found  -> abort
            print(f"Habit '{name}' is already checked off for {check_off_date}.")  # not relevant for app, leave in for testing
            return
        else:
            # Check if habit was checked off 1 day prior to the check-off date
            check_off_date_minus_1 = str(check_off_date - timedelta(days=1))
            cur.execute(
                "SELECT 1 FROM check_offs WHERE habit_name = ? AND check_off_date = ?",
                (name, check_off_date_minus_1))
            bool_day_before = cur.fetchone()

            #calculate streak_count
            if not bool_day_before:
                streak_day_count = 1 # for a new streak-start
            else:
                cur.execute(
                    "SELECT streak_day_count FROM check_offs WHERE habit_name = ? AND check_off_date = ?",
                    (name, check_off_date_minus_1),)
                streak_day_count = int(cur.fetchone()[0]) + 1 # add 1 to streak_count from day before

            # Insert the new check-off entry
            cur.execute(
                "INSERT INTO check_offs (check_off_date, check_off_time, habit_name, streak_day_count) "
                "VALUES (?, ?, ?, ?)",
                (str(check_off_date), check_off_time, name, streak_day_count))
            print(f"Habit '{name}' has been successfully checked off for {check_off_date}.")  # delete


    else:  # periodicity == "weekly"
        year, week, _ = check_off_date.isocalendar()
        calendar_week = f"{week}-{year}"
        # check if habit is already checked off that week
        cur.execute("SELECT 1 FROM check_offs WHERE habit_name = ? AND calendar_week = ?",
                    (name, calendar_week))
        if cur.fetchone():  # If a record is found -> abort
            print(f"Habit '{name}' is already checked off for {calendar_week}.")  # delete!!!!!!!!!!!!!!!1
            return
        else:
            check_off_date_minus_7 = check_off_date - timedelta(days=7)
            year_minus_1, week_minus_1, _ = check_off_date_minus_7.isocalendar()
            calendar_week_minus_1 = f"{week_minus_1}-{year_minus_1}"

            # Check if habit was checked off 1 week prior to the current week
            cur.execute(
                "SELECT 1 FROM check_offs WHERE habit_name = ? AND calendar_week = ?",
                (name, calendar_week_minus_1))
            bool_week_before = cur.fetchone()

            # calculate streak_count
            if not bool_week_before:
                streak_week_count = 1
            else:
                cur.execute(
                    "SELECT streak_week_count FROM check_offs WHERE habit_name = ? AND calendar_week = ?",
                    (name, calendar_week_minus_1))
                streak_week_count = int(cur.fetchone()[0]) + 1 # add 1 to streak_count

            # Insert the new check-off entry
            cur.execute(
                "INSERT INTO check_offs "
                "(check_off_date, check_off_time, habit_name, calendar_week, streak_week_count) "
                "VALUES (?, ?, ?, ?, ?)",
                (str(check_off_date), check_off_time, name, calendar_week, streak_week_count))

            print(f"Habit '{name}' has been successfully checked off for {calendar_week}.") # delete

    db.commit()


def display_habits_table(db,periodicity=None):
    """
    Display the habits table with optional filtering by periodicity.

    :param db: SQLite database connection object.
    :param periodicity: Filter habits by "daily", "weekly", or None for all habits.
    :return: PrettyTable object containing the habits table.
    """
    cur = db.cursor()

    # Build the query dynamically based on the filter
    query = "SELECT * FROM habits"
    if periodicity == "daily":
        query += " WHERE periodicity = 'daily'"
    elif periodicity == "weekly":
        query += " WHERE periodicity = 'weekly'"
    query += " ORDER BY periodicity, create_date"  # Add ordering

    cur.execute(query)
    # fetch all rows
    rows = cur.fetchall()
    # fetch column headers
    column_names = [description[0] for description in cur.description]

    # create PrettyTable
    table = PrettyTable()
    table.field_names = column_names
    for row in rows:
        table.add_row(row)

    return table



def display_check_offs_table(db, habit_name, periodicity):
    """
    Display the check_offs table filtered by habit name and periodicity.

    :param db: SQLite3 database connection object
    :param habit_name: Name of the habit to filter by
    :param periodicity: Periodicity of the habit (daily or weekly)
    :return: PrettyTable object containing the filtered check_offs data
    """
    cur = db.cursor()

    # Build the query dynamically based on the filters
    if periodicity == "weekly":
        query = f"""SELECT check_off_date AS "Check-Off-Dates", check_off_time AS "Check-Off-Time", 
                calendar_week AS "Check-Off-Week", streak_week_count AS "Streak-Count" 
                FROM check_offs WHERE habit_name = '{habit_name}' ORDER BY check_off_date"""
    else:  # periodicity == "daily"
        query = f"""SELECT check_off_date AS "Check-Off-Dates", check_off_time AS "Check-Off-Time", 
                streak_day_count AS "Streak-Count" 
                FROM check_offs WHERE habit_name = '{habit_name}' ORDER BY check_off_date"""


    cur.execute(query)
    #fetch all rows
    rows = cur.fetchall()
    # Fetch column names
    column_names = [description[0] for description in cur.description]

    # create PrettyTable
    table = PrettyTable()
    table.field_names = column_names
    for row in rows:
        table.add_row(row)

    return table


def fetch_habit_from_db(db, name):
    """
    Fetch a habit's attributes from the database by providing its name.

    :param db: SQLite database connection object.
    :param name: Name of the habit.
    :return: Tuple containing habit attributes (name, description, periodicity, create_date).
    """
    cursor = db.cursor()
    cursor.execute(
        "SELECT description, periodicity, create_date FROM habits WHERE name=?",
        (name,))
    habit_data = cursor.fetchone()
    habit_attributes = (name, habit_data[0], habit_data[1], habit_data[2])
    return habit_attributes
