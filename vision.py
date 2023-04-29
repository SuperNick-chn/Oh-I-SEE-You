import cv2
import numpy as np
import os
import shutil
import csv
import json



class SemanticAnalyzer(object):

    def __init__(self):
        i = 1 
        #os.system('python /home/Bishe/voice.py')

    def get(self):
        tf = open('/home/Bishe/voice.json', 'r')
        return json.load(tf)
        

class PedDetAndAttrRec(object):
    
    def __init__(self):
        i = 1

    def run(self):
        ret = os.system('python /home/Bishe/PaddleDetection/deploy/pipeline/pipeline.py --config PaddleDetection/deploy/pipeline/config/infer_cfg_pphuman.yml --image_file=/home/Bishe/input/test.jpg --device=gpu --output_dir=/home/Bishe/result')
        print('ret = ', ret)

    def get(self) -> list:
        ans = []
        with open('result/test.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                ans.append(line)
        return ans
        

class ConmmunicationWithFront(object):

    def __init__(self):
        i = 1

    def show(self, person:list, maxn:int):
        if maxn <= 0:
            print('no fit')
        else:
            print(answer)


if __name__ == '__main__':
    shutil.rmtree('voice')
    os.mkdir('voice')
    SA = SemanticAnalyzer()
    PDAAR = PedDetAndAttrRec()
    CWF = ConmmunicationWithFront()
    capture = cv2.VideoCapture(2)
    while True:
        shutil.rmtree('result')
        os.mkdir('result')
        ret, image = capture.read()
        if ret == False:
            print('ERROR: Cannot read from camera!')
            break
        # print('success')
        cv2.imwrite("input/origin.jpg", image)

        PDAAR.run()

        token_res = SA.get()
        print(token_res)
        
        attr_res = PDAAR.get()

        scores = []

        for boxes in attr_res:
            print(boxes)
            score = 0
            for token in token_res:
                if token == 'Glasses':
                    if boxes.find('Glasses:  False') > -1:
                        score -= 1
                    else:
                        score += 1
                elif token == 'Hat':
                    if boxes.find('Hat:  False'):
                        score -= 1
                    else:
                        score += 1
                elif token == 'HoldObjectsInFront':
                    if boxes.find('HoldObjectsInFront:  False'):
                        score -= 1
                    else:
                        score += 1
                elif token == 'Boots':
                    if boxes.find('No  boots'):
                        score -= 1
                    else:
                        score += 1
                elif boxes.find(token):
                    score += 1
                else:
                    score -= 1
                print(token, score)
            print('score=', score)
            scores.append(score)
        
        answer = []
        for person in range(len(scores)):
            if scores[person] == max(scores):
                answer.append(person)
        CWF.show(answer, max(scores))
        

        break 

        cv2.waitKey(50)

        
        
        


        
