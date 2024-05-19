import subprocess as sub
from models.frame_treater import FrameTreater
from models.json_reader import JsonReader

image_path = r'C:\\Users\\guilherme\\Desktop\\Python\\Automations\\FrameExtractor\\Frames_extracted_with_class\\'
treater = FrameTreater()
reader = JsonReader('./static/media/frames.json')
operation_type = reader.get_operation_type()

class FrameExtractor:
    def __init__(self):
        pass

    def call_script(self, video_name, video_sec):
        count = 0
        try:
            for frame, sec in zip(video_name, video_sec):
                cmd = [
                    r'C:\Users\guilherme\Desktop\ffmpeg\bin\ffmpeg.exe',
                    '-y', '-i', f'C:\\Users\\guilherme\\Desktop\\Python\\Automations\\FrameExtractor\\src\\{frame}',
                    '-vf', f"select='eq(n\,{sec})'",
                    '-update', 'true',
                    '-vframes', '1',
                    f'{image_path}out_%d.png' % (count)
                ]
                sub.call(cmd)
                print(operation_type[count])
                print(video_name[count])
                treater.treat_image(f'./static/frames/out_{count}.png', str(operation_type[count]))
                count += 1
        except Exception as e:
            print(f"### ERROR {e}")