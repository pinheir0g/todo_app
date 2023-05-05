import requests
from flask import Blueprint, render_template, redirect, url_for, flash
from todo_app.serializers.serializers import Task
from todo_app.db import db
from todo_app.db.models import Todo
from todo_app.form import TaskForm

bp_render = Blueprint("frontend", __name__)


@bp_render.route("/")
def home():
    """Home page da aplicação"""
    api_response = requests.get("http://localhost:5000/tasks")
    tasks = api_response.json()["tasks"]
    return render_template("tasks.html", tasks=tasks)


@bp_render.route("/create", methods=["GET", "POST"])
def create_task():
    """View para criar uma task pelo browser"""
    form = TaskForm()
    if form.validate_on_submit():
        data = Task(
            title=form.title.data, description=form.description.data
        ).dict()
        response = requests.post("http://localhost:5000/tasks", json=data)
        if response.status_code == 200:
            flash("Tarefa criada com sucesso!", category="success")
            return redirect(url_for("frontend.home"))
    return render_template("task_form.html", form=form)


@bp_render.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_task(id):
    """View para editar uma task pelo browser"""
    task = requests.get(f"http://localhost:5000/tasks/{id}").json()
    form = TaskForm(data=task)
    if form.validate_on_submit():
        data = Task(
            id=id, title=form.title.data, description=form.description.data
        ).dict()
        response = requests.put(f"http://localhost:5000/tasks/{id}", json=data)
        if response.status_code == 200:
            flash("Tarefa editada com sucesso!", category="success")
            return redirect(url_for("frontend.home"))
    return render_template("edit_task.html", form=form, task=task)


@bp_render.route("/delete/<int:id>", methods=["GET", "DELETE"])
def delete_task(id):
    """View para deletar uma task pelo browser"""
    response = requests.delete(f"http://localhost:5000/tasks/{id}")
    if response.status_code == 200:
        flash("Tarefa deletada com sucesso!", category="success")
        return redirect(url_for("frontend.home"))
    return redirect(url_for("frontend.home"))


@bp_render.route("/toggle-task/<int:id>", methods=["GET", "POST"])
def toggle_task(id):
    task = db.session.query(Todo).filter_by(id=id).first()
    task.done = True
    db.session.commit()
    return redirect(url_for("frontend.home"))
