import pandas as pd

class JsonReader:
    def __init__(self, file_path):
        self._file = pd.read_json(file_path)

    def get_file_name(self):
        try:
            file_names = self._file['video_ref'].tolist()
            return file_names
        except KeyError as e:
            print(f"FILE NAME ERROR: {e}")
            return []

    def get_frame_seconds_index(self):
        try:
            frame_seconds = self._file['frame_seconds_index'].tolist()
            return frame_seconds
        except KeyError as e:
            print(f"FRAME ERROR: {e}")
            return []

    def get_operation_type(self):
        try:
            operation_types = self._file['op_type'].tolist()
            return operation_types
        except KeyError as e:
            print(f"OPERATION TYPE ERROR: {e}")
            return []
