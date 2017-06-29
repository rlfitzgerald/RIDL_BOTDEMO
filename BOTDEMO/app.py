#!/usr/bin/env python
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import folium_gen_map
import pdb
import genplotly
import time
#import test
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')



@app.route('/map/<loc>')
def gen_map(loc):
	locstring =loc.split(",")
	lat = float(locstring[0])
	lon = float(locstring[1])
	try:
		geojson = locstring[2]
	except:
		map_string=folium_gen_map.mmap(lat,lon)
		if len(loc) == 0:
			loc = time.ctime()	
		socketio.emit('gen_map',{'data':map_string,'text':loc},namespace='/test')		
		return  'complete'
	map_string=folium_gen_map.mmap(lat,lon,geojson=geojson)
	socketio.emit('gen_map',{'data':map_string},namespace='/test')		
	return 'test' 

@app.route('/plotships/')
def gen_ship_map():
	timestamp = time.ctime()
	locs = folium_gen_map._get_locs("shiplocs.csv")
	map_string = folium_gen_map._gen_map_locs(locs)		
	socketio.emit('gen_map',{'data':map_string,"text":timestamp},namespace='/test')		
	return 'ffff'

@app.route("/genplot/")
def gen_plotly():
	plotdata = genplotly.gen_barchart()
	socketio.emit('addplotly',{'data':plotdata},namespace='/test')		
	return 'foo' 
@app.route('/text/<txt>')
def gen_text(txt):
	timestamp = time.ctime()	
	socketio.emit('gen_text',{'data':txt,'text':timestamp},namespace='/test')		
	return "complete"


@app.route('/removelast/')
def remove_child_divs():
	socketio.emit('removediv',{'data':'last'},namespace='/test')
	return "complete"

@app.route("/refresh")
def refresh():
        socketio.emit('refresh',{'data':map_string},namespace='/test')


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})

@socketio.on('testtest',namespace='/test')
def test_test(message):
	print ('test',message)
	
@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000)
