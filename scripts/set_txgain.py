import zmq
import sys, getopt
import time
import random

# Global variables
prevGain = 0
counter = 0
topGain = 84
bottomGain = 24
waveSlope = 1

# Gain update functions
def squareWaveUpdateGain():
    global counter
    if counter<10000000:
        counter += 1
        return 80
    else :
        if counter > 20000000:
			counter = 0
        counter += 1
        return 40

def triangularWaveUpdateGain(prevGain):
	global topGain
	global bottomGain
	global waveSlope

	if prevGain == 0:
		prevGain = (topGain + bottomGain) / 2 
	else:
		time.sleep(10)

	if prevGain >= topGain:
		waveSlope = -1
	if prevGain <= bottomGain:
	    waveSlope = 1

    prevGain += waveSlope

	return prevGain

def randomWaveUpdateGain(prevGain):
	global topGain
	global bottomGain
	global waveSlope

	if prevGain == 0:
		prevGain = random.randint(bottomGain, topGain)
	else:
		time.sleep(10)
		waveSlope = random.randint(-5,5)
		prevGain += waveSlope
        if prevGain > topGain:
            prevGain = topGain
        if prevGain < bottomGain:
            prevGain = bottomGain

	return prevGain


# Sets the tx gain limits depending on the mode (low = 'l', medium = 'm', or high = 'h')   
def setGainLimits(mode):
	modes = ['l', 'm', 'h']
    if mode not in modes:
		print ("Unvalid mode selected")
		return
    if mode == 'l':
		topGain = 38
		bottomGain = 24
    if mode == 'm':
		topGain = 50
        bottomGain = 39
    if mode == 'h':
        topGain = 84
        bottomGain = 51
    return topGain, bottomGain

# Main
def main(argv):
    global prevGain
	if len(argv) < 2:
		print("Not arguments enough. Need tx_gain mode (h, m, or l) and wave mode (trian or rand) ")
		return
    global topGain
    global bottomGain 
    topGain, bottomGain = setGainLimits(argv[0])
    
    if topGain == 84 and bottomGain == 24:
	print("Error setting tx_gain mode") 
        return 0
    if argv[1] == 'trian':
		gainUpdated = triangularWaveUpdateGain(prevGain)
    elif argv[1] == 'rand':
        gainUpdated = randomWaveUpdateGain(prevGain)

    if (prevGain <> gainUpdated):
	try:
        opts, args = getopt.getopt(argv,"hg:o:")
        except getopt.GetoptError:
            print('set_txgain.py -g <gain> ')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('set_txgain.py -p <gain>')
                sys.exit()
            elif opt in ("-g", "--gain"):
                gainUpdated = int(arg)
        print('Requesting tx gain = ', gainUpdated)

        context = zmq.Context()

        #  Socket to talk to server
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5557")

        # CONVERTING GAIN (BASE IS 74)
        gain = gainUpdated-74

        print("Sending request ...")
        socket.send_string(str(gain))

        #  Get the reply.
        message = socket.recv() 
        print("Received reply [ %s ]" % (message))
    prevGain = gainUpdated
    return 1

if __name__ == "__main__":
    running = 1
    while running==1:
	running = main(sys.argv[1:])

