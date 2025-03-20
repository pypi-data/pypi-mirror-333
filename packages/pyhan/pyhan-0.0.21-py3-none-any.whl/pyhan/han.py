import os


class Han:
    _dataset = {}
    _dataset2 = {}

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Han, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            base_dir = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(base_dir, 'files/st00.csv')
            with open(file_path) as f:
                for i in f:
                    arr = i.strip().split(',', 1)
                    self._dataset[arr[0]] = arr[1].split(',')

            file_path2 = os.path.join(base_dir, 'files/st02.csv')
            with open(file_path2) as f:
                for i in f:
                    arr = i.strip().split(',', 1)
                    if arr[0] not in self._dataset2:
                        self._dataset2[arr[0]] = []
                    self._dataset2[arr[0]].append(arr[1].split(','))

    def __predict(self, idx, original, length):
        character = original[idx]
        if character in self._dataset2:
            current = self._dataset2[character]
            for i in current:
                if len(i) > 1:
                    for ii in i[1:]:
                        arr = ii.split('|')

                        start_offset = int(arr[0])
                        end_offset = int(arr[1])

                        start_idx = idx + start_offset
                        end_idx = idx + end_offset

                        if start_idx < 0:
                            continue
                        if end_idx > length:
                            continue
                        if end_idx <= start_idx:
                            continue

                        if original[start_idx:end_idx] == arr[2]:
                            return i[0]
                else:
                    return i[0]

    def __match(self, idx, original, length):
        character = original[idx]
        if character not in self._dataset:
            return character
        else:
            arr = self._dataset[character]
            if len(arr) == 1:
                return arr[0]
            else:
                character_predict = self.__predict(idx, original, length)
                return character_predict if character_predict else character

    def add_rule(self, rule):
        """
        Add conversion rules to only support simplified Chinese characters
        that correspond to multiple traditional Chinese characters

        :param rule:
        :return:

        example:

        add_rule('卜,蔔,-1|0|胡')
        # output: 胡蔔
        print(to_traditional('胡卜'))

        """
        arr = rule.strip().split(',', 1)
        if arr[0] not in self._dataset2:
            self._dataset2[arr[0]] = []
        self._dataset2[arr[0]].insert(0, arr[1].split(','))

    def to_traditional(self, original):
        """
        Convert simplified Chinese characters to traditional Chinese characters

        :param original: 
        :return: 
        """
        length = len(original)
        return ''.join([self.__match(i, original, length) for i in range(length)])


if __name__ == '__main__':
    Han().add_rule('卜,蔔,-1|0|胡')
    print(Han().to_traditional('下台'))
