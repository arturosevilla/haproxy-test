#!/usr/bin/env python

from flask import Flask, jsonify, request
import sys

app = Flask(__name__)

# determines if the current instance is the master of the cluster
master = False
# this is the information that will be returned (will be used to differentiate
# between the instances)
node_id = 0

# this will simulate checking for the master instance in the cluster
@app.route('/check/master', methods=['GET'])
def check_master():
    if master:
        return jsonify({'master': True})
    # also fail with a 404 (Neo4j HA does this)
    return jsonify({'master': False}), 404

# this will simulate checking for slaves in the cluster
@app.route('/check/slave', methods=['GET'])
def check_slave():
    if master:
        # also fail with a 404 (Neo4j HA does this)
        return jsonify({'slave': False}), 404
    return jsonify({'slave': True})

# this will simulate checking just for availability in the cluster
@app.route('/check/availability', methods=['GET'])
def check_availability():
    # always succeed
    return jsonify({'available': True})

# this will toggle the status between master and slave
@app.route('/change/status', methods=['POST'])
def change_cluster_status():
    global master
    status = request.json
    if 'master' not in status:
        abort(400)
    master = bool(status['master'])
    return jsonify({'master': master})


@app.route('/query', methods=['GET'])
def query():
    return jsonify({'node_id': node_id})

if __name__ == '__main__':
    # should be run as ./web.py port_number master|slave node_id
    if len(sys.argv) != 4:
        sys.exit('Must be run as ./web.py port_number master|slave node_id')

    port_number = int(sys.argv[1])
    master = sys.argv[2] == 'master'
    node_id = int(sys.argv[3])
    print('Running %s instance on port %d with instance id: %d' % (
        'master' if master else 'slave', port_number, node_id))
    app.run(port=port_number, debug=True)

