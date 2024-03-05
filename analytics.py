"""
The analytics module displays habit streaks and logs

"""

from db import connect_database


def data_of_habits(db, periodicity) -> list:
    """
    Function to retrieve list of stored habits with specified periodicity.

    :param db: To maintain connection with DB.
    :param periodicity: Specified periodicity
    :return: List of stored habits with specified periodicity.
    """
    
    cur = db.cursor()
    if periodicity=="all":
        cur.execute("SELECT * FROM habit_tracker")
    else:    
        query = "SELECT * FROM habit_tracker WHERE periodicity = ?"
        cur.execute(query, (periodicity,)) 
    
    return  cur.fetchall()
    


def data_of_single_habit(db, habit_name) -> list:
    """
    Function to retrieve data of a specified habit.

    :param db: To maintain connection with DB.
    :param habit_name: Name of habit.
    :return: Data of specified habit
    """
    cur = db.cursor()
    query = "SELECT * FROM habit_tracker WHERE habit = ?"
    cur.execute(query, (habit_name,))
    return cur.fetchall()
    


def longest_habit_streak(db, habit_name) -> int:
    """
    Function to get longest habit streak from habit log.

    :param db: To maintain connection with DB.
    :param habit_name: Name of habit.
    :return: Longest streak of habit
    """
    cur = db.cursor()
    query = "SELECT MAX(streak) FROM habit_log WHERE habit = ?"
    cur.execute(query, (habit_name,))
    data = cur.fetchone()
    return data[0]


def habit_log(db, habit_name) -> list:
    """
    Function to fetch habit log of specified habit.

    :param db: To maintain connection with DB.
    :param habit_name: Name of habit.
    :return: Log of specified habit.
    """
    cur = db.cursor()
    query = "SELECT * FROM habit_log WHERE habit = ?"
    cur.execute(query, (habit_name,))
    return cur.fetchall()
    


# Table to show periodicity wise habit's data without streak
def display_habits_data(periodicity=None):
    """
    Function to show habit data in tabular format.

    :param periodicity: To display habits of specified periodicity. Empty param will display all habits.
    """
    db = connect_database()
    data = data_of_habits(db, periodicity)
    
    if len(data) > 0:
        # Uses string formatting to set columns and rows for the table
        print("\n{:<15} {:<15} {:<15} {:<15}".format("Name", "Periodicity", "Category", "Date/Time"))
        print("-----------------------------------------------------------------")
        for row in data:
            print("{:<15} {:<15} {:<15} {:<15}".format(
                row[0].capitalize(),  # Name
                row[1].capitalize(),  # Periodicity
                row[2].capitalize(),  # Streak
                row[3].capitalize()))  # Completion TIme
        print("-----------------------------------------------------------------\n")

    else:
        print("\nLooks empty in here! Please add a habit first.\n")


# Table to show habit's streak along with other columns
def show_habit_streak_data(habit=None):
    """
    
    Fuction to show streak data of a habit in tabular format.

    :param habit: To display streak of specified habit. Empty param will display current streak of all habits.
    """

    db = connect_database()
    if habit is None:
        data = data_of_habits(db, "all")
    else:    
        data = data_of_single_habit(db, habit)
    if len(data) > 0:
        # Uses string formatting to set columns and rows for the table
        print("\n{:<15} {:^15} {:>15} {:>15}".format("Name |", "Periodicity |", "Completion Time |",
                                                     "Current Streak" if habit is None else "Longest Streak"))
        print(f"{'_' * 70}")  # Print dashes - 70 times to pretty format the table
        for row in data:
            period = " Day(s)" if row[1] == "daily" else (" Week(s)" if row[1] == "weekly" else " Month(s)")
            print("{:<15} {:^15} {:>15} {:^15}".format(
                row[0].capitalize(),  # Name
                row[1].capitalize(),  # Periodicity
                row[5] if row[5] is not None else "--/--/-- --:--",  # Completion Time
                str(row[4]) + period if habit is None else str(longest_habit_streak(db, habit)) + period))  # Current or Longest Streak
            print(f"{'_' * 70}\n")
    else:
        print("\nLooks empty in here! Please add a habit first.\n")


# Displays habits log
def show_habit_logged_data(name_of_habit):
    """
        Function to show log of specified habit in tabular format.

        :param name_of_habit: To display logged data of specified habit.
        """
    db = connect_database()
    data = habit_log(db, name_of_habit)
    print(f"\n{'-' * 75}")  # Print dashes - 75 times to pretty format the table
    if len(data) > 0:
        for row in data:
            print(f"Habit: {row[0].capitalize()} | "
                  f"Completed : {'True' if row[1] == 1 else 'False'} | "
                  f"Streak: {row[2]} | Logged at: {row[3]}")
    else:
        print("No record found!")
    print(f"{'-' * 75}\n")
