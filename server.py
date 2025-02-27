from flask import Flask, request 
from flask_cors import CORS
from os import system


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
      back['mp3files'] = subprocess.getoutput('ls /home/pi/sound/*.mp3').split('\n')
      back['songs'] = subprocess.getoutput('mpc ls | sed -n "/mp3/p"').split('\n')
      back['stations'] = subprocess.getoutput('cat  /home/pi/sound/WorldwideFM.m3u').split('\n')
      return [back]
@app.route('/dave', methods=[ 'GET'])
def index():
   if request.method == 'GET':
      value = request.args.get('value')
      seek = request.args.get('seek')
      filemp3 = request.args.get('mp3')
      remove=request.args.get('remove')
      update=request.args.get('update')
      fix=request.args.get('fix')
      insert=request.args.get('insert')
      insert_station=request.args.get('station')
      back={}
      back['songs'] = subprocess.getoutput('mpc ls | sed -n "/mp3/p"').split('\n')
      back['stations'] = subprocess.getoutput('cat  /home/pi/sound/WorldwideFM.m3u').split('\n')

      back['value'] = value
      if filemp3!=None:back['filemp3'] = '/home/pi/sound/'+filemp3
      back['mp3files'] = subprocess.getoutput('ls /home/pi/sound/*.mp3').split('\n')
      if insert!=None:
          back['inserted']=system('mpc insert %s ' % insert)

      if insert_station!=None:
          #insert_station=insert_station.replace('%26','&')
          back['inserted_station']=system('mpc insert "%s" ' % insert_station)

      if value!= None:
          back['checkplay']=system('sleep 1;mpc play %s 1>/dev/null' % value)
          while back['checkplay'] == 256:back['checkplay']=system('sleep 1;mpc play %s 1>/dev/null' % value)

      if seek != None:
         if seek.find('%')>-1:
            subprocess.getoutput('mpc seek %s'%seek)
         else:
            subprocess.getoutput('mpc seek %s'%seek+'%')
      #else:
      #   seek='0%'
      #   subprocess.getoutput('mpc seek %s'%seek)
      back['status'] = subprocess.getoutput('mpc')
      if filemp3!=None:
          back['filemp3'] = '/home/pi/sound/'+filemp3
          print('cp %s /home/pi/Music/j3hour.mp3'% back['filemp3'] )
          subprocess.getoutput('cp %s /home/pi/Music/j3hour.mp3'% back['filemp3'] )
      if remove!=None:
          back['dellog']=subprocess.getoutput('mpc del %s'%remove)
          back['remove']='deleted %s'% remove 
      if fix!=None:
          back['serverstart']=subprocess.getoutput('/home/pi/mpcserver/update' )
      back['serverstart']=subprocess.getoutput('sed -n "/pager/p" /home/pi/mpcserver/update | sh' )

      if update!=None:
          request.args.get('mpc rescan')
          request.args.get('mpc update')
          back['update']='music database rescanned and updated'
      back['playlist'] = subprocess.getoutput('mpc playlist | cat -n').split('\n')
      back['mp3files'] = subprocess.getoutput('ls /home/pi/sound/*.mp3').split('\n')
      back['seek']=seek
      return [back]
   else:
      return 'Use GET requests'

if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0', port=1310)
