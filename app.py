from flask import Flask, logging, request
from flask_restful import Resource, Api, abort

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


todos = {}


class TodoDetail(Resource):
    def get(self, todo_id):
        if todo_id in todos:
            return {todo_id: todos[todo_id]}, 200
        else:
            abort(404, message="Todo {} doesn't exist".format(todo_id))

    def delete(self, todo_id):
        if todo_id in todos:
            del todos[todo_id]
            return '', 204
        else:
            abort(404, message="Todo {} doesn't exist".format(todo_id))

    def put(self, todo_id):
        if todo_id in todos:
            todos[todo_id] = request.form['data']
            return {todo_id: todos[todo_id]}, 201
        else:
            abort(404, message="Todo {} doesn't exist".format(todo_id))


class TodoList(Resource):
    def get(self):
        return todos

    def post(self):
        claves = todos.keys()
        todo_id = max(claves) + 1 if len(claves) > 0 else 1
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}, 201


api.add_resource(HelloWorld, '/')
api.add_resource(TodoDetail, '/todos/<int:todo_id>')
api.add_resource(TodoList, '/todos')

if __name__ == '__main__':
    app.run(debug=True)
