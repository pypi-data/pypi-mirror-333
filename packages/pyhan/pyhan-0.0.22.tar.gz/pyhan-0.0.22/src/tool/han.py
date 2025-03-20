import json
import os


class Han:
    _dataset = {}

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Han, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            base_dir = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(base_dir, '../pyhan/files/st00.csv')
            with open(file_path) as f:
                for i in f:
                    arr = i.strip().split(',', 1)
                    if arr[0] not in self._dataset:
                        self._dataset[arr[0]] = [arr[1].split(','), []]

            file_path2 = os.path.join(base_dir, '../pyhan/files/st02.csv')
            with open(file_path2) as f:
                for i in f:
                    arr = i.strip().split(',', 1)
                    if arr[0] not in self._dataset:
                        continue
                    self._dataset[arr[0]][1].append([x.split('|') for x in arr[1].split(',')[1:]])


if __name__ == '__main__':
    print(json.dumps(Han()._dataset, ensure_ascii=False))
    # print(json.dumps(Han()._dataset, ensure_ascii=False, indent=2))
