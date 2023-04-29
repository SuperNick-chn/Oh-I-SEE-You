#!/usr/bin/env python3

# prerequisites: as described in https://alphacephei.com/vosk/install and also python module `sounddevice` (simply run command `pip install sounddevice`)
# Example usage using Dutch (nl) recognition model: `python test_microphone.py -m nl`
# For more help run: `python test_microphone.py -h`

#import textWork

import argparse
import queue
import sys
import sounddevice as sd
from pprint import pprint
from paddlenlp import Taskflow
import json

from vosk import Model, KaldiRecognizer

q = queue.Queue()

global dic
dic = {}

def get_dic():
    return dic

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="audio file to store recording to")
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="input device (numeric ID or substring)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="sampling rate")
parser.add_argument(
    "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
args = parser.parse_args(remaining)

try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info["default_samplerate"])
        
    if args.model is None:
        model = Model("model-cn")
    else:
        model = Model(lang=args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device,
            dtype="int16", channels=1, callback=callback):
        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)

        #global dic

        rec = KaldiRecognizer(model, args.samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                #textWork.solve(rec.Result())
                result = rec.Result()
                #print(result)
                location = result.find('text')
                length = len(result)
                if location + 9 >= length - 3:
                    continue
                text = result[location + 9:length - 3]
                split = text.split()
                text = ''.join(split)
                print(text)
                #ie = Taskflow('word_segmentation')
                #pprint(ie(text))

                ie = Taskflow('information_extraction', schema=['年龄'])
                #pprint(ie(text)[0]['年龄'][0]['text'])

                res = ie(text)[0]
                if res:
                    res = res['年龄'][0]['text']
                    #print(res)
                    age = 0
                    std = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
                    for cha in range(len(res)):
                        flag = -1
                        for stdc in range(len(std)):
                            #print(res[cha], std[stdc])
                            if res[cha] == std[stdc]:
                                flag = stdc
                                break
                        #print(flag)
                        if flag > -1:
                            if age == 0 and flag == 10:
                                age = 1
                            if flag == 10:
                                age = age * 10
                            else:
                                age = age + flag
                    dic['Age'] = age
                
                if ('没' in text) or ('不' in text):
                    if '帽' in text:
                        if 'Hat' in dic:
                            dic.pop('Hat')
                    if '镜' in text:
                        if 'Glasses' in dic:
                            dic.pop('Glasses')
                    if '短袖' in text:
                        if 'ShortSleeve' in dic:
                            dic.pop('ShortSleeve')
                    if '长袖' in text:
                        if 'LongSleeve' in dic:
                            dic.pop('LongSleeve')
                    if (('衣' in text) or ('衫' in text)) and ('条纹' in text):
                        if 'UpperStripe' in dic:
                            dic.pop('UpperStripe')
                    if (('衣' in text) or ('衫' in text)) and ('徽章' in text):
                        if 'UpperLogo' in dic:
                            dic.pop('UpperLogo')
                    if (('衣' in text) or ('衫' in text)) and ('格' in text):
                        if 'UpperPlaid' in dic:
                            dic.pop('UpperPlaid')
                    if (('衣' in text) or ('衫' in text)) and ('拼接' in text):
                        if 'UpperSplice' in dic:
                            dic.pop('UpperSplice')
                    if (('裤' in text) or ('裙' in text)) and ('条纹' in text):
                        if 'LowerStripe' in dic:
                            dic.pop('LowerStripe')
                    if (('裤' in text) or ('裙' in text)) and ('图案' in text):
                        if 'LowerPattern' in dic:
                            dic.pop('LowerPattern')
                    if '外套' in text:
                        if 'LongCoat' in dic:
                            dic.pop('LongCoat')
                    if '长裤' in text:
                        if 'Trousers' in dic:
                            dic.pop('Trousers')
                    if '短裤' in text:
                        if 'Shorts' in dic:
                            dic.pop('Shorts')
                    if '裙' in text:
                        if 'Skirt&Dress' in dic:
                            dic.pop('Skirt&Dress')
                    if '靴' in text:
                        if 'Boots' in dic:
                            dic.pop('Boots')
                    if ('手提包' in text) or ('提' in text):
                        if 'HandBag' in dic:
                            dic.pop('HandBag')
                    if '单肩' in text:
                        if 'ShoulderBag' in dic:
                            dic.pop('ShoulderBag')
                    if ('双肩' in text) or ('背包' in text):
                        if 'Backpack' in dic:
                            dic.pop('Backpack')
                    if '拿' in text:
                        if 'HoldObjectsInFront' in dic:
                            dic.pop('HoldObjectsInFront')
                    if ('Age' in  dic) and dic['Age'] >= 60:
                        if 'AgeOver60' in dic:
                            dic.pop('AgeOver60')
                    if ('Age' in  dic) and dic['Age'] <= 18:
                        if 'AgeLess18' in dic:
                            dic.pop('AgeLess18')
                    if ('Age' in  dic) and 18 <= dic['Age'] and dic['Age'] <= 60:
                        if 'Age18-60' in dic:
                            dic.pop('Age18-60')
                    if '男' in text:
                        if 'Male' in dic:
                            dic.pop('Male')
                    if '女' in text:
                        if 'Female' in dic:
                            dic.pop('Female')
                else:
                    if '帽' in text:
                        if 'Hat' not in dic:
                            dic['Hat'] = 1
                    if '镜' in text:
                        if 'Glasses' not in dic:
                            dic['Glasses'] = 1
                    if '短袖' in text:
                        if 'ShortSleeve' not in dic:
                            dic['ShortSleeve'] = 1
                    if '长袖' in text:
                        if 'LongSleeve' not in dic:
                            dic['LongSleeve'] = 1
                    if (('衣' in text) or ('衫' in text)) and ('条纹' in text):
                        if 'UpperStripe' not in dic:
                            dic['UpperStripe'] = 1
                    if (('衣' in text) or ('衫' in text)) and ('徽章' in text):
                        if 'UpperLogo' not in dic:
                            dic['UpperLogo'] = 1
                    if (('衣' in text) or ('衫' in text)) and ('格' in text):
                        if 'UpperPlaid' not in dic:
                            dic['UpperPlaid'] = 1
                    if (('衣' in text) or ('衫' in text)) and ('拼接' in text):
                        if 'UpperSplice' not in dic:
                            dic['UpperSplice'] = 1 
                    if (('裤' in text) or ('裙' in text)) and ('条纹' in text):
                        if 'LowerStripe' not in dic:
                            dic['LowerStripe'] = 1
                    if (('裤' in text) or ('裙' in text)) and ('图案' in text):
                        if 'LowerPattern' not in dic:
                            dic['LowerPattern'] = 1
                    if '外套' in text:
                        if 'LongCoat' not in dic:
                            dic['LongCoat'] = 1
                    if '长裤' in text:
                        if 'Trousers' not in dic:
                            dic['Trousers'] = 1
                    if '短裤' in text:
                        if 'Shorts' not in dic:
                            dic['Shorts'] = 1
                    if '裙' in text:
                        if 'Skirt&Dress' not in dic:
                            dic['Skirt&Dress'] = 1
                    if '靴' in text:
                        if 'Boots' not in dic:
                            dic['Boots'] = 1
                    if ('手提包' in text) or ('提' in text):
                        if 'HandBag' not in dic:
                            dic['HandBag'] = 1
                    if '单肩' in text:
                        if 'ShoulderBag' not in dic:
                            dic['ShoulderBag'] = 1
                    if ('双肩' in text) or ('背包' in text):
                        if 'Backpack' not in dic:
                            dic['Backpack'] = 1
                    if '拿' in text:
                        if 'HoldObjectsInFront' not in dic:
                            dic['HoldObjectsInFront'] = 1
                    if ('Age' in  dic) and dic['Age'] >= 60:
                        if 'AgeOver60' not in dic:
                            dic['AgeOver60'] = 1
                    if ('Age' in  dic) and dic['Age'] <= 18:
                        if 'AgeLess18' not in dic:
                            dic['AgeLess18'] = 1
                    if ('Age' in  dic) and 18 <= dic['Age'] <= 60:
                        if 'Age18-60' not in dic:
                            dic['Age18-60'] = 1
                    if '男' in text:
                        if 'Male' not in dic:
                            dic['Male'] = 1
                    if '女' in text:
                        if 'Female' not in dic:
                            dic['Female'] = 1
                print(dic)
                tf = open('voice.json', 'w')
                json.dump(dic, tf)
                tf.close()
            else:
                rec.PartialResult()
                #print(rec.PartialResult())
            if dump_fn is not None:
                dump_fn.write(data)

except KeyboardInterrupt:
    print("\nDone")
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))
