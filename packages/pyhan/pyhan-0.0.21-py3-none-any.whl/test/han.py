import os
import unittest

from ..pyhan import to_traditional


class HanTestCase(unittest.TestCase):
    _dataset2 = {}

    def test_to_traditional(self):
        test_cases = [
            ('萝卜', '蘿蔔'),
            ('卜', '卜'),
        ]
        for simplified, traditional in test_cases:
            self.assertEqual(to_traditional(simplified), traditional)

    def test_file(self):
        base_dir = os.path.dirname(os.path.realpath(__file__))
        file_path2 = os.path.join(base_dir, '../pyhan/files/st02.csv')
        with open(file_path2) as f:
            for i in f:
                arr = i.strip().split(',', 1)
                if arr[0] not in self._dataset2:
                    self._dataset2[arr[0]] = []
                self._dataset2[arr[0]].append(arr[1].split(','))

        for k, i in self._dataset2.items():
            for ii in i:
                if len(ii) > 1:
                    a = ii[0]
                    b = ii[1:]
                    for iii in b:
                        arr = iii.split('|')
                        c = arr[2]

                        start_idx = int(arr[0])
                        end_idx = int(arr[1])

                        idx = 0 - start_idx

                        if start_idx > 0:
                            c = k + '*' * (start_idx - 1) + arr[2]
                            idx = 0
                        if end_idx < 2:
                            c = arr[2] + '*' * (- end_idx) + k
                            idx = -1

                        traditional = to_traditional(c)
                        # print(c, traditional, a, traditional[idx])
                        self.assertEqual(traditional[idx], a)


if __name__ == '__main__':
    unittest.main()
