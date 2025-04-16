from flask import Flask, render_template, request, redirect
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = "secret"

DATA_FILE = "data.json"

# Load data from JSON file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "chore_log": {"manha": [], "furqaan": []},
        "all_kids": ["manha", "furqaan"],
        "all_chores": {
            "Brush Teeth": 5,
            "Make Bed": 5,
            "Clean Room": 5,
            "Do Homework": 5,
            "Wash Dishes": 10,
            "Help Cook": 15,
            "Water Plants": 10,
            "Fold Laundry": 20,
            "Empty Dish washer": 10
        }
    }

# Save data to JSON file
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({
            "chore_log": chore_log,
            "all_kids": all_kids,
            "all_chores": all_chores
        }, f, indent=4)

# Load on startup
data = load_data()
chore_log = data["chore_log"]
all_kids = data["all_kids"]
all_chores = data["all_chores"]

@app.route("/", methods=["GET", "POST"])
def index():
    global all_kids, all_chores, chore_log

    selected_kid = request.form.get("kid") or "manha"

    if request.method == "POST" and "new_kid" in request.form:
        new_kid = request.form["new_kid"].strip().lower()
        if new_kid and new_kid not in all_kids:
            all_kids.append(new_kid)
            chore_log[new_kid] = []
            save_data()
        return redirect("/")

    elif request.method == "POST" and "new_chore" in request.form:
        new_chore = request.form["new_chore"]
        new_points = int(request.form["points"])
        all_chores[new_chore] = new_points
        save_data()
        return redirect("/")

    elif request.method == "POST" and "chores" in request.form:
        selected_chores = request.form.getlist("chores")
        date = request.form.get("date", datetime.now().strftime("%Y-%m-%d"))

        if selected_kid not in chore_log:
            chore_log[selected_kid] = []

        for chore in selected_chores:
            chore_log[selected_kid].append({
                "chore": chore,
                "points": all_chores.get(chore, 0),
                "date": date
            })
        save_data()
        return redirect("/")

    total_points_by_kid = {}
    badge_by_kid = {}
    for kid in all_kids:
        logs = chore_log.get(kid, [])
        total = sum(c["points"] for c in logs)
        total_points_by_kid[kid] = total
        badge_by_kid[kid] = "🥇 Awesome! You've earned a badge for reaching 100 points!" if total >= 100 else None

    return render_template("index.html",
                           selected_kid=selected_kid,
                           all_kids=all_kids,
                           all_chores=all_chores,
                           chore_log=chore_log,
                           total_points=total_points_by_kid,
                           badge=badge_by_kid)

if __name__ == "__main__":
    app.run(debug=True)
