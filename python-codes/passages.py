
import random

PASSAGES = {
    "Easy": [
        "Python is a popular programming language. It is simple to learn and useful for many projects.",
        "Practice every day to improve your typing speed and accuracy. Small steps can lead to great results.",
        "Learning new skills takes time. Stay patient, keep practicing, and celebrate your progress."
    ],
    "Medium": [
        "Programming helps us solve problems by breaking complicated tasks into smaller and more manageable steps.",
        "A good developer writes readable code, tests different situations, and learns from mistakes along the way.",
        "Technology continues to change how people communicate, study, work, and share information with others."
    ],
    "Hard": [
        "Software development requires logical thinking, consistent practice, careful testing, and attention to detail.",
        "Efficient programming combines readable code, appropriate data structures, reliable algorithms, and maintainable design.",
        "Debugging is an essential skill because unexpected errors can reveal weaknesses in assumptions or implementation."
    ]
}


def get_random_passage(difficulty="Easy"):
    passages = PASSAGES.get(difficulty, PASSAGES["Easy"])
    return random.choice(passages)


def get_custom_passage(text):
    return text.strip()


def get_passage_for_mode(difficulty="Easy", custom_text=""):
    if custom_text.strip():
        return custom_text.strip()

    return get_random_passage(difficulty)
