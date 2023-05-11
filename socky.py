import websocket
import _thread
import time
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
mcnt = 0
def read_file_lines(file_path):
    with open(file_path, 'r') as file:
        contents = file.read()
        lines = contents.split('\n')
    return lines
response = []
def intrude(payloads,socketmsg,ws):
    # Insert characters: ~$~
    # Socket message: 425["msg","~$~","static","loadAvailableReinYears",{}]
    # Each payload will be inserted at the marked locations and the message is sent.
    # If a response is received, the response is logged for review
    cnt = 0
    print("Intrude starting...")
    msg = ""
    for payload in read_file_lines("./payloads.txt"):
        msg = socketmsg.replace("~$~",payload)
        print(f"Sending message: {msg}")
        ws.send(msg)
        logging.info(f'[{cnt}] {msg}')
        time.sleep(.100)
        cnt += 1

def on_message(ws, message):
    global mcnt
    if mcnt >= 6:
        print("\n[socket-server]\n" + message + "\n\n")
        logging.info(f'[{mcnt-6}] {message}')
    mcnt += 1

def on_error(ws, error):
    print("Error: %s" % error)

def on_close(ws):
    print("### WebSocket closed ###")

def on_open(ws):
    def run(*args):
        ws.send('send message')

    _thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(False)
    custom_headers = [
        "Cookie: asnaprodsid=",
    ]
    ws = websocket.WebSocketApp("wss://url",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                header=custom_headers)
    ws.on_open = on_open
    ws.run_forever()
