from flask import Flask, render_template, send_from_directory
import os
from models.frame_treater import FrameTreater
from models.json_reader import JsonReader
from subprocess import call
from time import sleep
from dotenv import load_dotenv

UPLOAD_FOLDER = 'frames/'
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

def process_file(file_path):
    reader = JsonReader(file_path)
    video_names = reader.get_file_name()
    video_secs = reader.get_frame_seconds_index()
    operation_type = reader.get_operation_type()
    treater = FrameTreater()
    
    image_paths = []
    
    for count, (video_name, sec, op_type) in enumerate(zip(video_names, video_secs, operation_type)):
        output_image_name = f'out_{count}.png'
        output_image_path = os.path.join(app.config["UPLOAD_FOLDER"], output_image_name)
        cmd = [
            r'C:\Users\guilherme\Desktop\ffmpeg\bin\ffmpeg.exe',
            '-i', f'C:\\Users\\guilherme\\Desktop\\Python\\Automations\\FrameExtractor\\src\\{video_name}',
            '-vf', f"select='eq(n\,{sec})'",
            '-update', 'true',
            '-vframes', '1',
            output_image_path
        ]
        call(cmd)
        treater.treat_image(output_image_name, str(op_type))
        image_paths.append(output_image_name)
    
    return image_paths

@app.route('/')
def index():
    json_file_path = './static/media/frames.json'
    image_paths = process_file(json_file_path)
    sleep(5)
    return render_template('index.html', images=image_paths)

@app.route('/frames/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
