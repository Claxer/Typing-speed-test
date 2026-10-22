import random

PASSAGES = {
    "Easy": [
        "Practice makes progress. Keep typing and try to improve every day.",
        "Python is a useful programming language for beginners.",
        "Small steps can lead to big improvements over time.",
        "Learning to type faster takes patience and regular practice.",
        "Stay focused and try to make fewer mistakes each time."
    ],
    "Medium": [
        "Programming requires patience, logical thinking, and consistent practice.",
        "A good developer writes readable code and solves problems carefully.",
        "Typing accurately is more important than typing quickly at first.",
        "Building projects helps students understand programming concepts.",
        "Technology continues to change the way people learn and work."
    ],
    "Hard": [
        "Software development combines problem-solving, creativity, and technical knowledge.",
        "Efficient programmers analyze problems before implementing a practical solution.",
        "Consistency, accuracy, and concentration contribute to better typing performance.",
        "Applications should be reliable, maintainable, and easy to understand.",
        "Developing strong technical skills requires curiosity and continuous improvement."
    ]
}


def get_passage(difficulty="Easy"):
    """Return a random passage for the selected difficulty."""
    passages = PASSAGES.get(difficulty, PASSAGES["Easy"])
    return random.choice(passages)


def get_all_passages():
    """Return every passage organized by difficulty."""
    return PASSAGES
