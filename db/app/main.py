from flask import Flask,jsonify,request
from flask_pymongo import PyMongo
from pymongo import errors
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

mongodb_ip = os.environ.get("DB_IP", "chaos.mongodb.openshift")
mongodb_port = os.environ.get("DB_PORT", "8080")
db_name = os.environ.get("DB_NAME", "chaos")
server_port = int(os.environ.get("SERVER_PORT", 5001))
mongodb_ip = "52.255.160.180"

mongodb_uri = "mongodb://{}:{}/{}".format(mongodb_ip,mongodb_port,db_name)
app.config['MONGODB_NAME'] = db_name
app.config['MONGO_URI'] = mongodb_uri

mongo   = PyMongo(app)

@app.route('/servers',methods=['GET'])
@app.route('/server',methods=['GET'])
def get_all_servers():
    collection = "servers"
    expected_returned_keys = ["dns","active","groups"]
    output = get_all_objects(collection, expected_returned_keys)
    return output

@app.route('/servers/<dns>' ,methods=['GET'])
@app.route('/server/<dns>' ,methods=['GET'])
def get_one_server(dns):
    collection = "servers"
    identifier_key = "dns"
    identifier_value = dns
    expected_returned_keys = ["dns", "active","groups"]
    output = get_one_object(collection,identifier_key,identifier_value,expected_returned_keys)
    return output

@app.route('/servers', methods=['POST'])
@app.route('/server', methods=['POST'])
def add_server():
    collection = "servers"
    json_object = request.get_json()
    expected_returned_keys =  ["dns", "active","groups"]
    identifier_key = "dns"
    try :
        identifier_value = json_object["dns"]
    except KeyError :
        return "dns is a required parameter",400
    default_request_values = {'active' : False, 'groups' : [], 'last_fault' : '15:12:00:00:00:00'}
    add_object_to_db(collection, json_object, expected_returned_keys, identifier_key, identifier_value,default_request_values)


@app.route('/groups', methods=['GET'])
@app.route('/group', methods=['GET'])
def get_all_groups():
    collection = "groups"
    expected_returned_keys = ["name", "active"]
    output = get_all_objects(collection, expected_returned_keys)
    return output


@app.route('/groups/<name>' ,methods=['GET'])
@app.route('/group/<name>' ,methods=['GET'])
def get_one_group(name):
    collection = "groups"
    identifier_key = "name"
    identifier_value = name
    expected_returned_keys = ["name", "active"]
    output = get_one_object(collection, identifier_key, identifier_value, expected_returned_keys)
    return output


@app.route('/groups', methods=['POST'])
@app.route('/group', methods=['POST'])
def add_group():
    collection = "groups"
    json_object = request.get_json()
    expected_returned_keys = ["name", "active"]
    identifier_key = "name"
    try:
        identifier_value = json_object["name"]
    except KeyError:
        return "name is a required parameter", 400
    default_request_values = {'members' : [], 'active' : False}
    output = add_object_to_db(collection, json_object, expected_returned_keys, identifier_key, identifier_value,default_request_values)
    return output


@app.route('/methods', methods=['GET'])
@app.route('/method', methods=['GET'])
def get_all_methods():
    collection = "methods"
    expected_returned_keys = ["name", "active","targets","path"]
    output = get_all_objects(collection, expected_returned_keys)
    return output

@app.route('/methods/<name>' ,methods=['GET'])
@app.route('/method/<name>' ,methods=['GET'])
def get_one_method(name):
    collection = "methods"
    identifier_key = "name"
    identifier_value = name
    expected_returned_keys = ["name", "active","targets","path"]
    output = get_one_object(collection, identifier_key, identifier_value, expected_returned_keys)
    return output

@app.route('/methods', methods=['POST'])
@app.route('/method', methods=['POST'])
def add_method():
    collection = "methods"
    json_object = request.get_json()
    expected_returned_keys = ["name", "active"]
    identifier_key = "name"
    try:
        identifier_value = json_object["name"]
    except KeyError:
        return "name is a required parameter", 400
    default_request_values = {'targets' : [], 'active' : False}
    output = add_object_to_db(collection, json_object, expected_returned_keys, identifier_key, identifier_value,default_request_values)
    return output

