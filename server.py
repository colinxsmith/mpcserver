from flask import Flask, request 
from os import system
import subprocess

app = Flask(__name__)

@app.route('/dave', methods=[ 'GET'])
def index():
   if request.method == 'GET':
      value = request.args.get('value')
      back={}
      back['value'] = value
      if value!='':
         subprocess.getoutput('mpc play %s' % value)
      back['status'] = subprocess.getoutput('mpc')
      back['playlist'] = subprocess.getoutput('mpc playlist | cat -n').split('\n')
      return [back]
   else:
      return 'Use GET requests'

if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0', port=1310)
