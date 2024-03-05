import pytest
from habit import Habit
from db import add_habit, connect_database, fetch_habits, habit_exists, remove_habit, \
    fetch_categories, fetch_habit_periodicity, update_habit_streak, get_streak_count, remove_category
from freezegun import freeze_time


@pytest.fixture(scope='module')
def db():
    db = connect_database("test_habit.db")
    print("Creating temporary DB file for testing.\n")
    print("Starting tests...\n")
    yield db
    print('-----TEARDOWN-----')
    print("\nConnection with test DB closed.\n")
    db.close()
    import os
    os.remove("test_habit.db")
    print("\nRemoved temporary DB file for testing.")
    print("\nTest completed")


def test_add(db):
    habit = Habit("running", "daily", "health", database="test_habit.db")
    habit.add()
    habit1 = Habit("reading", "weekly", "growth", database="test_habit.db")
    habit1.add()
    assert habit_exists(db, "running")
    assert habit_exists(db, "reading")

def test_change_periodicity(db):
    assert fetch_habit_periodicity(db, "reading") == "daily"
    habit1 = Habit("reading", "weekly", database="test_habit.db")
    habit1.change_periodicity()
    assert fetch_habit_periodicity(db, "reading") == "weekly"

def test_remove(db):
    assert habit_exists(db, "running") is True
    habit = Habit("running", "daily", "health", database="test_habit.db")
    habit.remove()
    assert habit_exists(db, "running") is False


def test_remove_category(db):
    assert len(fetch_categories(db)) == 1
    habit3 = Habit("Movies", "weekly", "fun", database="test_habit.db")
    habit3.add()
    assert len(fetch_categories(db)) == 2
    habit3.remove_category()
    assert len(fetch_categories(db)) == 1


# Time format (YYYY-MM-DD)
@freeze_time("2023-12-17")
def test_add_custom_habits(db):
    habit4 = Habit("cycling", "weekly", "health", database="test_habit.db")
    habit4.add()
    habit5 = Habit("party", "monthly", "fun", database="test_habit.db")
    habit5.add()
    habit6 = Habit("dishes", "daily", "chores", database="test_habit.db")
    habit6.add()
    assert habit_exists(db, "cycling")


@freeze_time("2023-12-17")
def test_mark_habit4_as_completed(db):
    habit4 = Habit("cycling", "weekly", "health", database="test_habit.db")
    habit4.update_progress()
    assert get_streak_count(db, "cycling") == 1


@freeze_time("2023-12-17")
def test_mark_habit4_as_completed_again(db):
    habit4 = Habit("cycling", "weekly", "health", database="test_habit.db")
    habit4.update_progress()
    assert get_streak_count(db, "cycling") != 2


@freeze_time("2023-12-18")
def test_mark_habit4_as_completed_next_day(db):
    habit4 = Habit("cycling", "weekly", "health", database="test_habit.db")
    habit4.update_progress()
    assert get_streak_count(db, "cycling") == 2


@freeze_time("2023-12-17")
def test_mark_habit5_as_completed(db):
    assert get_streak_count(db, "party") == 0
    habit5 = Habit("party", "monthly", "fun", database="test_habit.db")
    habit5.update_progress()
    assert get_streak_count(db, "party") == 1


# Testing a day later
@freeze_time("2023-12-18")
def test_mark_habit5_as_completed_next_day(db):
    habit5 = Habit("party", "monthly", "fun", database="test_habit.db")
    habit5.update_progress()
    assert get_streak_count(db, "party") != 2


# Testing a week later
@freeze_time("2023-12-24")
def test_mark_habit5_as_completed_next_week(db):
    habit5 = Habit("party", "monthly", "fun", database="test_habit.db")
    habit5.update_progress()
    assert get_streak_count(db, "party") == 2


@freeze_time("2023-12-17")
def test_mark_habit6_as_completed(db):
    habit6 = Habit("dishes", "daily", "chores", database="test_habit.db")
    habit6.update_progress()
    assert get_streak_count(db, "dishes") == 1


# Testing 10 days later
@freeze_time("2023-12-27")
def test_mark_habit6_as_completed_10days_later(db):
    habit6 = Habit("dishes", "daily", "chores", database="test_habit.db")
    habit6.update_progress()
    assert get_streak_count(db, "dishes") != 2


# Testing a month later
@freeze_time("2024-01-17")
def test_mark_habit6_as_completed_month_later(db):
    habit6 = Habit("dishes", "daily", "chores", database="test_habit.db")
    habit6.update_progress()
    assert get_streak_count(db, "dishes") == 2
