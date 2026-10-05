"""sentence-splitter-lite 单元测试（覆盖大量边界）。运行：python3 -m unittest discover -s tests"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from splitter import split_sentences  # noqa: E402


class TestBasic(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(split_sentences(""), [])
        self.assertEqual(split_sentences("   "), [])

    def test_chinese(self):
        s = split_sentences("你好。世界！今天天气真好？")
        self.assertEqual(len(s), 3)

    def test_english(self):
        s = split_sentences("Hello world. How are you?")
        self.assertEqual(len(s), 2)


class TestAbbreviation(unittest.TestCase):
    def test_dr(self):
        s = split_sentences("Dr. Smith went home. He was tired.")
        self.assertEqual(len(s), 2)
        self.assertTrue(s[0].startswith("Dr."))

    def test_etc(self):
        s = split_sentences("We bought apples, bananas, etc. Then we left.")
        self.assertEqual(len(s), 2)

    def test_eg(self):
        s = split_sentences("Fruits (e.g. apple) are nice. Good bye.")
        self.assertEqual(len(s), 2)


class TestDecimal(unittest.TestCase):
    def test_pi(self):
        s = split_sentences("The value of pi is 3.14159. Amazing.")
        self.assertEqual(len(s), 2)
        self.assertIn("3.14159", s[0])


class TestEllipsis(unittest.TestCase):
    def test_three_dots(self):
        s = split_sentences("Wait... what do you mean?")
        self.assertEqual(len(s), 1)

    def test_cjk_ellipsis(self):
        s = split_sentences("他沉默了……然后转身离开。")
        self.assertEqual(len(s), 1)


class TestStackedPunct(unittest.TestCase):
    def test_stacked(self):
        s = split_sentences("Really?! Are you serious!!? Yes.")
        self.assertEqual(len(s), 3)
        self.assertEqual(s[0], "Really?!")

    def test_cjk_stacked(self):
        s = split_sentences("这怎么可能！？太惊人了。真的吗？")
        self.assertEqual(len(s), 3)


class TestQuotes(unittest.TestCase):
    def test_closing_quote(self):
        s = split_sentences('He said "Hello world." Then he left.')
        self.assertEqual(len(s), 2)
        self.assertTrue(s[0].endswith('"'))

    def test_cjk_quotes(self):
        s = split_sentences('他说：“你好。”然后离开了。')
        self.assertEqual(len(s), 2)


if __name__ == "__main__":
    unittest.main()
