#Install flask on raspberry pi using
#sudo apt install python3-flask
#sudo apt install python3-flask-cors
####################################
from flask import Flask, request
from flask_cors import CORS


import subprocess

app = Flask(__name__)
CORS(app)


@app.after_request
def add_headers(response):
    response.headers.add('Content-Type', 'application/json')
    response.headers.add(
        'Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS'
    )
    response.headers.add(
        'Access-Control-Allow-Headers', 'content-type, traceid, withcredentials'
    )
    response.status = 200
    return response


@app.route('/')
def helloWorld():
    wfm='wfm1.mp3'
    back = {}
    back['status'] = subprocess.getoutput('mpc')
    back['mp3files'] = subprocess.getoutput('ls /home/pi/sound/*.mp3').split('\n')
    back['stations'] = subprocess.getoutput(
        'cat  /home/pi/sound/WorldwideFM.m3u'
    ).split('\n')
    back['playlist'] = subprocess.getoutput('mpc playlist | cat -n').split('\n')
    back['report_record'] = subprocess.getoutput('id3v2 -l /home/pi/Music/%s'%wfm)
    back['songs'] = subprocess.getoutput('mpc ls').split('\n')
    back['songs'] += subprocess.getoutput('mpc ls m4a').split('\n')
    back['songs'] += subprocess.getoutput('mpc ls mp3').split('\n')
    back['serverstart'] = subprocess.getoutput(
        'sed -n "/pager/p" /home/pi/mpcserver/update | sh'
    )
    return [back]


@app.route('/dave', methods=['GET'])
def index():
    wfm='wfm1.mp3'
    if request.method == 'GET':
        record = request.args.get('record')
        value = request.args.get('value')
        seek = request.args.get('seek')
        filemp3 = request.args.get('mp3')
        remove = request.args.get('remove')
        update = request.args.get('update')
        fix = request.args.get('fix')
        insert = request.args.get('insert')
        move = request.args.get('move')
        insert_station = request.args.get('station')
        back = {}
        back['playlist'] = subprocess.getoutput('mpc playlist | cat -n').split('\n')
        back['stations'] = subprocess.getoutput(
            'cat  /home/pi/sound/WorldwideFM.m3u'
        ).split('\n')

        back['value'] = value
        if filemp3 != None:
            back['filemp3'] = '/home/pi/sound/' + filemp3
        back['mp3files'] = subprocess.getoutput('ls /home/pi/sound/*.mp3').split('\n')
        if move != None:
            move = move.split(' ')
            back["move"]= move
            subprocess.getoutput('mpc move %s %s'%(move[0],move[1]))
        if insert != None:
            insert = insert.replace('%26', '&')
            insert = insert.replace('%2f', '/')

            insert = insert.replace('%58', ':')
            insert = insert.replace('%20', ' ')
            insert = insert.replace('%59', ';')
            insert = insert.replace('%21', '!')
            insert = insert.replace('%23', '#')
            back['inserted'] = subprocess.getoutput('mpc insert "%s" ' % insert)

        if insert_station != None:
            insert_station = insert_station.replace('%26', '&')
            insert_station = insert_station.replace('%58', ':')
            insert_station = insert_station.replace('%20', ' ')
            insert_station = insert_station.replace('%2f', '/')

            insert_station = insert_station.replace('%59', ';')
            insert_station = insert_station.replace('%21', '!')
            insert_station = insert_station.replace('%23', '#')
            back['inserted_station'] = subprocess.getoutput(
                'mpc insert "%s" ' % insert_station
            )

        if record != None:
            back['report_record'] = subprocess.getoutput('rm /home/pi/sound/%s'%wfm)
            back['report_record'] += subprocess.getoutput(
                'ffmpeg -i "http://worldwidefm.out.airtime.pro:8000/worldwidefm_a" -t %s -c copy /home/pi/sound/%s'
                % (record,wfm)
            )
            subprocess.getoutput('id3v2 -y $(date +%Y)'+' /home/pi/sound/%s '%wfm)
            subprocess.getoutput('id3v2 -a "$(date +%d-%B) Recording"'+' /home/pi/sound/%s'%wfm)
            subprocess.getoutput(
                'id3v2 -t "World Wide FM (%s secs)" /home/pi/sound/%s'
                % (record,wfm)
            )
            subprocess.getoutput('id3v2 -A $(date +%H:%M:%S)'+' /home/pi/sound/%s'%wfm)
            back['report_record'] += subprocess.getoutput(
                'id3v2 -l /home/pi/Music/%s'%wfm
            )
            subprocess.getoutput('cp /home/pi/sound/%s /home/pi/Music/%s'%(wfm,wfm))
            subprocess.getoutput('mpc --wait update')
        else:
            back['report_record'] = subprocess.getoutput(
                'id3v2 -l /home/pi/Music/%s'%wfm
            )
        if value != None:
            back['checkplay'] = subprocess.getoutput(
                'sleep 1;mpc play %s 1>/dev/null' % value
            )
            while back['checkplay'] == 256:
                back['checkplay'] = subprocess.getoutput(
                    'sleep 1;mpc play %s 1>/dev/null' % value
                )

        if seek != None:
            if seek.find('%') > -1:
                subprocess.getoutput('mpc seek %s' % seek)
            elif seek != '-1':
                subprocess.getoutput('mpc seek %s' % seek + '%')
        back['status'] = subprocess.getoutput('mpc')
        if filemp3 != None:
            back['filemp3'] = '/home/pi/sound/' + filemp3
            print('cp %s /home/pi/Music/j3hour.mp3' % back['filemp3'])
            subprocess.getoutput('cp %s /home/pi/Music/j3hour.mp3;mpc --wait update' % back['filemp3'])
        if remove != None:
            back['dellog'] = subprocess.getoutput('mpc del %s' % remove)
            back['remove'] = 'deleted %s' % remove

        if update != None:
            back['update'] = subprocess.getoutput(
               #'cp /home/pi/sound/%s /home/pi/Music/%s;mpc --wait update' % (wfm,wfm)
                'mpc --wait update'
            )
            back['update'] += '\n'
            back['update'] += subprocess.getoutput('mpc --wait rescan')
            back['update'] += '\n'
            back['update'] += 'music database rescanned and updated'
        back['mp3files'] = subprocess.getoutput('ls /home/pi/sound/*.mp3').split('\n')
        back['seek'] = seek
        back['playlist'] = subprocess.getoutput('mpc playlist | cat -n').split('\n')
        back['songs'] = subprocess.getoutput('mpc ls').split('\n')
        back['songs'] += subprocess.getoutput('mpc ls m4a').split('\n')
        back['songs'] += subprocess.getoutput('mpc ls mp3').split('\n')
        back['serverstart'] = ''
        if fix != None:
            back['serverstart'] += subprocess.getoutput('/home/pi/mpcserver/update')
        back['serverstart'] += subprocess.getoutput(
            'sed -n "/pager/p" /home/pi/mpcserver/update | sh'
        )
        return [back]
    else:
        return 'Use GET requests'


if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=1310)