@app.route('/probes', methods=['GET'])
@app.route('/probe', methods=['GET'])
def get_all_probes():
    collection = "probes"
    expected_returned_keys = ["name", "active","targets","path"]
    output = get_all_objects(collection, expected_returned_keys)
    return output

@app.route('/probes/<name>' ,methods=['GET'])
@app.route('/probe/<name>' ,methods=['GET'])
def get_one_probe(name):
    collection = "probes"
    identifier_key = "name"
    identifier_value = name
    expected_returned_keys = ["name", "active","targets","path"]
    output = get_one_object(collection, identifier_key, identifier_value, expected_returned_keys)
    return output


@app.route('/probes', methods=['POST'])
@app.route('/probe', methods=['POST'])
def add_probe():
    collection = "probes"
    json_object = request.get_json()
    expected_returned_keys = ["name", "active"]
    identifier_key = "name"
    try:
        identifier_value = json_object["name"]
    except KeyError:
        return "name is a required parameter", 400
    default_request_values = {'targets' : [], 'active' : False}
    output = add_object_to_db(collection, json_object, expected_returned_keys, identifier_key, identifier_value,default_request_values)
    return output


@app.route('/rollbacks', methods=['GET'])
@app.route('/rollback', methods=['GET'])
def get_all_rollbacks():
    collection = "rollbacks"
    expected_returned_keys = ["name", "active","targets","path"]
    output = get_all_objects(collection, expected_returned_keys)
    return output

@app.route('/rollbacks/<name>' ,methods=['GET'])
@app.route('/rollback/<name>' ,methods=['GET'])
def get_one_rollback(name):
    collection = "rollbacks"
    identifier_key = "name"
    identifier_value = name
    expected_returned_keys = ["name", "active","targets","path"]
    output = get_one_object(collection, identifier_key, identifier_value, expected_returned_keys)
    return output


@app.route('/rollbacks', methods=['POST'])
@app.route('/rollback', methods=['POST'])
def add_rollback():
    collection = "rollbacks"
    json_object = request.get_json()
    expected_returned_keys = ["name", "active"]
    identifier_key = "name"
    try:
        identifier_value = json_object["name"]
    except KeyError:
        return "name is a required parameter", 400
    default_request_values = {'targets' : [], 'active' : False}
    output = add_object_to_db(collection, json_object, expected_returned_keys, identifier_key, identifier_value,default_request_values)
    return output


@app.route('/faults', methods=['GET'])
@app.route('/fault', methods=['GET'])
def get_all_faults():
    collection = "faults"
    expected_returned_keys = ["name", "active","targets","probes","methods","rollbacks"]
    output = get_all_objects(collection, expected_returned_keys)
    return output

@app.route('/faults/<name>' ,methods=['GET'])
@app.route('/fault/<name>' ,methods=['GET'])
def get_one_fault(name):
    collection = "faults"
    identifier_key = "name"
    identifier_value = name
    expected_returned_keys = ["name", "active","targets","probes","methods","rollbacks"]
    output = get_one_object(collection, identifier_key, identifier_value, expected_returned_keys)
    return output


@app.route('/faults', methods=['POST'])
@app.route('/fault', methods=['POST'])
def add_fault():
    collection = "faults"
    json_object = request.get_json()
    expected_returned_keys = ["name", "active","targets","probes","methods","rollbacks"]
    identifier_key = "name"
    try:
        identifier_value = json_object["name"]
    except KeyError:
        return "name is a required parameter", 400
    default_request_values = {'targets' : [], 'active' : False, 'probes' :[] , 'methods':[] , 'rollbacks':[] }

    output = add_object_to_db(collection, json_object, expected_returned_keys, identifier_key, identifier_value,default_request_values)
    return output



@app.route('/logs', methods=['POST'])
@app.route('/log', methods=['POST'])
def add_log():
    collection = "logs"
    json_object = request.get_json()
    expected_returned_keys = ["name", 'logs' , "date", "successful" ]
    identifier_key = "name"
    try:
        identifier_value = json_object["name"]
    except KeyError:
        return "name is a required parameter", 400
    default_request_values = {'logs' : [], 'date': "001215000000 ", 'successful' : False }

    output = add_object_to_db(collection, json_object, expected_returned_keys, identifier_key, identifier_value,default_request_values)
    return output

@app.route('/logs', methods=['GET'])
@app.route('/log', methods=['GET'])
def get_all_logs():
    collection = "logs"
    expected_returned_keys = ["name", 'logs' , "date", "successful" ]
    output = get_all_objects(collection, expected_returned_keys)
    return output

