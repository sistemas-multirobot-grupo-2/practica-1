from aurigapy import *
from time import sleep
from time import gmtime, strftime

BASE_SPEED = 40
BASE_TURN = 30

ap = AurigaPy(debug=False)
bluetooth = "/dev/rfcomm1"
ap.connect(bluetooth)
print("Conectado")
lastSpeedo = 'f'

def custom_speeds(robot, speed_L, speed_R):
	# Need to concatenate the hex sequence ff 55 07 00 02 05 <speedleft> <speedright> to the bot's output
	# Since the line follower direction control requires of custom speeds for each wheel, it's convenient to directly call
	# the _write method with a customized string

	# Minor changes to the usual callback generation
	rp = Response.generate_response_block(Frame.FRAME_TYPE_ACK, timeout=2)
	robot.add_responder(rp)

	# Generate hex string based on speeds
	data = bytearray([0xff, 0x55, 0x07, 0x00, 0x02, 0x5] +
	short2bytes(speed_L) +
	short2bytes(speed_R))

	# Write the hex string directly to the bot
	robot._write(data)
	# Wait for callback
	rp.wait_blocking()

while(True):
	value = ap.get_line_sensor(9)

	if(value == 0):
		if(lastSpeedo == "fwds"):
			custom_speeds(ap,-BASE_SPEED,BASE_SPEED)
		elif(lastSpeedo == "bwds"):
			custom_speeds(ap,BASE_SPEED,-BASE_SPEED) # Halt: EotL
		elif(lastSpeedo == "left"):
			custom_speeds(ap,-BASE_SPEED,BASE_SPEED+5) # We "trick" the system into readjusting itself, preventing a possible overcompensation in the turn
		elif(lastSpeedo == "rite"):
			custom_speeds(ap,-BASE_SPEED+5,BASE_SPEED) # Same as before, but this time favouring a slight left turn instead of a right one
		lastSpeedo = "fwds"

	elif(value == 1):
		if(lastSpeedo == "fwds"):
			custom_speeds(ap,-BASE_TURN,-BASE_TURN)
		elif(lastSpeedo == "bwds"):
			custom_speeds(ap,BASE_SPEED,BASE_TURN)
		elif(lastSpeedo == "left"):
			custom_speeds(ap,-BASE_SPEED,-BASE_TURN) # Pronounced left turn, speed up slightly
		elif(lastSpeedo == "rite"):
			custom_speeds(ap,-BASE_SPEED,-BASE_TURN) # Sharp "Z" turn, slow down slightly
		lastSpeedo = "left"

	elif(value == 2):
		if(lastSpeedo == "fwds"):
			custom_speeds(ap,BASE_TURN,BASE_SPEED)
		elif(lastSpeedo == "bwds"):
			custom_speeds(ap,-BASE_TURN,-BASE_SPEED)
		elif(lastSpeedo == "left"):
			custom_speeds(ap,BASE_TURN,BASE_SPEED) # Sharp "Z" turn, slow down slightly
		elif(lastSpeedo == "rite"):
			custom_speeds(ap,BASE_TURN,BASE_SPEED) # Pronounced right turn, speed up slightly
		lastSpeedo = "rite"

	elif(value == 3):
		custom_speeds(ap,BASE_SPEED,-BASE_SPEED)
		lastSpeedo = "bwds"
	#	if(lastSpeedo == "fwds"):
	#		custom_speeds(ap,BASE_SPEED,-BASE_SPEED) # Out of line after forwards action, go backwards
	#		lastSpeedo = "bwds"
	#	elif(lastSpeedo == "bwds"):
	#		custom_speeds(ap,-BASE_SPEED,BASE_SPEED) # OOL after backwards action, go back forwards
	#		lastSpeedo = "fwds"
	#	elif(lastSpeedo == "left"):
	#		custom_speeds(ap,BASE_SPEED,BASE_SPEED) # OOL after left turn, turn right
	#		lastSpeedo = "rite"
	#	elif(lastSpeedo == "rite"):
	#		custom_speeds(ap,-BASE_SPEED,-BASE_SPEED) # OOL after right turn, turn left
	#		lastSpeedo = "left"
