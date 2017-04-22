from flask import Flask
from flask_pymongo import PyMongo
import pymongo, json
from bson import json_util
import sched, time
import bitly_api
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART



app = Flask(__name__)

#mongo database
mongo = PyMongo(app)
uri = 'mongodb://heroku_6sbfpbmd:bok26mhnk5qipgihm3c78s5krf@ds131890.mlab.com:31890/heroku_6sbfpbmd'
connection = pymongo.MongoClient(uri)
db = connection['heroku_6sbfpbmd']
db.authenticate('heroku_6sbfpbmd','bok26mhnk5qipgihm3c78s5krf')


starting_scores = {}
startPoll = 0
#checks if a reaction can go again
#this increases by one every 5 seconds. When haha is used at time 10 seconds
#haha's canReactDB value is 2. Haha must wait 30 seconds until it can go again
#aka repeatChecker value of 8
repeatChecker = 0
canReactDB = {}
waitUntil = repeatChecker
emojiDB = db.emoji.find()
pollDB = db.poll.find()

for doc in emojiDB:
	starting_scores[doc["name"]] = doc["score"]
	canReactDB[doc["name"]] = -6
for doc in pollDB:
	starting_scores[doc["name"]] = doc["score"]
	canReactDB[doc["name"]] = -6
	startPoll = doc["score"]
scores = {}
s = sched.scheduler(time.time, time.sleep)


# Main function implements the program logic so it can run in a background
# thread.  Most platforms require the main thread to handle GUI events and other
# asyncronous events like BLE actions.  All of the threading logic is taken care
# of automatically though and you just need to provide a main function that uses
# the BLE provider.
def main():
    # Clear any cached data because both bluez and CoreBluetooth have issues with
    # caching data and it going stale.
    ble.clear_cached_data()

    # Get the first available BLE network adapter and make sure it's powered on.
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using adapter: {0}'.format(adapter.name))

    # Disconnect any currently connected UART devices.  Good for cleaning up and
    # starting from a fresh state.
    print('Disconnecting any connected UART devices...')
    UART.disconnect_devices()

    # Scan for UART devices.
    print('Searching for UART device...')
    try:
        adapter.start_scan()
        # Search for the first UART device found (will time out after 60 seconds
        # but you can specify an optional timeout_sec parameter to change it).
        device = UART.find_device()
        if device is None:
            raise RuntimeError('Failed to find UART device!')
    finally:
        # Make sure scanning is stopped before exiting.
        adapter.stop_scan()

    print('Connecting to device...')
    device.connect()  # Will time out after 60 seconds, specify timeout_sec parameter
                      # to change the timeout.

    # Once connected do everything else in a try/finally to make sure the device
    # is disconnected when done.
    try:
        # Wait for service discovery to complete for the UART service.  Will
        # time out after 60 seconds (specify timeout_sec parameter to override).
        print('Discovering services...')
        UART.discover(device)

        # Once service discovery is complete create an instance of the service
        # and start interacting with it.
        uart = UART(device)

        # Write a string to the TX characteristic.

        s.enter(5, 1, check_db, (s,repeatChecker, canReactDB, waitUntil, uart))
        s.run()

        ##should never get here

    finally:
        # Make sure device is disconnected on exit.
        device.disconnect()


def check_db(sc, repeatChecker, canReactDB, waitUntil, uart):
	emojiDB = db.emoji.find()
	pollDB = db.poll.find()

	for doc in emojiDB:
		scores[doc["name"]] = doc["score"]
	for doc in pollDB:
		scores[doc["name"]] = doc["score"]
	print scores

	repeatChecker = repeatChecker + 1

	for score in scores:
		if (scores[score] >= starting_scores[score] + 5) and (repeatChecker - canReactDB[score] > 6) and (waitUntil <= repeatChecker):
			if score == "haha":
				print "large change in " + score + " sending a " + "1" + " to the hardware!"
				send_data(1, uart)
			elif score == "wow":
				print "large change in " + score + " sending a " + "2" + " to the hardware!"
				send_data(2, uart)
			elif score == "love":
				print "large change in " + score + " sending a " + "3" + " to the hardware!"
				send_data(3, uart)
			elif score == "confusion":
				print "large change in " + score + " sending a " + "4" + " to the hardware!"
				send_data(4, uart)
			if score == "poll":
				run_poll()

			canReactDB[score] = repeatChecker
			waitUntil = repeatChecker + 4
			#reset all scores
			for score in scores:
				starting_scores[score] = scores[score]
		elif (scores[score] >= starting_scores[score] + 5) and not (repeatChecker - canReactDB[score] > 6):
			starting_scores[score] = scores[score]
		elif (scores[score] >= starting_scores[score] + 5) and not (waitUntil <= repeatChecker):
			starting_scores[score] = scores[score]

	s.enter(5, 1, check_db, (sc,repeatChecker, canReactDB, waitUntil, uart))



def send_data(data, uart):
	if data is 1:
		uart.write('mo\r\n')	##change to correct  ##right now mo is on and mf is off
	elif data is 2:
		uart.write('mo\r\n')	##change to correct
	elif data is 3:
		uart.write('mf\r\n')	##change to correct	
	elif data is 4:
		uart.write('mf\r\n')	##change to correct		
	print("Sent " + str(data) +  " to the device.")
	# Now wait up to one minute to receive data from the device.
	print('hopefully data given to device...')
	# received = uart.read(timeout_sec=60)
	# if received is not None:
	#     # Received data, print it out.
	#     print('Received: {0}'.format(received))
	# else:
	#     # Timeout waiting for data, None is returned.
	#     print('Received no data!')

	
def run_poll():
	###### use for bitly thing #####
	conn_btly = bitly_api.Connection(access_token='fe3a361216aa47a6a823a32613bba81ddf01cf29')

	#get links
	clicks = conn_btly.link_clicks('http://bit.ly/stc309test', rollup=False, unit='hour')

	numberInAudience = clicks[0]["clicks"] + clicks[1]["clicks"]

	pollDB = db.poll.find()
	currentPoll = 0
	for doc in pollDB:
		if doc["name"] == "poll":
			currentPoll = doc["score"]
	print "the percent of people who agree with the poll is (should be less than 100) " + str((currentPoll-startPoll)/numberInAudience)


# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()

# Initialize the BLE system.  MUST be called before other BLE calls!
ble.initialize()

# Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.
ble.run_mainloop_with(main)


@app.route('/')
def home_page():
    online_users = db.users.find({'online': True})
    return render_template('index.html',
        online_users=online_users)
if __name__ == '__main__':
    app.run(debug = True)