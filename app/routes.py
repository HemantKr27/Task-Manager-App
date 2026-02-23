from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import Task
from app import db

main = Blueprint("main",__name__)

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/test")
def test():
    return "test route working"

@main.route("/dashboard")
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", tasks=tasks)

@main.route("/add_task", methods = ["POST"])
@login_required
def add_task():
    title = request.form.get("title")  

    if not title or title.strip() == "":
        flash("Task title cannot be empty.", "danger")
        return redirect(url_for("main.dashboard"))

    new_task = Task( title = title,
                    user_id = current_user.id
                    )

    db.session.add(new_task)
    db.session.commit()

    flash("Task added successfully!", "success")
    return redirect(url_for("main.dashboard"))

@main.route("/complete/<int:task_id>", methods = ["POST"])
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)

    #Security check
    if task.user_id != current_user.id:
        flash("Unauthorized action", "danger")
        return redirect(url_for("main.dashboard"))
    task.completed = not task.completed
    db.session.commit()

    #flash("Task marked as completed!", "success")
    #return redirect(url_for("main.dashboard"))
    return jsonify({
        "success": True,
        "completed": task.completed
    })


@main.route("/delete/<int:task_id>", methods = ["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    #check for correct task
    if task.user_id != current_user.id:
        flash("Unauthorized action", "danger")
        return redirect(url_for("main.dashboard"))
    
    db.session.delete(task)
    db.session.commit()

    flash("Task deleted successfully!", "success")
    return redirect(url_for("main.dashboard"))