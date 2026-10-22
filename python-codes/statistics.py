from database import get_results


def get_statistics():
    results = get_results()

    if not results:
        return {
            "total_tests": 0,
            "best_wpm": 0,
            "average_wpm": 0,
            "average_accuracy": 0,
            "total_practice_minutes": 0,
            "total_characters": 0,
            "total_mistakes": 0
        }

    wpms = [row["wpm"] for row in results]
    accuracies = [row["accuracy"] for row in results]

    return {
        "total_tests": len(results),
        "best_wpm": max(wpms),
        "average_wpm": sum(wpms) / len(wpms),
        "average_accuracy": sum(accuracies) / len(accuracies),
        "total_practice_minutes": sum(
            row["duration"] for row in results
        ) / 60,
        "total_characters": sum(
            row["characters"] for row in results
        ),
        "total_mistakes": sum(
            row["mistakes"] for row in results
        )
    }


def get_recent_progress(limit=10):
    results = get_results()
    recent = list(reversed(results[:limit]))

    return {
        "labels": [
            row["created_at"][5:] for row in recent
        ],
        "wpms": [
            row["wpm"] for row in recent
        ]
    }
