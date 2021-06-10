import zmq
import sys, getopt

def main(argv):
    if argv[0] == 'h':
	gain = 63
    elif argv[0] == 'm':
	gain = 45
    elif argv[0] == 'l':
	gain = 31
    else:
	gain = 85 
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
            gain = int(arg)
    print('Requesting tx gain = ', gain)

    context = zmq.Context()

    #  Socket to talk to server
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5557")


    # CONVERTING GAIN (BASE IS 74)
    gain = gain-74

    print("Sending request ...")
    socket.send_string(str(gain))

    #  Get the reply.
    message = socket.recv()
    print("Received reply [ %s ]" % (message))

if __name__ == "__main__":
   main(sys.argv[1:])
