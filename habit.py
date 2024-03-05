import db
from datetime import datetime


class Habit:
    """
        Habit class to maintain habit data
    """
    DATE_FORMAT = "%m/%d/%Y %H:%M"
    def __init__(self, name: str = None, periodicity: str = None, category: str = None, database="main.db"):
        """
        Parameters
        ----------
        name : str, default: None
            The habit's name.
        periodicity : str, default: None
            The habit's frequency (daily, weekly, or monthly).
        category : str, default: None
            The category to which the habit belongs.
        database: str, default: main.db
            The database connection for running tests.
                """

        self.name = name
        self.periodicity = periodicity
        self.category = category
        self.db = db.connect_database(database)
        self.streak = 0
        self.current_time = datetime.now().strftime(self.DATE_FORMAT)

    def add(self):
        """
        Function to update habit details to DB and update log
        """
        if not db.habit_exists(self.db, self.name):
            db.add_habit(self.db, self.name, self.periodicity, self.category, self.current_time, self.streak)
            db.update_log(self.db, self.name, False, 0, self.current_time)
            print(f"\nYour Habit '{self.name.capitalize()}' as a '{self.periodicity.capitalize()}' "
                  f"Habit in '{self.category.capitalize()}' category has been completed.\n")
        else:
            print("\nLooks like you already have this habit! Please choose a different one.\n")

    def remove(self):
        """
        Function to remove a habit from DB.
        """
        db.remove_habit(self.db, self.name)
        print(f"\nYour habit '{self.name.capitalize()}' has been removed.\n")

    def change_periodicity(self):
        """
        Function to change periodicity of a habit
        """
        db.update_periodicity(self.db, self.name, self.periodicity)
        db.update_log(self.db, self.name, False, 0, self.current_time)
        print(f"\nPeriodicity of habit '{self.name.capitalize()}' has been changed to '{self.periodicity.capitalize()}'\n")
    
    def remove_category(self):
        """
        Fuction to delete a category and its associated habits.
        """
        db.remove_category(self.db, self.category)
        print(f"\nYour category '{self.category.capitalize()}' and its associated habits have been removed.\n")

    
    def reset_streak(self):
        """
        Function to reset a habit streak to 1 in the case where habit progress was not updated within defined period.
        """
        self.streak = 1
        db.update_habit_streak(self.db, self.name, self.streak, self.current_time)
        db.update_log(self.db, self.name, False, db.get_streak_count(self.db, self.name), self.current_time)
        print("\nOh dear! It seems you missed your streak. Don't worry; your streak has been reset. Let's try to keep the streak going this time!")
        print(f"Streak of babit '{self.name.capitalize()}' is now {self.streak} because you completed it.\n")


    def update_streak(self):
        """
        Function to increment streak by 1 and update DB.
        """
        self.streak = db.get_streak_count(self.db, self.name)
        self.streak += 1
        db.update_habit_streak(self.db, self.name, self.streak, self.current_time)
        db.update_log(self.db, self.name, True, db.get_streak_count(self.db, self.name), self.current_time)
        print(f"\nGreat! Your new streak for habit '{self.name.capitalize()}' is {self.streak}\n")


    
   
    def update_progress(self):
        """
        Function to update progress on a habit. 
        Checks if progress has been made within defined periodicity and increments or resets streak accordingly

        """
        # Daily Streak Tracker & Assignment
        if db.fetch_habit_periodicity(self.db, self.name) == "daily":
            if self.daily_habit_streak_verification() == 0:
                print("\nProgress for this habit has already been updated today. Let's do it again tomorrow!\n")
            elif self.daily_habit_streak_verification() == 1:
                self.update_streak()
            else:
                self.reset_streak()

        # Weekly Streak Tracker & Assignment
        elif db.fetch_habit_periodicity(self.db, self.name) == "weekly":
            if self.weekly_habit_streak_verification() == 1:
                print("\nProgress for this habit has already been updated this week. Let's do it again next week!\n")
            elif self.weekly_habit_streak_verification() == 2:
                self.update_streak()
            else:
                self.reset_streak()

        # Monthly Streak Tracker & Assignment
        elif db.fetch_habit_periodicity(self.db, self.name) == "monthly":
            if self.monthly_habit_streak_verification() == 0:
                print("\nProgress for this habit has already been updated this month. Let's do it again next month!.\n")
            elif self.monthly_habit_streak_verification() == 1:
                self.update_streak()
            else:
                self.reset_streak()

    def monthly_habit_streak_verification(self):
        """
        Function to update progress of monthly habits.
        :return months: Number of month(s) since last completion of habit
        """
        last_visit = db.habit_progress_time(self.db, self.name)
        previous_streak = db.get_streak_count(self.db, self.name)
        
        if previous_streak == 0 or last_visit is None:
            return 1
        else:
            current_month = self.current_time
            month = int(current_month[:2]) - int(last_visit[:2])
            print(month)
            return month

    def weekly_habit_streak_verification(self):
        """
        Function to update progress of weekly habits.
        :return week: Number of week(s) since last completion of habit
        """
        last_streak = db.habit_progress_time(self.db, self.name)
        previous_streak = db.get_streak_count(self.db, self.name)
        
        if previous_streak == 0 or last_streak is None:
            return 2
        else:
            today = self.current_time
            delt = datetime.strptime(today[:10], "%m/%d/%Y") - datetime.strptime(last_streak[:10], "%m/%d/%Y")
            week = 3 if (delt.days + 1) > 14 else (2 if (delt.days + 1) > 7 else 1)
            return week

    def daily_habit_streak_verification(self):
        """
        Function to update progress of dailyg habits.
        :return date.days: Number of day(s) since last completion of habit
        """
        last_visit = db.habit_progress_time(self.db, self.name)
        previous_streak = db.get_streak_count(self.db, self.name)
        
        if previous_streak == 0 or last_visit is None:
            return 1
        else:
            today = self.current_time
            date = datetime.strptime(today[:10], "%m/%d/%Y") - datetime.strptime(last_visit[:10], "%m/%d/%Y")
            return date.days



