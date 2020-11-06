#!/usr/bin/env python3
from pypresence import Presence
import time, os, subprocess

# Initialize RPC
client_id = "773825528921849856" # DO NOT CHANGE
RPC = Presence(client_id)  # Initialize the Presence client

# Variables
appicon = "appicon" # DO NOT CHANGE
appicon_desc = "Apple Music (macOS)"

# Return number of Apple Music process running (int)
def music_sessions_as():
    return int(subprocess.run(["osascript",
                "-e", "tell application \"System Events\"",
                "-e", "count (every process whose name is \"Music\")",
                "-e", "end tell"], capture_output=True).stdout.decode('utf-8'))

# Return if Apple Music is "playing", "paused" or "stopped"
# Only works when Apple Music is currently running
def music_state_as():
    return subprocess.run(["osascript",
            "-e", "tell application \"Music\"",
            "-e", "if player state is playing then",
            "-e", "set playerStateText to \"playing\"",
            "-e", "else if player state is paused then",
            "-e", "set playerStateText to \"paused\"",
            "-e", "else",
            "-e", "set playerStateText to \"stopped\"",
            "-e", "end if",
            "-e", "end tell"], capture_output=True).stdout.decode('utf-8').rstrip()

# Return [name, artist, album, year, duration, player position] of current track
# Only works when Apple Music is currently running
def music_info_as():
    return subprocess.run(["osascript",
            "-e", "tell application \"Music\"",
            "-e", "get {name, artist, album, year, duration} of current track & {player position}",
            "-e", "end tell"], capture_output=True).stdout.decode('utf-8').rstrip().split(", ")

# Return "playing","paused" or "stopped" at each call whenever Apple Music is running or not
def music_state():
    if music_sessions_as() > 0 : return music_state_as()
    else: return "stopped"

RPC.connect() # Start the handshake loop
while True: # The presence will stay on as long as the program is running
    state = music_state()
    if state=="playing":
        infos = music_info_as()
        RPC.update(
        large_image = appicon,
        large_text = appicon_desc,
        small_image = state, # DO NOT CHANGE
        small_text = "Listening『" + infos[0] + "』by " + infos[1],
        details = infos[0],
        state = infos[1] + " — " + infos[2] + " (" + infos[3] + ")",
        end = time.time() + float(infos[4]) - float(infos[5]))
    elif state=="paused":
        infos = music_info_as()
        RPC.update(
        large_image = appicon,
        large_text = appicon_desc,
        small_image = state, # DO NOT CHANGE
        small_text = "Paused『" + infos[0] + "』by " + infos[1],
        details = infos[0],
        state = infos[1] + " — " + infos[2] + " (" + infos[3] + ")")
    else:
        RPC.update(
        large_image = appicon,
        large_text = appicon_desc,
        small_image = state, # DO NOT CHANGE
        small_text = "Stopped",
        details = "Nothing is playing")
    time.sleep(15)