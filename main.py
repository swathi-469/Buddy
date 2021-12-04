from __future__ import division

import re
import sys
import os
import VirtualMouse as vm
from pynput.keyboard import Key, Controller
import multiprocessing
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="location of google authentication"
import playsound
from threading import Thread
from pynput.keyboard import Key, Controller

# from win32com.client import GetObject

# WMI = GetObject('winmgmts:')
# processes = WMI.InstancesOf('Win32_Process')


from google.cloud import speech
import pyaudio
from six.moves import queue



# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

keyboard = Controller()

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)
stop = False
def play_music():
    print("......")
    playsound.playsound(r'music\\music.mp3')
    global stop
    if stop:
        print("stoppp")
        return 0

def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    flag = False
    # music_thread = Thread(target=play_music)
    music_thread = multiprocessing.Process(target=playsound.playsound,args=("music\music.mp3",))
    name = 'Taskmgr.exe'
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = " " * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:   
            print(transcript+overwrite_chars)  
            # print(flag)    
            if re.search(r"\b(hello buddy|hello birdie|hello body)\b", transcript.lower(), re.I):
                print("Listening...")
                flag = True
            if re.search(r"\b(play music)\b", transcript, re.I) and flag:
                music_thread.start()
                print("music started")
                # process.start()

            if re.search(r"\b(stop|stop music)\b", transcript, re.I) and flag:
                # music_thread.deamon()
                # music_thread.terminate()
                print("music stopped")
                stop=True

            if re.search(r"\b(log off|logoff)\b", transcript, re.I) and flag:
                # os.system("shutdown -l")
                pass

            if re.search(r"\b(turn off|turnoff)\b", transcript, re.I) and flag:
                # os.system('shutdown -s')
                pass
            if re.search(r"\b(sleep)\b", transcript, re.I) and flag:
                # os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                pass

            if re.search(r"\b(restart)\b", transcript, re.I) and flag:
                # os.system("shutdown -t 0 -r -f")
                pass
            
            if re.search(r"\b(open virtual mouse|start virtual mouse|activate virtual mouse)\b", transcript, re.I) and flag:
                print("Activate virtual mouse")
                vm.start_vm()
                print("Deactivate virtual mouse")
            
            if re.search(r"\b(virtual keyboard)\b", transcript, re.I) and flag:
                with keyboard.pressed(Key.cmd_l):
                    with keyboard.pressed(Key.ctrl):
                        keyboard.press('o')
                        keyboard.release('o')

            if re.search(r"\b(open task manager)\b", transcript, re.I) and flag:
                with keyboard.pressed(Key.ctrl):
                    with keyboard.pressed(Key.shift):
                        keyboard.press(Key.esc)
                        keyboard.release(Key.esc)

            if re.search(r"\b(close task manager)\b", transcript, re.I) and flag:
                os.system('wmic process where name="Taskmgr.exe" delete')

            if re.search(r"\b(close current window| close current app| close current tab)\b", transcript, re.I) and flag:
                with keyboard.pressed(Key.alt):
                    keyboard.press(Key.f4)
                    keyboard.release(Key.f4)

            # if re.search(r"\b(Upload file)\b", transcript, re.I) and flag:
            #     print("Sleep..")

            # if re.search(r"\b(open)\b", transcript, re.I) and flag:
            #     print("Sleep..")

            if re.search(r"\b(delete temp file| delete temporary file| delete temprary files| delete temp files)\b", transcript, re.I) and flag:
                del_dir = r'C:\Users\User\AppData\Local\Temp'
                #pObj = subprocess.Popen('rmdir /S /Q %s' % del_dir, shell=True, stdout = subprocess.PIPE, stderr= subprocess.PIPE)

            if re.search(r"\b(time)\b", transcript, re.I) and flag:
                print("Sleep..")

            if re.search(r"\b(weather)\b", transcript, re.I) and flag:
                print("Sleep..")

            if re.search(r"\b(exit|bye|quit)\b", transcript, re.I):
                print("Exiting..")
                flag = False           

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            

            num_chars_printed = 0


def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = "en-US"  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )
    print("started....")
    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        listen_print_loop(responses)



main()