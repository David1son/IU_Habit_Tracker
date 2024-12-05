from datetime import date


def current_streak_calculation(db, name,periodicity):
    """
       Calculate the current streak for a given habit and store streak_count and the message to print for the app-user in a dictionary.

       :param db: SQLite database connection object.
       :param name: Name of the habit.
       :param periodicity: Periodicity of the habit ("daily" or "weekly").
       :return: Dictionary with the current streak details.
       """
    cur = db.cursor()
    today = date.today()
    # create dictionary template
    streak_dict = {"current_streak": 0, "message": "", "periodicity": periodicity}

    # update dictionary template with correct input
    if periodicity == "daily":
        # check if a streak exists
        cur.execute("SELECT 1 FROM check_offs WHERE habit_name=? AND check_off_date=?", (name, str(today)))
        bool = cur.fetchone()
        if not bool:
            streak_dict["message"] = f"\nCurrent Streak: Check \"{name}\" off today to continue or start a streak."
        else:
            cur.execute("SELECT streak_day_count FROM check_offs WHERE habit_name=? AND check_off_date=?", (name, str(today)))
            streak = cur.fetchone()[0]
            streak_dict["current_streak"] = streak
            # differentiate between a streak that just started and anything else
            if streak == 1:
                streak_dict["message"] = f"\nCurrent Streak: You just started your \"{name}\"-streak today. Keep going!"
            else:
                streak_dict["message"] = f"\nCurrent Streak: Well done! You've kept your \"{name}\"-streak alive for {streak} consecutive days already."

    else:  # periodicity == "weekly"
        year, week, _ = today.isocalendar()
        calendar_week = f"{week}-{year}"

        # check if a streak exists
        cur.execute("SELECT 1 FROM check_offs WHERE habit_name=? AND calendar_week=?", (name, calendar_week))
        bool = cur.fetchone()
        if not bool:
            streak_dict["message"] = f"\nCurrent Streak: Check \"{name}\" off this week to continue or start a streak."
        else:
            cur.execute("SELECT streak_week_count FROM check_offs WHERE habit_name=? AND calendar_week=?", (name, calendar_week))
            streak = cur.fetchone()[0]
            streak_dict["current_streak"] = streak
            # differentiate between a streak that just started and anything else
            if streak == 1:
                streak_dict["message"] = f"\nCurrent Streak: You just started your \"{name}\"-streak this week. Keep going!"
            else:
                streak_dict["message"] = f"\nCurrent Streak: Well done! You've kept your \"{name}\"-streak alive for {streak} consecutive weeks already."

    return streak_dict


