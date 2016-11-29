#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import urllib.request
import cv2
import numpy as np
import os


def store_raw_images():
    neg_images_link = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=n03960490'
    neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()
    pic_num = 1

    if not os.path.exists("pos_plate"):
        os.makedirs('pos_plate')

    for i in neg_image_urls.split('\n'):
        try:
            print(i)
            urllib.request.urlretrieve(i, "pos_plate/" + str(pic_num) + ".jpg")
            img = cv2.imread("pos_plate/" + str(pic_num) + ".jpg", cv2.IMREAD_GRAYSCALE)
            # should be larger than samples / pos pic (so we can place our image on it)
            resized_image = cv2.resize(img, (50, 50))
            cv2.imwrite("pos_plate/" + str(pic_num) + ".jpg", resized_image)
            pic_num += 1

        except Exception as e:
            print(str(e))

def edit_image():
    for file_type in ['pos_knife']:
        for img in os.listdir(file_type):
            icv2 = cv2.imread("pos_knife/"+str(img), cv2.IMREAD_GRAYSCALE)
            resized_image = cv2.resize(icv2, (50, 50))
            cv2.imwrite("pos_knife/"+str(img), resized_image)

def find_uglies():
    match = False
    for file_type in ['pos_plate']:
        for img in os.listdir(file_type):
            for ugly in os.listdir('uglies'):
                try:
                    current_image_path = str(file_type)+'/'+str(img)
                    ugly = cv2.imread('uglies/'+str(ugly))
                    question = cv2.imread(current_image_path)
                    if ugly.shape == question.shape and not(np.bitwise_xor(ugly,question).any()):
                        print('That is one ugly pic! Deleting!')
                        print(current_image_path)
                        os.remove(current_image_path)
                except Exception as e:
                    print(str(e))

def create_pos_n_neg():
    for file_type in ['pos_plate']:
        for img in os.listdir(file_type):
            if file_type == 'pos_plate':
                line = file_type + '/' + img + ' 1 0 0 50 50\n'
                with open('info_plate.dat', 'a') as f:
                    f.write(line)
            elif file_type == 'pos_fork':
                line = file_type + '/' + img + ' 1 0 0 50 50\n'
                with open('info_fork.dat', 'a') as f:
                    f.write(line)
            elif file_type == 'pos_knife':
                line = file_type + '/' + img + ' 1 0 0 50 50\n'
                with open('info_knife.dat', 'a') as f:
                    f.write(line)
            elif file_type == 'neg':
                line = file_type + '/' + img + '\n'
                with open('bg.txt', 'a') as f:
                    f.write(line)

create_pos_n_neg()
#store_raw_images()
#find_uglies()
#edit_image()
