from flask import Flask,jsonify,request
import chaos_injector_slave

app = Flask(__name__)
injection_slave = chaos_injector_slave.InjectionSlave()

@app.route('/inject_fault',methods=['GET'])
def get_instructions():
    return "just do it"

@app.route('/inject_fault',methods=['POST'])
def inject_fault():
    dns = request.json['dns']
    fault = request.json['fault']
    call_slave(dns,fault)
    return "yaay"

def call_slave(dns,fault):
    injection_slave.initiate_fault(dns, fault)

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0')
