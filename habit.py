from analyse import current_streak_calculation, longest_streak_calculation
from database import add_habit, check_off_habit


class Habit:


    def __init__(self, name, description, periodicity, create_date=None):
        """
        Habit class to represent a habit with tracking functionality.

        :param name: Name of the habit.
        :param description: Description of the habit.
        :param periodicity: Periodicity of the habit (daily/weekly).
        :param create_date: Date on which the habit was created.
        """
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.create_date = create_date


    def __str__(self):
        return f"name: {self.name}, description: {self.description}, periodicity: {self.periodicity}, create_date: {self.create_date}"


    def store(self, db):
        """
        Store the habit in the database.

        :param db: SQLite database connection object.
        """
        add_habit(db, self.name, self.description, self.periodicity, self.create_date)


    def check_off(self, db,check_off_date=None, check_off_time=None):
        """
        Mark the habit as completed for a specific date and store associated check-off-data in the database.

        :param db: SQLite database connection object.
        :param check_off_date: Date of the check-off (default is today).
        :param check_off_time: Time of the check-off (default is current time).
        """
        check_off_habit(db, self.name, self.periodicity,check_off_date, check_off_time)


    def current_streak(self,db):
        """
        Calculate the current streak of the habit.

        :param db: SQLite database connection object.
        :return: Dictionary with the current streak details.
        """
        return current_streak_calculation(db,self.name,self.periodicity)

    def longest_streak(self,db):
        """
        Calculate the longest streak of the habit.

        :param db: SQLite database connection object.
        :return: Dictionary with the longest streak details.
        """
        return longest_streak_calculation(db,self.name,self.periodicity)
