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
            with self.m as source: self.r.adjust_for_ambient_noise(source)
            with open("recognized.txt","w") as output:
                print("Listening.....")
                with self.m as source: audio = self.r.listen(source)
                try:
                    value = self.r.recognize_google(audio)
                    if str is bytes:
                        print("You said {}".format(value).encode("utf-8"))
                        output.write(str(format(value).encode("utf-8")))
                        output.writelines("\n")
                        return (str(format(value).encode("utf-8")))
                    else:
                        print("You said {}".format(value))
                        output.write(str(format(value)))
                        output.writelines("\n")
                        return (str(format(value)))
                except sr.UnknownValueError:
                    print("Oops! Didn't catch that")
                except sr.RequestError as e:
                    print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))

        except KeyboardInterrupt:
            pass




