import questionary as qt
from db import connect_database, fetch_categories, fetch_habits

def habit_name():
    """
    Function to get name of habit.
    """
    return qt.text(
        "Enter name of Habit:",
        validate=lambda name: name.isalpha() and len(name) > 1,
    ).ask().lower()

def habit_category():
    """
    Function to get name of category.
    """
    return qt.text(
        "Enter name of Category:",
        validate=lambda category: category.isalpha() and len(category) > 1,
    ).ask().lower()


def habit_periodicity():
    """
    Function to get periodicity of habit.
    """
    return qt.select(
        "Select periodicity of Habit",
        choices=["Daily", "Weekly", "Monthly"],
    ).ask().lower()


def stored_categories():
    """
    Function to retrieve all stored categories.
    """
    db = connect_database()
    arr = fetch_categories(db)
    if arr:
        return qt.select("Select a Category", choices=sorted(arr)).ask().lower()
    raise ValueError("Looks empty in here; Please add a habit and its category first")

def change_periodicity():
    """
    Function to confirm periodicity change.
    """
    return qt.confirm(
        "Modifying periodicity will reset habit streak. Do you want to continue?"
    ).ask()


def delete_category(habit_category):
    """
    Function to confirm deletion of category.
    """
    return qt.confirm(
        f"Deleting '{habit_category.capitalize()}' will delete all associated habits. Do you want to continue?"
    ).ask()


def delete_habit(habit_name):
    """
    Function to confirm deletion of habit.
    """
    return qt.confirm(f"Do you want to delete '{habit_name.capitalize()}' habit?").ask()

def stored_habits():
    """
    Function to retrieve all stored habits.
    """
    db = connect_database()
    list_of_habits = fetch_habits(db)
    if list_of_habits:
        return qt.select("Please Select a Habit", choices=sorted(list_of_habits)).ask().lower()
    raise ValueError("No habit in database; Add a habit first to use this function")

def analytics_choices():
    """
    Function to display choices in analytics menu.
    """
    return qt.select(
        "Select an option:",
        choices=[
            "View Streaks of All Habits",
            "View Longest Streak of a Habit",
            "View Streak Log of a Habit",
            "Back to Main Menu",
        ],
    ).ask()


def period_choices():
    """
    Function to display period choices in display habit menu.
    """
    return qt.select(
        "Select an option:",
        choices=[
            "View All Habits",
            "View Daily Habits",
            "View Weekly Habits",
            "View Monthly Habits",
            "Back to Main Menu",
        ],
    ).ask()