def longest_streak_calculation(db, name, periodicity):
    """
    Calculate the longest streak for a given habit and store streak_count and the message to print for the app-user in a dictionary.

    :param db: SQLite database connection object.
    :param name: Name of the habit.
    :param periodicity: Periodicity of the habit ("daily" or "weekly").
    :return: Dictionary with the longest streak details.
    """
    cur = db.cursor()
    today = date.today()
    # create dictionary template
    streak_dict = {"longest_streak": 0, "message": "", "periodicity": periodicity}

    # update dictionary template with correct input
    if periodicity == "daily":
        cur.execute("SELECT 1 FROM check_offs WHERE habit_name=? AND streak_day_count >= 1", (name,))
        bool = cur.fetchone()
        if not bool:
            streak_dict["message"] = f"\nLongest Streak: You haven't started checking off \"{name}\" yet."
        else:
            # fetch all entries with the maximum streak_count and their respective check_off_date
            cur.execute("SELECT streak_day_count, check_off_date FROM check_offs WHERE habit_name = ? "
                        "AND streak_day_count = (SELECT MAX(streak_day_count) FROM check_offs WHERE habit_name = ?) "
                        "ORDER BY check_off_date DESC", (name, name))
            fetch = cur.fetchall()
            streak = fetch[0][0]
            streak_last_date = fetch[0][1] # last check_off date of last streak
            streak_dict["longest_streak"] = streak
            nr_of_occasions = len(fetch) # how many different longest streaks

            # differentiate between 1 vs many longest streaks AND longest=current vs longest!=current
            if nr_of_occasions == 1:
                if streak_last_date == str(today):
                    streak_dict["message"] = f"\nLongest Streak: Your longest \"{name}\"-streak is {streak} day(s) and is still going. Don't stop here."
                else:
                    streak_dict["message"] = f"\nLongest Streak: Your longest \"{name}\"-streak was {streak} day(s) and ended on {streak_last_date}."
            else:
                if streak_last_date == str(today):
                    streak_dict["message"] = f"\nLongest Streak: You've had {nr_of_occasions} separate longest streaks of {streak} day(s) for \"{name}\". Check it off tomorrow to set a new record."
                else:
                    streak_dict["message"] = f"\nLongest Streak: You've had {nr_of_occasions} separate longest streaks of {streak} day(s) for \"{name}\", with the most recent one ending on {streak_last_date}."

    else:  # periodicity == "weekly"   analogue to daily procedure
        year, week, _ = today.isocalendar()
        calendar_week = f"{week}-{year}"

        cur.execute("SELECT 1 FROM check_offs WHERE habit_name=? AND streak_week_count >= 1", (name,))
        bool = cur.fetchone()
        if not bool:
            streak_dict["message"] = f"\nLongest Streak: You haven't started checking off \"{name}\" yet."
        else:
            cur.execute("SELECT streak_week_count, calendar_week FROM check_offs WHERE habit_name = ? "
                        "AND streak_week_count = (SELECT MAX(streak_week_count) FROM check_offs WHERE habit_name = ?) "
                        "ORDER BY check_off_date DESC", (name, name))
            fetch = cur.fetchall()
            streak = fetch[0][0]
            streak_last_week = fetch[0][1]
            streak_dict["longest_streak"] = streak
            nr_of_occasions = len(fetch)

            # differentiate between 1 vs many longest streaks AND ongoing longest=current vs longest!=current
            if nr_of_occasions == 1:
                if streak_last_week == calendar_week:
                    streak_dict["message"] = f"\nLongest Streak: Your longest \"{name}\"-streak is {streak} week(s) and is still going. Don't stop here."
                else:
                    streak_dict["message"] = f"\nLongest Streak: Your longest \"{name}\"-streak was {streak} week(s) and ended in week: {streak_last_week}."
            else:
                if streak_last_week == calendar_week:
                    streak_dict["message"] = f"\nLongest Streak: You've had {nr_of_occasions} separate longest streaks of {streak} week(s) for \"{name}\". Check it off next week to set a new record."
                else:
                    streak_dict["message"] = f"\nLongest Streak: You've had {nr_of_occasions} separate longest streaks of {streak} week(s) for \"{name}\", with the most recent one ending in week: {streak_last_week}."

    return streak_dict


def hyper_streak_daily(db):
    """
    Fetch all longest daily streaks across all daily habits.

    :param db: SQLite database connection object.
    :return: List of dictionaries containing habit name, streak count, and last date.
    """
    cur = db.cursor()
    cur.execute(
        "SELECT habit_name, streak_day_count, check_off_date FROM check_offs "
        "WHERE streak_day_count = (SELECT MAX(streak_day_count) FROM check_offs) "
        "ORDER BY check_off_date")
    fetch = cur.fetchall()

    # Check if no results were found
    if not fetch:
        return None

    # Collect all longest streaks in a list of dictionaries
    longest_streaks = []
    for row in fetch:
        longest_streaks.append({"habit": row[0], "streak": row[1], "last_date": row[2]})

    return longest_streaks


def hyper_streak_weekly(db):
    """
    Fetch all longest weekly streaks across habits.

    :param db: SQLite database connection object.
    :return: List of dictionaries containing habit name, streak count, last week, and last date.
    """
    cur = db.cursor()
    cur.execute(
        "SELECT habit_name, streak_week_count, calendar_week, check_off_date FROM check_offs "
        "WHERE streak_week_count = (SELECT MAX(streak_week_count) FROM check_offs) "
        "ORDER BY check_off_date")
    fetch = cur.fetchall()

    # Check if no results were found
    if not fetch:
        return None

    # Collect all longest streaks in a list of dictionaries
    longest_streaks = []
    for row in fetch:
        longest_streaks.append({"habit": row[0], "streak": row[1], "last_week": row[2], "last_date": row[3]})

    return longest_streaks
