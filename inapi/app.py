# coding=utf-8

from flask import Flask,request
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/put', methods=['PUT'])
def handleput():
    c=request.data
    print len(c)
    print request.headers
    for i in request.form:
        print i,": ",request.form[i]
    return "hahaha"

if __name__ == "__main__":
    app.run(host="0.0.0.0",threaded=True)
