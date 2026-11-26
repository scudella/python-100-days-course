import os
from flask import Flask, render_template, redirect, url_for
from models import db, Todo
from forms import TodoForm, ActionForm

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    form = TodoForm()
    action_form = ActionForm()

    if form.validate_on_submit():
        new_todo = Todo(title=form.title.data.strip())
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("index"))

    todos = Todo.query.order_by(Todo.completed.asc(), Todo.id.desc()).all()
    return render_template(
        "index.html",
        form=form,
        action_form=action_form,
        todos=todos,
    )


@app.route("/toggle/<int:todo_id>", methods=["POST"])
def toggle(todo_id):
    form = ActionForm()
    if form.validate_on_submit():
        todo = db.get_or_404(Todo, todo_id)
        todo.completed = not todo.completed
        db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete(todo_id):
    form = ActionForm()
    if form.validate_on_submit():
        todo = db.get_or_404(Todo, todo_id)
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
