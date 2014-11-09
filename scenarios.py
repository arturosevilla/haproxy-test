#!/usr/bin/env python
import json
import urllib2
import sys

# the initial master address
instances = ['http://localhost:5000', 'http://localhost:5001']

def make_request(address, master_flag):
    req = urllib2.Request(address + '/change/status')
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps({'master': master_flag}))
    if response.getcode() == 200:
        print('Successfully %s master at %s instance' % (
            'activated' if master_flag else 'deactivated', address))
    else:
        print('There was an error while trying to change master status')

def determine_master():
    for configured_address in instances:
        try:
            response = urllib2.urlopen(configured_address + '/check/master')
        except urllib2.HTTPError, httperror:
            if httperror.code != 404:
                # other kind of error
                raise
            continue
        if response.getcode() == 200:
            return configured_address
    raise Exception('Master not found')

def change_master():
    if len(instances) == 1:
        raise Exception('To change masters, the cluster needs to have at least two instances')
    try:
        current_master = determine_master()
        master_index = instances.index(current_master)
    except ValueError:
        raise Exception('Misconfigured? %s was not found among instances' % master)
    
    # just do a round robin for the next instance
    master_index = (master_index + 1) % len(instances)
    new_master = instances[master_index]
    # make the old master a slave
    make_request(current_master, False)
    # make the selected instance the master
    make_request(new_master, True)

def crash_master():
    # this function just makes master unavailable
    make_request(determine_master(), False)


if __name__ == '__main__':
    should_change_master = len(sys.argv) != 2 or sys.argv[1] == 'change_master'
    if should_change_master:
        change_master()
    else:
        crash_master()

