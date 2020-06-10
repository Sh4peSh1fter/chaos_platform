from flask import Flask,request
import chaos_injector_slave
import os

injector_url = os.environ.get("INJECTOR_API", "http://chaos.injector.openshift:5002")
db_url = os.environ.get("DB_API", "http://chaos.db.openshift:5001")
server_port = int(os.environ.get("SERVER_PORT", 5001))


app = Flask(__name__)
injection_slave = chaos_injector_slave.InjectionSlave(db_url)

@app.route('/inject_fault',methods=['GET'])
def get_instructions():
    return "send dns and fault name in json object"

@app.route('/inject_fault',methods=['POST'])
def inject_fault():
    dns = request.json['dns']
    fault = request.json['fault']
    output = call_slave(dns,fault)
    return output

def call_slave(dns,fault):
    output = injection_slave.initiate_fault(dns, fault)
    return  output
if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port= server_port)
