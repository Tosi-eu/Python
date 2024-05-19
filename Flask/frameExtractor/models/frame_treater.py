import cv2
import os
from random import randint, uniform
from scipy.ndimage import rotate
import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
images_path = r'C:\\Users\\guilherme\\Desktop\\Python\\Flask\\frameExtractor\\frames\\'

class FrameTreater:
    def __init__(self):
        pass

    def treat_image(self, image:str, effect:str):
        image_path = f'{images_path}{image}'
        dest_path = f'{images_path}{image}'

        if not os.path.isfile(image_path):
            logging.error(f"Arquivo não encontrado: {image_path}")
            return
        if not self._is_image_readable(image_path):
            logging.error(f"Arquivo não pode ser lido: {image_path}")
            return

        match effect:
            case "noise":
                dest = self._noise(image_path)
                cv2.imwrite(dest_path, dest)
            case "grayscale":
                dest = self._grey_scale(image_path)
                cv2.imwrite(dest_path, dest)
            case "random_rotation":
                dest = self._random_rotation(image_path)
                cv2.imwrite(dest_path, dest)
            case "flip":
                dest = self._mirror(image_path)
                cv2.imwrite(dest_path, dest)

    def _is_image_readable(self, image_path):
        try:
            image = cv2.imread(image_path)
            return image is not None
        except Exception as e:
            logging.error(f"Erro ao tentar ler a imagem {image_path}: {e}")
            return False

    def _random_rotation(self, image):
        angle_rand = randint(0, 180)
        source = cv2.imread(image)
        rotated = rotate(source, angle_rand, reshape=False)
        return rotated

    def _mirror(self, image):
        image_read = cv2.imread(image)
        image_mirrored = np.fliplr(image_read)
        return image_mirrored

    def _grey_scale(self, image):
        image_read = cv2.imread(image)
        image_gray_scaled = cv2.cvtColor(image_read, cv2.COLOR_BGR2GRAY)
        return image_gray_scaled

    def _noise(self, image, noise_amount=uniform(0.4, 0.8)):
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