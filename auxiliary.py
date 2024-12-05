# print in colors from https://www.geeksforgeeks.org/print-colors-python-terminal/
def print_red(text):
    print("\033[91m {}\033[00m".format(text))

def print_green(text):
    print("\033[92m {}\033[00m".format(text))

def print_yellow(text):
    print("\033[93m {}\033[00m".format(text))

# written input validation from https://questionary.readthedocs.io/en/stable/pages/advanced.html#validation
def input_validator(max_length):
    def validate(input):
        if len(input) == 0:
            return "Don't leave this empty"
        elif len(input) > max_length:
            return f"No more than {max_length} characters, please."
        else:
            return True
    return validate

helptext = """
\033[1mHelp Center\033[22m

Welcome to the Habit Tracker Help Center! Below you’ll find guidance on how to use the features in the application.

---

\033[1mMAIN MENU OPTIONS\033[22m

\033[1m1. Create New Habit\033[22m  
- Use this option to add a new habit.  
- You will be prompted to:  
  1. Enter the name of the habit.  
  2. Choose the periodicity: daily or weekly.  
  3. Provide a short description of the habit.  
- The habit will be saved and available for tracking.  

\033[1m2. Check-Off Habit\033[22m  
- This allows you to mark a habit as completed for the current day or week.  
- Steps:  
  1. Choose the periodicity (daily or weekly).  
  2. Select a habit from the list of habits not yet checked off.  
  3. Once checked off, the habit will count toward your streak.  

\033[1m3. Remove Habit\033[22m  
- Select this option to delete a habit and all its related data, including check-offs.  
- Be careful—this action cannot be undone.  

\033[1m4. Statistics Menu\033[22m  
Dive deeper into your habits and streaks with the following options:  
1. \033[1mView Your Habits:\033[22m  
   - Display all habits or habits with the same periodicity (daily or weekly).  
2. \033[1mIndividual Habit & Streak Analysis:\033[22m  
   - Analyze a specific habit's performance.  
   - View all past check-offs, your current streak and your longest streak.
   - Note that by design there can only be a current streak if you checked off your habit for today/this week.
   - The longest streak shows your best streak for a given habit, highlighting the most recent one in case of a tie.  
3. \033[1mYour Record Streaks:\033[22m  
   - See your longest overall streaks for both daily and weekly habits.  
   - In case of a tie, it shows all of the longest streaks.

\033[1m5. Helpcenter\033[22m  
- Displays this guide.  

\033[1m5. Mock Data\033[22m  
- Load (or delete) preconfigured mock data to explore and fully understand the app's functionality. 

\033[1m6. Exit\033[22m  
- Close the application.  

---

\033[1mGeneral Tips\033[22m  
1. \033[1mUser Experience:\033[22m For optimal readability, maximize your terminal window. 
1. \033[1mCheck Regularly:\033[22m Ensure you mark your habits on time to maintain streaks. You can't check-off past days. 
2. \033[1mPredefined Habits:\033[22m They will be only installed on your first use. If you don't need them, remove them!
3. \033[1mAnalyze Progress:\033[22m Use the statistics features to stay motivated.  

---

If you have any questions, feel free to revisit this guide via the \033[1mHelpcenter\033[22m in the MAIN MENU. Let’s build great habits together!
"""

