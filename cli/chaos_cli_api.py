from flask import Flask,jsonify,request

app = Flask(__name__)


@app.route('/random',methods=['GET'])
def get_method():
    return "random hello"

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0')
