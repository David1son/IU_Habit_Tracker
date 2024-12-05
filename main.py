import questionary
from datetime import date, timedelta
from auxiliary import print_green, print_red, print_yellow, input_validator, helptext
from habit import Habit
from database import get_db, display_habits_table, display_check_offs_table, fetch_habit_from_db
from analyse import hyper_streak_daily, hyper_streak_weekly
from loading import load_mock_data, load_predefined_habits


def statistics_loop(db):
    """
    Handles the STATISTICS menu and its sub-options.
    Options include viewing habits, analyzing individual habits, and viewing record streaks.

    :param db: an initialized sqlite3 database connection
    """
    cur = db.cursor()
    stats = True
    while stats:
        # Display the statistics menu
        stats_choice = questionary.select(
            "STATISTICS MENU: please choose",
            choices=["View Your Habits", "Individual Habit & Streak Analysis", "Your Record Streaks", "BACK TO MAIN MENU"],
        ).ask()

        if stats_choice == "View Your Habits":
            periodicity = questionary.select(
                "\nWhich Habits do you want to view?",
                choices=["daily", "weekly", "all"],
            ).ask()
            if periodicity == "all":
                # Use default function and don't filter
                print_yellow(display_habits_table(db))
            else:
                print_yellow(display_habits_table(db, periodicity))

            questionary.text("Press Enter to go back to STATISTICS.").ask()


        elif stats_choice == "Individual Habit & Streak Analysis":
            # user chooses habit name
            cur.execute(
                "SELECT name, periodicity FROM habits ORDER BY periodicity, name COLLATE NOCASE")  # Fetch unique habit names, nocase for case insentivity
            unique_habits_list = [n[0] for n in cur.fetchall()]

            if not unique_habits_list:
                print_red("\nThere are no stored habits in the app.")
            else:
                name = questionary.select(
                    "\nWhich habit do you want to take a closer look at?",
                    choices=unique_habits_list).ask()

                # restore habit
                habit_attributes = fetch_habit_from_db(db, name)
                habit = Habit(habit_attributes[0], habit_attributes[1], habit_attributes[2], habit_attributes[3])
                periodicity = habit.periodicity

                # retun prettytable with all check offs
                print_yellow(display_check_offs_table(db, name, periodicity))

                # current streak handling
                cur_streak_dict = habit.current_streak(db)
                if cur_streak_dict["current_streak"] == 0:
                    print_red(cur_streak_dict["message"])
                else:
                    print_green(cur_streak_dict["message"])

                # longest streak handling
                long_streak_dict = habit.longest_streak(db)
                if long_streak_dict["longest_streak"] == 0:
                    print_red(long_streak_dict["message"])
                else:
                    print_green(long_streak_dict["message"])

                questionary.text("Scroll up to see all checked-off dates. Press Enter to go back to STATISTICS.").ask()


        elif stats_choice == "Your Record Streaks":
            # Display daily streak(s)
            streak_daily = hyper_streak_daily(db)
            if not streak_daily:
                print_red("\nYou don't have any daily streak. Start checking a daily habit off!")
            else:
                occasions = len(streak_daily)
                # differentiate between 1 vs many longest daily streaks
                if occasions == 1:
                    print_green(f"\nYou achieved your longest daily streak of \033[1m{streak_daily[0]['streak']}\033[22m day(s) "
                                f"with \"{streak_daily[0]['habit']}\", last checked-off on {streak_daily[0]['last_date']}.")
                else:
                    print_green(f"\nYou have {occasions} different longest daily streaks with \033[1m{streak_daily[0]['streak']}\033[22m day(s).\n") # just take the streak count from the first entry in the dictionary
                    for index, entry in enumerate(streak_daily, 1):
                        print_green(f"{index}. \"{entry['habit']}\"-streak, last checked-off on {entry['last_date']}.")

            # Display weekly streak(s)
            streak_weekly = hyper_streak_weekly(db)
            if not streak_weekly:
                print_red("\nYou don't have any weekly streak. Start checking a weekly habit off!")
            else:
                occasions = len(streak_weekly)
                # differentiate between 1 vs many longest weekly streaks
                if occasions == 1:
                    print_green(f"\nYou achieved your longest weekly streak of \033[1m{streak_weekly[0]['streak']}\033[22m week(s) "
                        f"with \"{streak_weekly[0]['habit']}\", last checked-off in week {streak_weekly[0]['last_week']} on {streak_weekly[0]['last_date']}.")
                else:
                    print_green(f"\nYou have {occasions} different longest weekly streaks with \033[1m{streak_weekly[0]['streak']}\033[22m week(s).\n")
                    for index, entry in enumerate(streak_weekly, start=1):
                        print_green(f"{index}. \"{entry['habit']}\"-streak, last checked-off in week {entry['last_week']} on {entry['last_date']}.")

            questionary.text("Press Enter to go back to STATISTICS.").ask()

        else:  # Back to Main Menu
            stats = False



