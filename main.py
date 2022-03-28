import serial
import pygame as pg 
import time
import threading 
pg.mixer.init()
pg.init()

#Number of channels repsresents number of sounds, that can be played at the same time
pg.mixer.set_num_channels(130)

#(width, height) = (300, 200)
#screen = pg.display.set_mode((width, height))
#pg.display.flip()

#Serial port config
PORT = "COM4"
BAUDRATE = 9600

#Number of tiles (spoons etc.)
TILES_COUNT = 6



INSTRUMENT = "hand_bells"

instruments = {
	"hand_bells":{
		"path":"Sounds/hand_bells/",
		"files":[
			"c.wav",
			"b.wav",
			"e.wav",
			"f.wav",
			"g.wav",
			"a.wav"
		]
	},
	"piano1":{
		"path":"Sounds/piano/",
		"files":[
			"c1.ogg",
			"d1.ogg",
			"e1.ogg",
			"f1.ogg",
			"g1.ogg",
			"a1.ogg"
		]
	},
	"piano3":{
		"path":"Sounds/piano/",
		"files":[
			"c3.ogg",
			"d3.ogg",
			"e3.ogg",
			"f3.ogg",
			"g3.ogg",
			"a3.ogg"
		]
	},
	"piano7":{
		"path":"Sounds/piano/",
		"files":[
			"c7.ogg",
			"d7.ogg",
			"e7.ogg",
			"f7.ogg",
			"g7.ogg",
			"a7.ogg"
		]
	},
	"guitar":{
		"path":"Sounds/guitar/",
		"files":[
			"c.wav",
			"d.wav",
			"f-chord.wav",
			"g.wav",
			"a.wav",
			"a-chord.wav"
		]
	}
}

buffer = [False] * TILES_COUNT
serial =  serial.Serial(port = PORT, baudrate=BAUDRATE,bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)



def play_note(note_index):
	instrument =  instruments[INSTRUMENT]
	path = instrument["path"]
	files = instrument["files"]
	file = path + files[note_index]
	print(file)
	pg.mixer.Sound(file).play()


def InterpreteNote(note : int):
	for i in range(0,TILES_COUNT):
		value = (note >> i) & 0b1
		if value and not buffer[i]:
			threading.Thread(target=play_note,args=(i,)).start()
			buffer[i] = True
		elif not value and buffer[i]:
			buffer[i] = False
		

def recv():
	if(serial.in_waiting > 0):
		serialString = serial.readline()
		aserialString = serialString.decode('Ascii')
		note = int(aserialString)
		InterpreteNote(note)


while True:
	recv()