@app.route('/logs/<name>' ,methods=['GET'])
@app.route('/log/<name>' ,methods=['GET'])
def get_one_log(name):
    collection = "logs"
    identifier_key = "name"
    identifier_value = name
    expected_returned_keys = ["name", 'logs' , "date", "successful" ]
    output = get_one_object(collection, identifier_key, identifier_value, expected_returned_keys)
    return output




@app.route('/experiments', methods=['GET'])
@app.route('/experiment', methods=['GET'])
def get_all_experiments():
    collection = "experiments"
    expected_returned_keys = ["id", 'status' , "start_time", "end_time" ,"successful" ]
    output = get_all_objects(collection, expected_returned_keys)
    return output


@app.route('/experiments', methods=['POST'])
@app.route('/experiment', methods=['POST'])
def add_experiment():
    collection = "experiments"
    json_object = request.get_json()
    expected_returned_keys = ["id", 'status' , "start_time", "end_time" ,"successful" ]
    identifier_key = "id"
    try:
        identifier_value = json_object["id"]
    except KeyError:
        return "id is a required parameter", 400
    default_request_values = {'successful' : False }

    output = add_object_to_db(collection, json_object, expected_returned_keys, identifier_key, identifier_value,default_request_values)
    return output


@app.route('/experiments/<id>' ,methods=['GET'])
@app.route('/experiments/<id>' ,methods=['GET'])
def get_one_experiment(id):
    collection = "experiments"
    identifier_key = "id"
    identifier_value = id
    expected_returned_keys = ["id", 'status' , "start_time", "end_time" ,"successful" ]
    output = get_one_object(collection, identifier_key, identifier_value, expected_returned_keys)
    return output


@app.route('/experiments/<id>', methods=['PUT'])
@app.route('/experiment/<id>', methods=['PUT'])
def update_experiment(id):
    collection = "experiments"
    json_object = request.get_json()
    print(request.get_json())
    identifier_key = "id"
    try:
        identifier_value = id
    except KeyError:
        return "id is a required parameter", 400
    output = update_object_in_db(collection, json_object, identifier_key, identifier_value)
    return output

def get_one_object(collection,identifier_key,identifier_value,expected_returned_keys):
    # Easyiest way to use a string as a property of an object
    objects = eval("mongo.db.{}".format(collection))
    query = objects.find_one({identifier_key : identifier_value})
    if query:
        output = {}
        for key in expected_returned_keys :
            output[key] = query[key]
    else :
        output = "object not found"
    return jsonify(output)


def get_all_objects(collection,expected_returned_keys):
    # Easyiest way to use a string as a property of an object
    objects = eval("mongo.db.{}".format(collection))
    output = []
    for query in objects.find():
        found_object = {}
        for key in expected_returned_keys :
            found_object[key] = query[key]
        output.append(found_object)

    return jsonify({'result' : output})


def update_object_in_db(collection, json_object, identifier_key, identifier_value):
    objects = eval("mongo.db.{}".format(collection))
    output = objects.update({identifier_key: identifier_value}, {'$set' : json_object} )
    return  output


def add_object_to_db(collection,json_object,expected_returned_keys,identifier_key,identifier_value,default_request_values):

    # Easyiest way to use a string as a property of an object
    objects = eval("mongo.db.{}".format(collection))

    # Fill out default values if not in sent object
    json_object = parse_json_object(json_object, default_request_values)
    try:
        if objects.count_documents({identifier_key: identifier_value}) > 0:
           return {"result" : "object with the same identifier already exists"}, 400
        else:
            new_object_id = objects.insert(json_object, check_keys=False)
            query = objects.find_one({'_id': new_object_id})
    except (errors.WriteError, TypeError) as E:
        print(E)
        return jsonify({'result': 'the object failed the validation schema'}), 400
    output = {}

    for expected_key in expected_returned_keys:
      output[expected_key] = query[expected_key]

    return jsonify({'result': output})


def parse_json_object(json_object,default_values_dict):
    default_keys = default_values_dict.keys()
    object_keys = json_object.keys()
    for default_key in default_keys:
        if default_key not in object_keys :
            json_object[default_key] = default_values_dict[default_key]
    return  json_object

if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=server_port)