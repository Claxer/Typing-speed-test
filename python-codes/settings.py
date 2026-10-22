from database import get_setting, set_setting


def get_daily_goal():
    return int(get_setting("daily_goal", "3"))


def update_daily_goal(goal):
    goal = int(goal)

    if goal < 1 or goal > 100:
        raise ValueError("Daily goal must be between 1 and 100.")

    set_setting("daily_goal", goal)
    return goal
