from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import NotFound, BadRequest

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'description': self.description, 'status': self.status}

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        raise NotFound('Task not found')
    return jsonify(task.to_dict())

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    if 'title' not in data or 'description' not in data or 'status' not in data:
        raise BadRequest('Missing required fields')
    task = Task(title=data['title'], description=data['description'], status=data['status'])
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        raise NotFound('Task not found')
    data = request.json
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        task.status = data['status']
    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        raise NotFound('Task not found')
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'})

@app.errorhandler(NotFound)
def handle_not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(BadRequest)
def handle_bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)