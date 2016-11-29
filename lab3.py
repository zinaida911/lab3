#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import cv2
import math

def maxmin(number1,number2):
    if number1>number2:
        max = number1
        min = number2
    else:
        max = number2
        min = number1
    return max, min

def dis(p1x,p1y, p2x, p2y):
    return math.sqrt((p1x-p2x)*(p1x-p2x)+(p1y-p2y)*(p1y-p2y))

def centerPoint(p1x,p1y, p2x, p2y):
    maxX, minX = maxmin(p1x,p2x)
    maxY, minY = maxmin(p1y, p2y)
    return int(minX+(maxX-minX)/2), int(minY+(maxY-minY)/2)

eyes_cascade = cv2.CascadeClassifier('cascades/haarcascade_eye.xml');
mouth_cascade = cv2.CascadeClassifier('cascades/Mouth.xml')

image = cv2.imread('tests/5.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

font = cv2.FONT_HERSHEY_SIMPLEX

eyes = eyes_cascade.detectMultiScale(gray,1.2,15)
mouths = mouth_cascade.detectMultiScale(gray,2,15)

print("Найдено глаз - ", len(eyes))
print("Найдено ртов - ", len(mouths))
if len(eyes)>1:
    eye_combo = []
    for i in range (0, len(eyes), 1):
        eye1_x, eye1_y, eye1_w, eye1_h = eyes[i]
        if i != len(eyes) - 1:
            for j in range (i+1, len(eyes), 1):
                eye2_x, eye2_y, eye2_w, eye2_h = eyes[j]
                maxW, minW = maxmin(eye1_w,eye2_w)
                if (int((dis(eye1_x, eye1_y,eye2_x, eye2_y)-(eye1_w+eye2_w)/2)) > minW*0.6 and int((dis(eye1_x, eye1_y,eye2_x, eye2_y)-(eye1_w+eye2_w)/2))< maxW*1.5 ):
                    eye_combo.append([i,j])
    print("Найдено возможных пар глаз - ", len(eye_combo))
    face_combo =[]
    for i in range(0,len(mouths),1):
        mounth_x, mounth_y, mounth_w, mounth_h = mouths[i]
        for item in eye_combo:
            eye1_x, eye1_y, eye1_w, eye1_h = eyes[item[0]]
            eye2_x, eye2_y, eye2_w, eye2_h = eyes[item[1]]
            center = centerPoint(eye1_x + int(eye1_w / 2), eye1_y+ int(eye1_h / 2), eye2_x + int(eye2_w / 2), eye2_y+ int(eye2_h / 2))
            eyeW, eyeH = (eye1_w+eye2_w)/2, (eye1_h+eye2_h)/2
            mounth_xm, mounth_ym = int(mounth_x+mounth_w/2), int(mounth_y+mounth_h/2)
            maxH,minH = maxmin(eyeH,mounth_h)
            if (int((dis(center[0], center[1], mounth_xm, mounth_ym) - (eyeH + mounth_h) / 2)) > minH * 0.6 and int((dis(center[0], center[1], mounth_xm, mounth_ym) - (eyeH + mounth_h) / 2)) < maxW * 1.5):
                face_combo.append([item[0],item[1],i])
    if len(face_combo)!=0:
        print("Найдено потенциальных лиц - ", len(face_combo))
    print("Анализ лицевых треугольников")
    face_filtered = []
    for item in face_combo:
        eye1_x, eye1_y, eye1_w, eye1_h = eyes[item[0]] #A
        eye2_x, eye2_y, eye2_w, eye2_h = eyes[item[1]] #B
        mounth_x, mounth_y, mounth_w, mounth_h = mouths[item[2]] #C
        eye1_x, eye1_y = int(eye1_x+eye1_w/2), int(eye1_y+eye1_h/2)
        eye2_x, eye2_y = int(eye2_x+eye2_w/2), int(eye2_y+eye2_h/2)
        mounth_x, mounth_y = int(mounth_x+ mounth_w/2), int(mounth_y+mounth_h/2)
        AB = dis(eye1_x,eye1_y,eye2_x,eye2_y)
        AC = dis(eye1_x,eye1_y,mounth_x, mounth_y)
        BC = dis(eye2_x, eye2_y,mounth_x, mounth_y)
        if ((AC+BC)/2) > AB:
            if (eye1_w*eye1_h+eye2_w*eye2_h)/2 < mounth_w*mounth_h*1.28:
                cd = (AC+BC)/2
                if AC > cd*0.9 and AC < cd*1.1 and BC > cd*0.9 and BC < cd*1.1:
                    face_filtered.append(item)
                    cv2.line(image, (eye1_x, eye1_y), (eye2_x, eye2_y), (255, 255, 0), 2)
                    cv2.line(image, (eye1_x, eye1_y), (mounth_x, mounth_y), (255, 0, 255), 2)
                    cv2.line(image, (eye2_x, eye2_y), (mounth_x, mounth_y), (255, 0, 255), 2)
    print("Найдено уникальных лиц - ", len(face_filtered))
else:
    print("Надено слишком мало глаз...")
cv2.imshow('img', image)
cv2.waitKey(0)