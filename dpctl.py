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

if __name__ == '__main__':
        test.run(debug=True) #run app on port 5000

