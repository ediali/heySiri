import speech_recognition as sr
import os
import commands
from googleapiclient.discovery import build

api = "AIzaSyCK7ArbfGF__csktWXKtTEdpV82-JRBrg8"

r = sr.Recognizer()
mic = sr.Microphone()


def search():
    print("hey")


global output
output = ""

def main():
    while True:
        vol = commands.getoutput("osascript -e 'tell application \"iTunes\" to sound volume as integer'")

        try:
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, phrase_time_limit=3)
                output = r.recognize_google(audio)

            if "siri" in output or "Siri" in output:
                vol = commands.getoutput("osascript -e 'tell application \"iTunes\" to sound volume as integer'")
                os.system("osascript -e 'tell application \"iTunes\" to set sound volume to 5'")
                print(output)
                voiceControl(vol)

        except sr.RequestError:
            print("Could not connect")

        except sr.UnknownValueError:
            continue


def voiceControl(vol):
    os.system('afplay /System/Library/Sounds/Purr.aiff')

    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, phrase_time_limit = 2)
            output = r.recognize_google(audio)

        if output == "play":
            os.system("osascript -e 'tell application \"iTunes\" to play'")
            os.system("osascript -e 'tell application \"iTunes\" to set sound volume to " + str(vol) + "'")
            print("play")

        elif output == "pause":
            os.system("osascript -e 'tell application \"iTunes\" to pause'")
            print("pause")

        elif "up" in output:
            increaseby = 10
            if int(vol) == 100:
                increaseby = 0
            elif int(vol) > 90:
                increaseby = 100-int(vol)
            elif int(vol) < 90:
                increaseby = 10
            vol = int(vol) + increaseby
            os.system("osascript -e 'tell application \"iTunes\" to set sound volume to " + str(vol) + "'")

        elif "down" in output:
            decreaseby = -10
            if int(vol) == 0:
                decreaseby = 0
            elif int(vol) < 10:
                decreaseby = 10 - int(vol)
            elif int(vol) > 90:
                decreaseby = -10

            vol = int(vol) + decreaseby
            os.system("osascript -e 'tell application \"iTunes\" to set sound volume to " + str(vol) + "'")

        elif "volume" in output:
            print(vol)

            newvol = output.split(" ")[1]
            if int(newvol) > 100:
                vol = 100
            elif int(newvol) < 0:
                vol = 0
            else:
                vol = newvol
            print(vol)
            os.system("osascript -e 'tell application \"iTunes\" to set sound volume to " + str(vol) + "'")


        elif "next" in output:
            os.system("osascript -e 'tell application \"iTunes\" to next track'")
            os.system("osascript -e 'tell application \"iTunes\" to set sound volume to " + str(vol) + "'")
            print("next")
            main()

        elif "previous" in output:
            os.system("osascript -e 'tell application \"iTunes\" to previous track'")
            os.system("osascript -e 'tell application \"iTunes\" to set sound volume to " + str(vol) + "'")
            print("previous")
            main()

        elif "what" and "song" in output:
            track = commands.getoutput("osascript -e 'tell application \"iTunes\" to name of current track as string'")
            artist = commands.getoutput("osascript -e 'tell application \"iTunes\" to artist of current track as string'")
            os.system("say "+track.replace('(','').replace(')','') + "by" + artist)
            os.system("osascript -e 'tell application \"iTunes\" to set sound volume to " + str(vol) + "'")
            print(track)
            main()

        elif "what" in output:
            os.system("osascript -e 'tell application \"iTunes\" to set sound volume to " + str(vol) + "'")

            search()

        else:
            print(output)
            os.system("osascript -e 'tell application \"iTunes\" to set sound volume to " + str(vol) + "'")

            main()

    except sr.RequestError:
        os.system("say Could not connect")
        main()

    except sr.UnknownValueError:
        os.system("say Could not recognize")
        os.system("osascript -e 'tell application \"iTunes\" to set sound volume to " + str(vol) + "'")

        main()


main()