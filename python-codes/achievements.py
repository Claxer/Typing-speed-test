from database import get_results, get_today_count, get_setting


def get_achievements():
    results = get_results()
    total = len(results)

    best_wpm = max(
        (row["wpm"] for row in results),
        default=0
    )

    total_characters = sum(
        row["characters"] for row in results
    )

    goal = int(get_setting("daily_goal", "3"))
    today_count = get_today_count()

    achievements = [
        {
            "name": "First Steps",
            "description": "Complete your first typing test.",
            "unlocked": total >= 1
        },
        {
            "name": "Getting Started",
            "description": "Complete 10 typing tests.",
            "unlocked": total >= 10
        },
        {
            "name": "Practice Pro",
            "description": "Complete 50 typing tests.",
            "unlocked": total >= 50
        },
        {
            "name": "Speed Demon",
            "description": "Reach 60 WPM.",
            "unlocked": best_wpm >= 60
        },
        {
            "name": "Speed Master",
            "description": "Reach 100 WPM.",
            "unlocked": best_wpm >= 100
        },
        {
            "name": "Keyboard Explorer",
            "description": "Type 10,000 characters.",
            "unlocked": total_characters >= 10000
        },
        {
            "name": "Daily Dedication",
            "description": "Complete today's practice goal.",
            "unlocked": today_count >= goal
        }
    ]

    return achievements
