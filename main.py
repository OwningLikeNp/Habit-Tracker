import questionary as qt
from habit import Habit
import analytics
import get

# Greeting message
print("*** Welcome ***")


# CLI Interface
def menu():
    """
    Command Line Interface (CLI) employing the questionary library 
    to elegantly present the application to the user.
    """
    # Choices for the user to choose from
    choices = [
        "Add/Remove Habit or Category",
        "Change Periodicity of a Habit",
        "Update Progress of a Habit",
        "Display Your Habits",
        "Display Analytics",
        "Exit"
    ]

    choice = qt.select("Select an Option:", choices=choices).ask()

    if choice == "Add/Remove Habit or Category":
        handle_add_remove()

    elif choice == "Change Periodicity of a Habit":
        handle_change_periodicity()

    elif choice == "Update Progress of a Habit":
        handle_update_progress()

    elif choice == "Display Your Habits":
        handle_display_habits()

    elif choice == "Display Analytics":
        handle_analytics()

    elif choice == "Exit":
        print("\nHappy Tracking! See you next time :)")  # Goodbye message
        exit()  # exit() completely exits the program


def handle_add_remove():
    """
    Function to add or remove a habit or category.
    Deleting  a category also removes all associated habits.
    """
    choices = [
        "Add Habit",
        "Remove Habit",
        "Remove Category",
        "Return to Main Menu"
    ]

    second_choice = qt.select("Choose an Option:",
     choices=choices).ask()

    if second_choice == "Add Habit":
        handle_add_habit()

    elif second_choice == "Remove Habit":
        handle_remove_habit()

    elif second_choice == "Remove Category":
        handle_remove_category()

    elif second_choice == "Return to Main Menu":
        menu()


def handle_add_habit():
    """
    Function to add a new habit and associated details.
    """
    habit_name = get.habit_name()
    habit_periodicity = get.habit_periodicity()
    habit_category = get.habit_category()

    habit = Habit(habit_name, habit_periodicity, habit_category)
    habit.add()

def handle_remove_habit():
    """
    Function to remove a habit.
    """
    try:
        habit_name = get.stored_habits()
    except ValueError:
        print("\nLooks empty in here! Please add a habit first.\n")
    else:
        habit = Habit(habit_name)
        if get.delete_habit(habit_name):
            habit.remove()
            
        else:
            print("\nReturning to Main Menu\n")


def handle_remove_category():
    """
    Function to remove a category.
    """
    try:
        habit_category = get.stored_categories()
    except ValueError:
        print("\nLooks empty in here! Please add a habit and its category first.\n")
    else:
        if get.delete_category(habit_category):
            habit = Habit(category=habit_category)
            habit.remove_category()
            
        else:
            print("\nReturning to Main Menu!\n")


def handle_change_periodicity():
    """
    Function to change periodicity of a habit.
    """
    try:
        habit_name = get.stored_habits()
    except ValueError:
        print("\nLooks empty in here! Please add a habit first.\n")
    else:
        new_periodicity = get.habit_periodicity()
        if get.change_periodicity():
            habit = Habit(habit_name, new_periodicity)
            habit.change_periodicity()
        else:
            print(f"\nPeriodicity of {habit_name} remains unchanged!\n")


def handle_update_progress():
    """
    Function to update progress of a habit.
    """
    try:
        habit_name = get.stored_habits()
    except ValueError:
        print("\nLooks empty in here! Please add a habit first to update its progress!\n")
    else:
        habit = Habit(habit_name)
        habit.update_progress()


def handle_display_habits():
    
    """
    Function to display list of stored habits.
    """
    second_choice = get.period_choices()

    if second_choice.startswith("View "):
        period = second_choice.split(" ", 1)[1].lower().replace(" habits", "")
        analytics.display_habits_data(period)
    elif second_choice == "Return to Main Menu":
        menu()



def handle_analytics():
    """
    Function to display analytics.
    """
    second_choice = get.analytics_choices()

    if second_choice == "View Streaks of All Habits":
        analytics.show_habit_streak_data()

    elif second_choice in ["View Longest Streak of a Habit", "View Streak Log of a Habit"]:
        try:
            habit_name = get.stored_habits()
        except ValueError:
            print("\nLooks empty in here! Please add a habit first\n")
        else:
            analytics.show_habit_streak_data(habit_name) if second_choice == "View Longest Streak of a Habit" else analytics.show_habit_logged_data(habit_name)

    elif second_choice == "Return to Main Menu":
        menu()



if __name__ == "__main__":
    while True:
        menu()
