from flask import Blueprint
from controllers.todoController import TodoController
todo = Blueprint('todo', __name__)


@todo.route('/')
def index():
    return TodoController.index()
