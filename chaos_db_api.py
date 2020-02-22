from flask import Flask,jsonify,request
from flask_pymongo import PyMongo
from pymongo import errors



app = Flask(__name__)
app.config['MONGODB_NAME'] = 'chaos'
app.config['MONGO_URI'] = 'mongodb://192.168.56.103:2717/chaos'

mongo   = PyMongo(app)





###########################################[SERVERS]####################################################
@app.route('/server',methods=['GET'])
def get_all_servers():
    servers = mongo.db.servers

    output = []
    for query in servers.find():
        output.append({'ip' : query['ip'] ,"dns" : query['dns'],  'groups' : query['groups']})

    return jsonify({'result' : output})


@app.route('/server/<dns>' ,methods=['GET'])
def get_one_server(dns):
    servers = mongo.db.servers
    query = servers.find_one({'dns' : dns})

    if query:
        output = {'ip' : query['ip'] ,"dns" : query['dns'],  'groups' : query['groups']}
    else :
        output = "server not found"
    return jsonify(output)

@app.route('/server', methods=['POST'])
def add_server():
    servers = mongo.db.servers
    request_dict = request.get_json()
    # Last fault is in format of DAY:MONTH:YEAR:HOUR:MINUTE:SECOND
    default_request_values = {'ip' : '127.127.127.127', 'active' : False, 'groups' : [], 'last_fault' : '15:12:00:00:00:00'}
    parse_request(request_dict,default_request_values)
    print(request_dict)

    try:
        dns = request_dict['dns']
        ip = request_dict['ip']
        groups = request_dict['groups']
        active = request_dict['active']
        last_fault = request_dict['last_fault']

        if servers.find({'dns': dns}).count() > 0:
           servers.find_one_and_update({'dns': dns}, {'$set': {'active': active},'$set' : {'ip' : ip} , '$set' : {'last_fault' : last_fault}})
           add_data_to_array(servers, {'identifier_key' : 'dns','identifier_value' : dns}, groups , 'groups')
           query = servers.find_one({'dns': dns})
        else:
            new_server_id = servers.insert({'dns': dns , 'groups' : groups , 'active' : active , 'ip' : ip , 'last_fault' : last_fault})
            query = servers.find_one({'_id' : new_server_id })
    except (errors.WriteError , TypeError) as e:
        raise e
        return jsonify({ 'result' : 'the object failed the validation schema'}) , 400

    output = {'dns' : query['dns'],  'groups' : query['groups'], 'active' :  query['active'],'ip' : query['ip'],'last_fault' : query['last_fault']}

    return jsonify({ 'result' : output})

###########################################[GROUPS]######################################################33

@app.route('/group', methods=['GET'])
def get_all_groups():
    groups = mongo.db.groups

    output = []
    for query in groups.find():
        output.append({'name' : query['name'],  'members' : query['members'], 'active' : query['active']})

    return jsonify({'result' : output})


@app.route('/group/<name>' ,methods=['GET'])
def get_one_group(name):
    groups = mongo.db.groups
    query = groups.find_one({'name' : name})
    if query:
        output = {'name' : query['name'],  'members' : query['members'], 'active' : query['active']}
    else :
        output = "group not found"
    return jsonify(output)


@app.route('/group', methods=['POST'])
def add_group():
    groups = mongo.db.groups
    request_dict = request.get_json()
    default_request_values = {'members' : [], 'active' : False}
    parse_request(request_dict,default_request_values)
    print(request_dict)

    try:
        name = request_dict['name']
        members = request_dict['members']
        active = request.json['active']

        if groups.find({'name': name}).count() > 0:
           groups.find_one_and_update({'name': name}, {'$set': {'active': active}})
           add_data_to_array(groups, {'identifier_key' : 'name','identifier_value' : name}, members , 'members')
           query = groups.find_one({'name': name})
        else:
            new_group_id = groups.insert({'name': name , 'members' : members , 'active' : active})
            query = groups.find_one({'_id' : new_group_id })
    except (errors.WriteError , TypeError) as e:
        raise e
        return jsonify({ 'result' : 'the object failed the validation schema'}) , 400

    output = {'name' : query['name'],  'members' : query['members'], 'active' :  query['active']}

    return jsonify({ 'result' : output})
#############################################[FAULTS]##############################################3

@app.route('/fault', methods=['GET'])
def get_all_faults():
    faults = mongo.db.faults

    output = []
    for query in faults.find():
        output.append({'name' : query['name'],  'content' : query['content'], 'active' : query['active'], 'targets' : query['targets']})

    return jsonify({'result' : output})


@app.route('/fault/<name>' ,methods=['GET'])
def get_one_fault(name):
    faults = mongo.db.faults
    query = faults.find_one({'name' : name})
    if query:
        output = {'name' : query['name'],  'content' : query['content'], 'active' : query['active'], 'targets' : query['targets']}
    else :
        output = "fault not found"
    return jsonify(output)


@app.route('/fault', methods=['POST'])
def add_fault():
    faults = mongo.db.faults
    request_dict = request.get_json()
    default_request_values = {'targets' : [], 'active' : False}
    parse_request(request_dict,default_request_values)
    print(request_dict)

    try:
        name = request_dict['name']
        targets = request_dict['targets']
        active = request_dict['active']
        content = request_dict['content']

        if faults.find({'name': name}).count() > 0:
           faults.find_one_and_update({'name': name}, {'$set': {'active': active},'$set': {'content': content}})
           add_data_to_array(faults, {'identifier_key' : 'name','identifier_value' : name}, targets , 'targets')
           query = faults.find_one({'name': name})
        else:
            new_fault_id = faults.insert({'name': name , 'targets' : targets , 'active' : active, 'content' : content})
            query = faults.find_one({'_id' : new_fault_id })
    except (errors.WriteError , TypeError) as e:
        raise e
        return jsonify({ 'result' : 'the object failed the validation schema'}) , 400

    output = {'name' : query['name'],  'targets' : query['targets'], 'active' :  query['active'], 'content' : query['content']}

    return jsonify({ 'result' : output})



def parse_request(request_dict,default_values_dict):
    default_keys = default_values_dict.keys()
    request_keys = request_dict.keys()
    for default_key in default_keys:
        if default_key not in request_keys :
            request_dict[default_key] = default_values_dict[default_key]
    return  request_dict

def add_data_to_array(collection,identifier_key_value,data,array_name):
    identifier_key = identifier_key_value['identifier_key']
    identifier_value = identifier_key_value['identifier_value']
    data = [] + data
    for data_cell in data :
        collection.update({identifier_key: identifier_value},{'$addToSet' : { array_name : data_cell}})


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0')
