import cv2
import os
from random import randint
from scipy.ndimage import rotate
import numpy as np

images = sorted([image for image in os.listdir(r'C:\\Users\\guilherme\\Desktop\\FrameExtractor\\Frames_extracted_with_class\\')])

class FrameTreater:
    def __init__(self):
        pass

    def treat_image(self, effects:list):
        count = 0
        for image in images:
            image_path = os.path.join(r'C:\\Users\\guilherme\Desktop\\FrameExtractor\\Frames_extracted_with_class\\', image)
            dest_path = os.path.join(r'C:\\Users\\guilherme\Desktop\\FrameExtractor\\Frames_extracted_with_class\\', image)
            match effects[count]:
                    case "noise":
                        dest = self._noise(image_path, 0.7)
                        count+=1
                    case "grayscale":
                        dest = self._grey_scale(image_path)
                        count+=1
                    case "random_rotation":
                        dest = self._random_rotation(image_path)
                        count+=1
                    case "flip":
                        dest = self._mirror(image_path)
                        count+=1
                    case _:
                        print("### OPTYPE NOT RECOGNIZED ###")
            cv2.imwrite(dest_path, dest)
                
    def _random_rotation(self, image):
        angle_rand = randint(0, 180) #random angle, in each execution
        source = cv2.imread(image)
        rotated = rotate(source, angle_rand)
        return rotated

    def _mirror(self, image):
        image_read = cv2.imread(image)
        image_mirrowed = np.fliplr(image_read)
        return image_mirrowed

    def _grey_scale(self, image):
        image_read = cv2.imread(image)
        image_gray_scaled = cv2.cvtColor(image_read, cv2.COLOR_BGR2GRAY)
        return image_gray_scaled

    def _noise(self, image, noise_amount):
        image_read = cv2.imread(image)
        output = image_read.copy()

        if len(image_read.shape) == 2:
            black = 0
            white = 255            
        else:
            colorspace = image_read.shape[2]
            if colorspace == 3: 
                black = np.array([0, 0, 0], dtype='uint8')
                white = np.array([255, 255, 255], dtype='uint8')
            else:  # RGBA
                black = np.array([0, 0, 0, 255], dtype='uint8')
                white = np.array([255, 255, 255, 255], dtype='uint8')

        probs = np.random.random(output.shape[:2])
        output[probs < (noise_amount / 2)] = black
        output[probs > 1 - (noise_amount / 2)] = white
        
        return output
