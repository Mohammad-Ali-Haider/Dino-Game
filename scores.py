import hashlib
import os

SECRET_KEY = os.getenv("SECRET_KEY")

def save_score(score, filename="high_score.txt"):
    score = int(score)

    score_data = f"{score}{SECRET_KEY}"
    score_hash = hashlib.sha256(score_data.encode()).hexdigest()

    with open(filename, "w") as file:
        file.write(f"{score}\n{score_hash}")

def load_score(filename="high_score.txt"):
    if not os.path.exists(filename):
        return 0

    with open(filename, "r") as file:
        lines = file.readlines()

        if len(lines) != 2:
            return 0

        saved_score = lines[0].strip()
        saved_hash = lines[1].strip()

        score_data = f"{saved_score}{SECRET_KEY}"
        expected_hash = hashlib.sha256(score_data.encode()).hexdigest()

        if saved_hash == expected_hash:
            return int(saved_score)
        else:
            return 0