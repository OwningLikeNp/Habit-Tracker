from db import add_habit, connect_database, fetch_habits, habit_exists, remove_habit, \
    fetch_categories, update_periodicity, fetch_habit_periodicity, update_habit_streak, get_streak_count


class TestDatabase:
    """
    TestDatabase class contains method that tests the important functions of db module
    """

    def setup_method(self):
        self.db = connect_database("test_db.db")
        # Total 6 habits and 6 categories
        add_habit(self.db, "running", "daily", "health", "12/17/2023 20:13", 0)
        add_habit(self.db, "saving", "monthly", "finance", "12/17/2023 20:13", 0)
        add_habit(self.db, "socialize", "weekly", "life", "12/17/2023 20:13", 0)
        add_habit(self.db, "cleaning", "daily", "chores", "12/17/2023 20:13", 0)
        add_habit(self.db, "reading", "weekly", "growth", "12/17/2023 20:13", 0)
        add_habit(self.db, "gaming", "daily", "fun", "12/17/2023 20:13", 0)

    def test_fetch_habits_as_choices(self):
        assert len(fetch_habits(self.db)) == 6

    def test_fetch_categories(self):
        assert len(fetch_categories(self.db)) == 6

    def test_remove_habit(self):
        remove_habit(self.db, "gaming")
        assert habit_exists(self.db, "gaming") is False
        assert len(fetch_habits(self.db)) == 5

    def test_update_periodicity(self):
        update_periodicity(self.db, "reading", "daily")
        assert fetch_habit_periodicity(self.db, "reflection") == "daily"

    def test_update_habit_streak(self):
        update_habit_streak(self.db, "running", 1, "12/18/2023 15:00")
        assert get_streak_count(self.db, "running") == 1

    def teardown_method(self):
        self.db.close()
        import os
        os.remove("test_db.db")
