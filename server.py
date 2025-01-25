from flask import Flask, request 
from os import system

app = Flask(__name__)

@app.route('/dave', methods=[ 'GET'])
def index():
   if request.method == 'GET':
      value = request.args.get('value')
      system('mpc play %s'%value)
      return 'OK'
   else:
      return 'Use GET requests'

if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0', port=1310)