def main_loop():
    """
    Handles the MAIN MENU and its sub-options.

    The main menu provides options to manage habits, view statistics, and load/delete mock data.
    """

    db = get_db()
    cur = db.cursor()
    stop = False
    while not stop:
        today = date.today()
        year, week, _ = today.isocalendar()
        calendar_week = f"{week}-{year}"
        cur.execute("SELECT name FROM habits ORDER BY name COLLATE NOCASE")  # give me all unique habit names ordered case-insensitively
        unique_habits_list = [n[0] for n in cur.fetchall()]  # list of unique names

        choice = questionary.select(
            "\nMAIN MENU: please choose",
            choices=["Create New Habit", "Check-Off Habit", "Remove Habit",
                     "STATISTICS MENU", "Helpcenter", "Mock Data", "Exit"]).ask()

        if choice == "Helpcenter":
            print_green("\n" + helptext)
            questionary.text("\nScroll up to read.\nPress Enter to go back to MAIN MENU").ask()

        elif choice == "Create New Habit":
            # restrict name to 30 characters
            name = questionary.text("What's the name of your new habit?",validate=input_validator(30)).ask()
            if name in unique_habits_list:
                # abort if name exists already
                print_red(f'\nA habit named "{name}" already exists.')
            else:
                periodicity = questionary.select("Which Periodicity?", choices=["daily", "weekly"]).ask()
                # restrict description to 70 characters
                desc = questionary.text("What's the description of your habit?",validate=input_validator(70)).ask()
                habit = Habit(name, desc, periodicity)
                habit.store(db)
                print_green(f'\nThe new {periodicity} habit "{name}" has been created.')

        elif choice == "Check-Off Habit":
            periodicity = questionary.select(
                "Which kind of habit do you want to check-off?",
                choices=["daily","weekly"]).ask()

            if periodicity == "daily":
                today1 = str(today) # to prevent error for the sqlite query execution

                # only select habits that haven't been checked-off today
                cur.execute("""SELECT name FROM habits WHERE periodicity = 'daily' AND name NOT IN (SELECT habit_name FROM check_offs 
                                                WHERE check_off_date = ?) ORDER BY name COLLATE NOCASE""", (today1,))
                check_off_choices = [n[0] for n in cur.fetchall()]
                if not check_off_choices:
                    print_red("\nThere are no habits to check off today. Maybe you checked them all off already?")
                    continue
                else:
                    check_off_choices.append("CANCEL & BACK TO MAIN MENU")
                    name = questionary.select(
                    "Which habit do you want to check-off?",
                    choices=check_off_choices).ask()
                    if name == "CANCEL & BACK TO MAIN MENU":
                        continue
                    else:
                        # restore habit from name and check it off
                        habit_attributes = fetch_habit_from_db(db,name)
                        habit = Habit(habit_attributes[0],habit_attributes[1],habit_attributes[2],habit_attributes[3])
                        habit.check_off(db)
                        print_green(f'\nCongrats, you completed "{name}" for today!')

            else:  # periodicity == weekly
                # only select habits that haven't been checked-off this week
                cur.execute("""SELECT name FROM habits WHERE periodicity = 'weekly' AND 
                name NOT IN (SELECT habit_name FROM check_offs WHERE calendar_week = ?) ORDER BY name COLLATE NOCASE""",
                            (calendar_week,))

                check_off_choices = [n[0] for n in cur.fetchall()]
                if not check_off_choices:
                    print_red("\nThere are no habits to check off for this week. Maybe you checked them all off already?")
                    continue
                else:
                    check_off_choices.append("CANCEL & BACK TO MAIN MENU")
                    name = questionary.select(
                        "Which habit do you want to check-off?",
                        choices=check_off_choices).ask()
                    if name == "CANCEL & BACK TO MAIN MENU":
                        continue
                    else:
                        # restore habit from name and check it off
                        habit_attributes = fetch_habit_from_db(db, name)
                        habit = Habit(habit_attributes[0], habit_attributes[1], habit_attributes[2], habit_attributes[3])
                        habit.check_off(db)
                        print_green(f'\nCongrats, you completed "{name}" for this week!')




        elif choice == "Remove Habit":
            name = questionary.select(
                "\nWhich habit do you want to remove?",
                choices=unique_habits_list + ["CANCEL & BACK TO MAIN MENU"]).ask()
            if name == "CANCEL & BACK TO MAIN MENU":
                continue
            else:
                security_check = questionary.confirm("Are you sure? Deletion of a habit can't be undone.").ask()
                if security_check == False:
                    continue
                else:
                    cur.execute("DELETE FROM habits WHERE name=?", (name,))
                    cur.execute("DELETE FROM check_offs WHERE habit_name=?", (name,))
                    db.commit()
                    print_green(f'\nYour habit "{name}" and all the related data has been deleted from the application.')

        elif choice == "STATISTICS MENU":
            statistics_loop(db)

        elif choice == "Mock Data":
            mock_choice = questionary.select(
                "\nWhat do you want to do?",
                choices=["Load Mock Data","Delete Mock Data", "CANCEL & BACK TO MAIN MENU"]).ask()
            if mock_choice == "CANCEL & BACK TO MAIN MENU":
                continue
            elif mock_choice == "Load Mock Data":
                load_mock_data()
                print_green("\nMock habits have been successfully added to the app. \nYou can check them off and explore their details in the Statistics menu.")
            else: # "Delete Mock Data"
                cur.execute("DELETE FROM habits WHERE name LIKE ?", ("MOCK%",)) # name starts with "MOCK"
                cur.execute("DELETE FROM check_offs WHERE habit_name LIKE ?", ("MOCK%",))
                db.commit()
                print_green("\nMock data has been deleted successfully.")


        else: # Exit
            print("Bye")
            stop = True


if __name__ == "__main__":
    load_predefined_habits()
    main_loop()
