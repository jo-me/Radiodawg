import os
import time
import sys

TIMEOUT_SEC = 1
DNS_TO_QUERY = "8.8.8.8"
MUTE = " > /dev/null 2>&1"
MIN_DROPPED_PACKETS = 2

def stop_playback():
    print("Stopping Volumio playback...")
    sys.stdout.flush()
    os.system("volumio stop")

def start_playback():
    print("Starting Volumio playback...")
    sys.stdout.flush()
    os.system("volumio play")

def is_net_reachable():
    response = os.system("ping -c 1 " + DNS_TO_QUERY + MUTE)
    if response is 0:
        return True
    else:
        return False

def is_connection_down():
    dropped_packets = 0
    if is_net_reachable():
        return False
    else:
        dropped_packets += 1
        while dropped_packets <= MIN_DROPPED_PACKETS:
            if dropped_packets == MIN_DROPPED_PACKETS:
                return True
            else:
                if is_net_reachable():
                    return False
                dropped_packets += 1

def is_streaming_webradio():
    response = os.system("volumio status | grep webradio" + MUTE)
    if response is 0:
        return True
    else:
        return False

while True:
    if is_streaming_webradio():
        if is_connection_down():
            print(DNS_TO_QUERY + " is not reachable (" + str(MIN_DROPPED_PACKETS) 
                    + " subsequently dropped packets), stopping Volumio playback")
            sys.stdout.flush()
            stop_playback()
            while not is_net_reachable():
                print(DNS_TO_QUERY + " is still not reachable, trying again in " + str(TIMEOUT_SEC) + " sec")
                sys.stdout.flush()
                time.sleep(TIMEOUT_SEC)
            print(DNS_TO_QUERY + " is reachable again, resuming Volumio playback now")
            sys.stdout.flush()
            start_playback()

    time.sleep(TIMEOUT_SEC)
