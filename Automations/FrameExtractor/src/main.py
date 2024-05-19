from frame_extractor import FrameExtractor
from json_reader import JsonReader

reader = JsonReader('./media/frames.json')
extractor = FrameExtractor()

if __name__ == "__main__":
        try:
            video_names = reader.get_file_name()
            frame_seconds = reader.get_frame_seconds_index()
            extractor.call_script(video_names, frame_seconds)
        except Exception as e:
            print(f"### ERROR -> {e} ###")