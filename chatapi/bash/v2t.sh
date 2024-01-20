#!/bin/bash

# Loop until the user decides to stop
while true; do
    # Ask the user if they want to talk
    read -p "speak? (y/n)? " answer

    # Check if the answer is "y" or "Y"
    if [[ $answer = "y" ]] || [[ $answer = "Y" ]]; then
        # Record audio
        echo "Recording & sending ..."
        rec -r 16000 -c 1 -b 16 v2t.wav

        # Check if the recording was successful
        if [[ $? -eq 0 ]]; then
            echo "almost done..."

            # Send the audio file to the remote machine
            sshpass -p 'runescape' scp -P 2212 v2t.wav truffle@172.90.224.13:/home/truffle/chatapi/audio/

            # Check if the file transfer was successful
            if [[ $? -eq 0 ]]; then
                echo "done.."
            else
                echo "Error sending..."
            fi
        else
            echo "Error recording audio."
        fi
    # Check if the answer is "n" or "N"
    elif [[ $answer = "n" ]] || [[ $answer = "N" ]]; then
        # Exit the loop
        break
    else
        echo "Invalid input. Please enter 'y' or 'n'."
    fi
done
