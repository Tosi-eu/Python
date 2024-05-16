from frame_extractor import FrameExtractor
from frame_treater import FrameTreater
from json_reader import JsonReader

reader = JsonReader()
extractor = FrameExtractor()
treater = FrameTreater()

if __name__ == "__main__":
    video_names = reader.get_file_name()
    frame_seconds = reader.get_frame_seconds_index()
    operation_type = reader.get_operation_type()

    #extractor.call_script(video_names, frame_seconds)
    treater.treat_image(operation_type)