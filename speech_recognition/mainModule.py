import speech_recognition as sr
import random

class Speech_Reg:
    def __init__(self):
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        self.STARTUP_FILTER={}

        self.STARTUP_FILTER["GREETING_WORDS"]=["Hi, How may I help you","Hello","What can I do for you Today",
                                  "How may I help you today"," Hi, Ready to eat"]
        print(random.choice(self.STARTUP_FILTER["GREETING_WORDS"]))


    def speech_recognition(self):

        try:
            #print("A moment of silence, please...")
            with self.m as source: self.r.adjust_for_ambient_noise(source)
            #print("Set minimum energy threshold to {}".format(r.energy_threshold))
            with open("recognized.txt","w") as output:
                #print("Say something please!")
                print("Listening Now!")
                with self.m as source: audio = self.r.listen(source)
                #print("Got it! Now to recognize it...")
                try:
                    # recognize speech using Google Speech Recognition
                    value = self.r.recognize_google(audio)

                    # we need some special handling here to correctly print unicode characters to standard output
                    if str is bytes: # this version of Python uses bytes for strings (Python 2)
                        print(u"You said {}".format(value).encode("utf-8"))
                        print(str(format(value).encode("utf-8")))
                        output.write(str(format(value).encode("utf-8")))
                        output.writelines("\n")
                        return (str(format(value).encode("utf-8")))
                    else: # this version of Python uses unicode for strings (Python 3+)
                        print("You said {}".format(value))
                        print(str(format(value)))
                        output.write(str(format(value)))
                        output.writelines("\n")
                        return (str(format(value)))
                except sr.UnknownValueError:
                    print("Oops! Didn't catch that")
                except sr.RequestError as e:
                    print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))

        except KeyboardInterrupt:
            pass




