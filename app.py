from flask import Flask, render_template, request, redirect
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
app.secret_key = "secret"

# In-memory chore log per kid
chore_log = {
    "manha": [],
    "furqaan": []
}

# Default chores
mandatory_chores = {
    "Brush Teeth": 5,
    "Make Bed": 5,
    "Clean Room": 5,
    "Do Homework": 5,
}

bonus_chores = {
    "Wash Dishes": 10,
    "Help Cook": 15,
    "Water Plants": 10,
    "Fold Laundry": 20,
    "Empty Dish washer": 10
}

# Combine all chores into one dictionary
all_chores = {**mandatory_chores, **bonus_chores}

@app.route("/", methods=["GET", "POST"])
def index():
    selected_kid = request.form.get("kid", "manha")  # Default to Manha

    # Adding a new chore
    if request.method == "POST" and "new_chore" in request.form:
        new_chore = request.form["new_chore"]
        new_points = int(request.form["points"])
        all_chores[new_chore] = new_points
        return redirect("/")

    # Submitting completed chores
    elif request.method == "POST" and "chores" in request.form:
        selected_chores = request.form.getlist("chores")
        date = request.form.get("date", datetime.now().strftime("%Y-%m-%d"))

        for chore in selected_chores:
            chore_log[selected_kid].append({
                "chore": chore,
                "points": all_chores.get(chore, 0),
                "date": date
            })
        return redirect("/")

    # Weekly summary for selected kid
    logs = chore_log[selected_kid]
    weekly_summary_data = defaultdict(int)
    for c in logs:
        date_obj = datetime.strptime(c["date"], "%Y-%m-%d")
        week = f"Week {date_obj.isocalendar().week}"
        weekly_summary_data[week] += c["points"]

    total_points = sum(c["points"] for c in logs)
    badge = "🥇 Awesome! You've earned a badge for reaching 100 points!" if total_points >= 100 else None

    return render_template("index.html",
                           selected_kid=selected_kid,
                           all_chores=all_chores,
                           chore_log=chore_log,
                           total_points=total_points,
                           badge=badge,
                           weekly_summary_labels=list(weekly_summary_data.keys()),
                           weekly_summary_data=list(weekly_summary_data.values()))
    
if __name__ == "__main__":
    app.run(debug=True)
