import subprocess as sub

image_path = 'C:\\Users\\guilherme\\Desktop\\FrameExtractor\\Frames_extracted_with_class\\'

class FrameExtractor:
    def __init__(self):
        pass

    def call_script(self, video_name, video_sec):
        count = 0
        try:
            for frame, sec in zip(video_name, video_sec):
                cmd = [
                    r'C:\Users\guilherme\Desktop\ffmpeg\bin\ffmpeg.exe',
                    '-i', f'C:\\Users\\guilherme\\Desktop\\FrameExtractor\\src\\{frame}',
                    '-vf', f"select='eq(n\,{sec})'",
                    '-vframes', '1',
                    f'{image_path}%d.png' % (count + 1)
                ]
                sub.call(cmd, shell=True)
                count += 1
        except Exception as e:
            print(f"### ERROR {e}")
            exit(1)