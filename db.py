"""
The database module serves as the primary entity responsible for creating database tables, storing information, and facilitating the retrieval of data.
"""

import sqlite3


def connect_database(name="main.db"):
    """
    This function establishes and manages a connection with the database.

    name: Name of DB to create or connect to (default: main.db).
    returns: DB connection.
    """
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    """
    This function generates two database tables: 'habit_tracker' and 'habit_log'.
    The 'habit_tracker' database includes columns such as habit, periodicity, category, creation_time, streak, and completion_time. 
    The 'habit_log' database comprises columns like habit, completed, streak, and completion_time.
    param: 'db' To maintain the connection with the database.
    """
    cur = db.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS habit_tracker (
               habit TEXT PRIMARY KEY , 
               periodicity TEXT,
               category TEXT,
               creation_time TEXT,
               streak INT,
               completion_time TEXT   
           )''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS habit_log (
            habit TEXT,
            completed BOOL,
            streak INT DEFAULT 0,
            completion_time TIME,
            FOREIGN KEY (habit) REFERENCES habit_tracker(habit)
        )''')
    db.commit()


def add_habit(db, name, periodicity, category, creation_time, streak, progress_time=None):
    """
    This function inserts habit details into the 'habit_tracker' database.
    
    :param db: To maintain connection with DB.
    :param name: Name of habit.
    :param periodicity: Periodicity of habit.
    :param category: Category of habit.
    :param creation_time: Habit creation time.
    :param streak: Habit streak.
    :param progress_time: Time when progress on habit was updated.
    """
    cur = db.cursor()
    cur.execute("INSERT INTO habit_tracker VALUES(?, ?, ?, ?, ?, ?)",
                (name, periodicity, category,
                 creation_time, streak, progress_time))
    db.commit()


def update_log(db, name, is_progressed, streak, progress_time):
    """
    This function modifies the 'habit_log' database using the provided information.

    :param db: To maintain connection with DB.
    :param name: Name of habit.
    :param is_progressed: Indicates whether progress has been made on habit.
    :param streak: Habit streak.
    :param progress_time: Time when progress on habit was updated.
        """
    cur = db.cursor()
    cur.execute("INSERT INTO habit_log VALUES(?, ?, ?, ?)",
                (name, is_progressed, streak, progress_time))
    db.commit()


def habit_exists(db, name):
    """
    This function examines whether the specified habit is present in the database or not.

    :param db: To maintain connection with DB.
    :param name: Name of habit.
    :return: True if habit is already in the database; False otherwise.
    """
    cur = db.cursor()
    query = """SELECT * FROM habit_tracker WHERE habit = ?"""
    cur.execute(query, (name,))
    data = cur.fetchone()
    return True if data is not None else False


def remove_habit(db, name):
    """
    This function removes the specified habit from habit_tracker database.
    Also simultaneously resets the log for that particular habit.

    :param db: To maintain connection with DB.
    :param name: Name of habit.
    """
    cur = db.cursor()
    cur.execute(f"DELETE FROM habit_tracker WHERE habit == '{name}';")
    db.commit()
    reset_logs(db, name)


def fetch_categories(db):
    """
    This function retrieves all categories stored in habit_tracker database.

    :param db: To maintain connection with DB.
    :return: List of category names.
    """
    cur = db.cursor()
    cur.execute("SELECT category FROM habit_tracker")
    data = cur.fetchall()
    return [i[0].capitalize() for i in set(data)]


def remove_category(db, category_name):
    """
    This function removes the specified category and associated habits from habit_tracker database.

    :param db: To maintain connection with DB.
    :param category_name: Name of category
    """
    cur = db.cursor()
    cur.execute(f"DELETE FROM habit_Tracker where category == '{category_name}';")
    db.commit()


def fetch_habits(db):
    """
    This function retrieves all habits stored in habit_tracker database.

    :param db: To maintain connection with DB.
    :return: List of habit names
    """
    cur = db.cursor()
    cur.execute("SELECT habit FROM habit_tracker")
    data = cur.fetchall()
    return [i[0].capitalize() for i in set(data)] if len(data) > 0 else None


def update_periodicity(db, name, new_periodicity):
    """
    This function the periodicity of the specified habit to a new setting and concurrently resets the logs associated with that habit.

    :param db: To maintain connection with DB.
    :param name: Name of habit.
    :param new_periodicity: New periodicity to be assigned to habit
    """
    cur = db.cursor()
    query = "UPDATE habit_tracker SET periodicity = ?, streak = 0, completion_time = NULL WHERE habit = ?"
    data = (new_periodicity, name)
    cur.execute(query, data)
    db.commit()
    reset_logs(db, name)


def get_streak_count(db, name):
    """
    This function returns  current streak of specified habit.

    :param db: To maintain connection with DB.
    :param name: Name of habit.
    :return: Current streak of specified habit.
    """
    cur = db.cursor()
    query = "SELECT streak FROM habit_tracker WHERE habit = ?"
    cur.execute(query, (name,))
    streak_count = cur.fetchall()
    return streak_count[0][0]


def update_habit_streak(db, name, streak, time=None):
    """
    This function updates streak of specified habit.

    :param db: To maintain connection with DB.
    :param name: Name of habit.
    :param streak: streak of habit
    :param time: Time when streak was updated
    """
    cur = db.cursor()
    query = "UPDATE habit_tracker SET streak = ?, completion_time = ? WHERE habit = ?"
    data = (streak, time, name)
    cur.execute(query, data)
    db.commit()


def reset_logs(db, name):
    """
    This function resets log entries of specified habit.

    :param db: To maintain connection with DB.
    :param name: Name of the habit
    """
    cur = db.cursor()
    query = "DELETE FROM habit_log WHERE habit = ?"
    cur.execute(query, (name,))
    db.commit()


def habit_progress_time(db, name):
    """
    This function returns last time a habit's progress was updated.

    :param db: To maintain connection with DB.
    :param name: Name of habit.
    :return: Last time progress was updated
    """
    cur = db.cursor()
    query = "SELECT completion_time FROM habit_tracker WHERE habit = ?"
    cur.execute(query, (name,))
    data = cur.fetchall()
    return data[0][0]


def fetch_habit_periodicity(db, habit_name):
    """
    This function returns periodicity of specified habit.

    :param db: To maintain connection with DB.
    :param name: Name of habit.
    :return: Periodicity of specified habit.
    """
    cur = db.cursor()
    query = "SELECT periodicity FROM habit_tracker WHERE habit =?"
    cur.execute(query, (habit_name,))
    data = cur.fetchall()
    return data[0][0]
