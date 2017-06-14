#!flask/bin/python                                  
from flask import Flask, jsonify, request, abort, make_response #import object from the Flask model

test = Flask(__name__) #define app using Flask

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

    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }

    tasks.append(task)
    return jsonify({'task': task}), 201

@test.route('/get-dps/test/v1.0/tasks/<int:task_id>', methods=['PUT'])
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
   
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@test.route('/get-dps/test/v1.0/tasks/deleteoutput/<int:task_id>', methods = ['DELETE'])
def delete_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)

    tasks.remove(task[0])
    return jsonify( { 'result': True } )

if __name__ == '__main__':
        test.run(debug=True) #run app on port 5000

