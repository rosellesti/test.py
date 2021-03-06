#!flask/bin/python                                  
from flask import Flask, jsonify, request, abort, make_response #import object from the Flask model
from flask_httpauth import HTTPBasicAuth
import subprocess

test = Flask(__name__) #define app using Flask
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'rose':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)

@test.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@test.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

tasks = [
                {
                'id': 1,
                'title': u'Show Ovs-Dpctl show command',
                'description': u'the command: ovs-dpctl show-dps',
                'done': False
                },
                {
                'id': 2,
                'title': u'Add in dp in OpenvSwitch',
                'description': u'the command: ovs-dpctl add-dp',
                'done': False
                }
        ]

@test.route('/get-dps/test/v1.0/tasks', methods=['GET'])
def returnAll():
        return jsonify({'tasks': tasks})

@test.route('/get-dps/test/v1.0/tasks/showoutput', methods=['GET'])
def returnOne():
        p = subprocess.Popen(["sudo", "ovs-dpctl", "dump-dps"], stdout=subprocess.PIPE)
        output, err = p.communicate()
        return output

@test.route('/get-dps/test/v1.0/tasks/addinput', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)

    title = str(request.json['title'])
    concat = "sudo ovs-dpctl add-dp %s" % (title)
    subprocess.call(concat, shell = True)

    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }


    tasks.append(task)
    return jsonify({'task': task}), 201

@test.route('/get-dps/test/v1.0/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    title = str(request.json['title'])
    concat = "ovs-dpctl set-if dp port %s" % (title)
    subprocess.call(concat, shell = True)

    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@test.route('/get-dps/test/v1.0/tasks/deleteoutput/<int:task_id>', methods = ['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)

    title = str(request.json['title'])
    concat = "ovs-dpctl del-dp %s" % (title)
    subprocess.call(concat, shell = True)

    tasks.remove(task[0])
    return jsonify( { 'result': True } )

if __name__ == '__main__':
        test.run(debug=True) #run app on port 5000
