import random

PASSAGES = {
    "Easy": [
        "The sun is shining and the weather is nice today. I enjoy learning new things and practicing my typing skills.",
        "Python is a programming language that is easy to read and useful for building many different applications.",
        "A good student practices every day and tries to improve one step at a time. Small efforts can lead to great results.",
        "Technology helps people communicate, learn, and solve problems. Computers are useful tools in our daily lives.",
        "Reading books and writing code can help improve your knowledge. Practice makes difficult tasks easier over time."
    ],
    "Medium": [
        "Programming requires patience, logical thinking, and consistent practice. Developers often solve complex problems by dividing them into smaller tasks.",
        "Information technology connects people through computer networks, software applications, databases, and digital communication systems.",
        "Learning a new programming language takes time. Understanding the fundamentals is more important than memorizing every command.",
        "A computer system combines hardware and software to process information, perform calculations, and complete useful tasks.",
        "Successful projects begin with clear goals, organized planning, careful testing, and a willingness to learn from mistakes."
    ],
    "Hard": [
        "Software development involves analyzing requirements, designing solutions, implementing algorithms, debugging errors, and maintaining reliable applications.",
        "Cybersecurity professionals protect computer systems by identifying vulnerabilities, monitoring suspicious activities, and applying appropriate security controls.",
        "Efficient algorithms reduce unnecessary operations, improve processing time, and help applications handle increasingly complicated workloads.",
        "Database management requires structured information, reliable transactions, appropriate permissions, and consistent backup procedures.",
        "Artificial intelligence can analyze large datasets, recognize patterns, and support decision-making when implemented responsibly."
    ]
}


def get_passage(difficulty):
    passages = PASSAGES.get(difficulty, PASSAGES["Easy"])
    return random.choice(passages)
