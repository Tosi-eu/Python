import subprocess
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

num_images = int(input("Number of images to be processed: "))

os.chdir('/usr/lib/darknet')

image_folder = 'data/train2017'
output_folder = 'predictions'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

processed_images = []

image_files = os.listdir(image_folder)[:num_images]
for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    command = ['./darknet', 'detect', 'cfg/yolov3.cfg', 'yolov3.weights', image_path]
    
    subprocess.run(command, stdout=subprocess.PIPE)
    
    result_image = 'predictions.jpg'
    result_path = os.path.join(output_folder, image_file)
    os.rename(result_image, result_path)
    processed_images.append(result_path)

pdf_path = 'predictions/results.pdf'
with PdfPages(pdf_path) as pdf:
    for image_path in processed_images:
        img = plt.imread(image_path)
        plt.imshow(img)
        plt.title(os.path.basename(image_path))
        plt.axis('off')
        pdf.savefig()
        plt.close()

# for i, res in enumerate(processed_images):
#     print(f"Resultado para a imagem {image_files[i]}:\n{res}")
#     print("-" * 50)
