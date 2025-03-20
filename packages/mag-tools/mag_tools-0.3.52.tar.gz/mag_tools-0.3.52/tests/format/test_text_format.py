import unittest

from mag_tools.format.text_formatter import TextFormatter

from mag_tools.model.justify_type import JustifyType


class TestTextFormat(unittest.TestCase):
    def setUp(self):
        self.format = TextFormatter(
            number_per_line=3,
            justify_type=JustifyType.LEFT,
            at_header='   ',
            decimal_places=3,
            decimal_places_of_zero=3,
            pad_length=None,
            pad_char=' ',
            scientific=False,
            none_default='NA'
        )

    def test_array_1d_to_lines(self):
        text_format = TextFormatter(number_per_line=3, justify_type=JustifyType.LEFT)

        # 测试整数数组
        array_1d = [1, 1, 2, 3, 3, 3]
        expected_output = ['2*1 2   3*3']
        result = text_format.array_1d_to_lines(array_1d)
        self.assertEqual(result, expected_output)

        # 测试浮点数数组
        array_1d = [1.1, 1.1, 2.2, 3.3, 3.3, 3.3]
        expected_output = ['2*1.1 2.2   3*3.3']
        result = text_format.array_1d_to_lines(array_1d)
        self.assertEqual(result, expected_output)

        # 测试布尔值数组
        array_1d = [True, True, False, True, True, True]
        expected_output = ['2*True False  3*True']
        result = text_format.array_1d_to_lines(array_1d)
        self.assertEqual(result, expected_output)

        # 测试字符串数组
        array_1d = ['a', 'a', 'b', 'c', 'c', 'c']
        expected_output = ['2*a b   3*c']
        result = text_format.array_1d_to_lines(array_1d)
        self.assertEqual(result, expected_output)

    def test_array_2d_to_lines(self):
        text_format = TextFormatter(number_per_line=3, justify_type=JustifyType.LEFT)

        # 测试整数数组
        array_2d = [
            [1, 1, 2],
            [3, 3, 3]
        ]
        expected_output = ['2*1 2   3*3']
        result = text_format.array_2d_to_lines(array_2d)
        self.assertEqual(result, expected_output)

        # 测试浮点数数组
        array_2d = [
            [1.1, 1.1, 2.2],
            [3.3, 3.3, 3.3]
        ]
        expected_output = ['2*1.1 2.2   3*3.3']
        result = text_format.array_2d_to_lines(array_2d)
        self.assertEqual(result, expected_output)

        # 测试布尔值数组
        array_2d = [
            [True, True, False],
            [True, True, True]
        ]
        expected_output = ['2*True False  3*True']
        result = text_format.array_2d_to_lines(array_2d)
        self.assertEqual(result, expected_output)

        # 测试字符串数组
        array_2d = [
            ['a', 'a', 'b'],
            ['c', 'c', 'c']
        ]
        expected_output = ['2*a b   3*c']
        result = text_format.array_2d_to_lines(array_2d)
        self.assertEqual(result, expected_output)

    def test_array_3d_to_lines(self):
        text_format = TextFormatter(number_per_line=3, justify_type=JustifyType.LEFT)

        # 测试整数数组
        array_3d = [
            [
                [1, 1, 2],
                [2, 3, 3]
            ],
            [
                [4, 4, 5],
                [5, 6, 6]
            ]
        ]
        expected_output = ['2*1 2*2 2*3', '2*4 2*5 2*6']
        result = text_format.array_3d_to_lines(array_3d)
        self.assertEqual(expected_output, result)

        # 测试浮点数数组
        array_3d = [
            [
                [1.1, 1.1, 2.2],
                [3.3, 3.3, 3.3]
            ],
            [
                [4.4, 4.4, 5.5],
                [6.6, 6.6, 6.6]
            ]
        ]
        expected_output = ['2*1.1 2.2   3*3.3', '2*4.4 5.5   3*6.6']
        result = text_format.array_3d_to_lines(array_3d)
        self.assertEqual(expected_output, result)

        # 测试布尔值数组
        array_3d = [
            [
                [True, True, False],
                [True, True, True]
            ],
            [
                [False, False, True],
                [False, False, False]
            ]
        ]
        expected_output = ['2*True False  3*True', '2*False True    3*False']
        result = text_format.array_3d_to_lines(array_3d)
        self.assertEqual(expected_output, result)

        # 测试字符串数组
        array_3d = [
            [
                ['a', 'a', 'b'],
                ['c', 'c', 'c']
            ],
            [
                ['d', 'd', 'e'],
                ['f', 'f', 'f']
            ]
        ]
        expected_output = ['2*a b   3*c', '2*d e   3*f']
        result = text_format.array_3d_to_lines(array_3d)
        self.assertEqual(expected_output, result)