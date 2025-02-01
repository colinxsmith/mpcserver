from flask import Flask, request 
from flask_cors import CORS


import subprocess

app = Flask(__name__)
CORS(app)
@app.after_request
def add_headers(response):
    response.headers.add('Content-Type', 'application/json')
    response.headers.add('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'content-type, traceid, withcredentials')
    response.status=200
    return response

@app.route("/")
def helloWorld():
      back={}
      back['status'] = subprocess.getoutput('mpc')
      back['playlist'] = subprocess.getoutput('mpc playlist | cat -n').split('\n')
      return [back]
@app.route('/dave', methods=[ 'GET'])
def index():
   if request.method == 'GET':
      value = request.args.get('value')
      seek = request.args.get('seek')
      back={}
      back['value'] = value
      if value!='':
         subprocess.getoutput('mpc play %s' % value)
      try:
         if seek.find('%')>-1:
            subprocess.getoutput('mpc seek %s'%seek)
         else:
            subprocess.getoutput('mpc seek %s'%seek+'%')
      except:
         seek='0%'
         subprocess.getoutput('mpc seek 0%')
      back['status'] = subprocess.getoutput('mpc')
      back['playlist'] = subprocess.getoutput('mpc playlist | cat -n').split('\n')
      back['seek']=seek
      return [back]
   else:
      return 'Use GET requests'

if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0', port=1310)
