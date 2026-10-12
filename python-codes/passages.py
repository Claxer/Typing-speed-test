import random

PASSAGES = {
    "Easy": [
        "Small steps can lead to big changes. Keep practicing and try to improve a little every day.",
        "Learning to type faster takes time. Stay calm, look at the screen, and use the correct fingers.",
        "A good habit starts with a simple action. Practice often and celebrate your progress.",
        "Python is a useful programming language. It can help beginners build tools, games, and applications.",
        "Focus on accuracy before speed. As your typing becomes more natural, your words per minute can improve."
    ],
    "Medium": [
        "Good programmers solve problems by breaking them into smaller steps. They test each part, read error messages, and improve their code.",
        "Technology changes quickly, but curiosity and consistent practice remain valuable skills for every student.",
        "A reliable application should be easy to use, validate information, and handle unexpected situations without crashing.",
        "Typing practice develops coordination between your eyes, hands, and mind. Accuracy is an important part of useful speed.",
        "Every project teaches something new. Keep your files organized, write clear functions, and save your progress regularly."
    ],
    "Hard": [
        "Debugging is not simply fixing mistakes; it is a process of observing behavior, forming a hypothesis, testing it, and learning from the result.",
        "A well-designed program balances usability, performance, reliability, and maintainability. Small improvements can make a noticeable difference.",
        "Before releasing software, developers should verify edge cases, validate user input, review database operations, and document important decisions.",
        "Consistency matters more than a single impressive result. Measure your progress over time, identify weak areas, and practice deliberately.",
        "In Python, readable code is often better than clever code. Meaningful names, focused functions, and helpful comments make a project easier to maintain."
    ]
}

def get_passage(difficulty="Medium"):
    """Return a random passage for the selected difficulty."""
    passages = PASSAGES.get(difficulty, PASSAGES["Medium"])
    return random.choice(passages)
