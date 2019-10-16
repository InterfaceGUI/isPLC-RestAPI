from flask import abort
from flask import Flask
from flask import request, json, jsonify

import isPLC_Package.isPLC

import time
import datetime
import sys
import os

plc = isPLC_Package.isPLC.ClassCGS_isPLC(0x01)


#plc.open('/dev/ttyACM0')
plc.open('COM4')
info = plc.Version

print(info)
api = Flask(__name__)



@api.route('/Read', methods=['GET'])
def get_Read():
    r = request.args

    prefix = r['q'][:1].lower()

    if prefix == "x":
        rrr = plc.Read_coils('X')
        return jsonify({'x':rrr}), 200

    elif prefix == "y":
        rrr = plc.Read_coils('Y')
        return jsonify({'y':rrr}), 200

    elif prefix == "d":
        rrr = plc.ReadRegister(int(r['q'][1:]))

        return jsonify({'D':rrr}), 200

    else:
        abort(400, 'Unknow args')

@api.route('/Read/M', methods=['GET'])
def get_ReadM():
    r = request.args
    print(r['n'])
    rrr = plc.Read_coil('M'+r['n'])
    return jsonify({'m':rrr}), 200

@api.route('/Write', methods=['GET'])
def get_Write():
    r = request.args
    rdict = r.to_dict()
    kist = [(k,v) for k,v in rdict.items()][0]
    E = kist[0][0]
    ID = int(kist[0][1])
    B = bool(int(kist[1]))
    plc.Write_coil(E,ID,B)

    return {'Status':'OK'} , 200

@api.route('/Write/Reg', methods=['GET'])
def get_WriteReg():
    r = request.args
    rdict = r.to_dict()
    kist = [(k,v) for k,v in rdict.items()][0]
    E = kist[0][0]
    ID = int(kist[0][1])
    V = bool(int(kist[1]))
    plc.Write_Register(ID,V)

    return {'Status':'OK'} , 200

helps = ('/help  Show API Helps <br><br>'
         '/Read?q=x0  , /Read/?q=y1 , /Read/?q=d0 ; Return {"Y":True}... <br><br>'
         '/Read/M?n=0 ; Return {"M0":True}... <br><br>'
         '/Write?M0=1 , /Write?Y0=1 ; Return {"status":"OK"}... <br><br>'
         '/Write/Reg?D0=1023 ,/Write/Reg?D1=0  ; Return {"status":"OK"}... <br><br>'
        )

@api.route('/help', methods=['GET'])
def get_help():

    return helps,200

@api.route('/', methods=['GET'])
def get_Information():
    return 'isPLC_RestAPI', 200



if __name__ == '__main__':
    #api.run(host='0.0.0.0', port=25565)
    api.run(host='127.0.0.1', port=25565)
