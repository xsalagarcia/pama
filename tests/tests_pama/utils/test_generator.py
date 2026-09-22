import unittest

from pama.utils import generator


class TestGenerator(unittest.TestCase):
    def test_password_generator(self):
        digits_set = '0123456789'
        lower_set = "abcdefghijklmnopqrstuvwxyz"
        upper_set = lower_set.upper()
        special_set = "àáäâèéëêìíïîòóöôùúüûºª!\"·$%&/()=?¿'¡@[]{}-_<>"

        pw = generator.password_generator(length=11, numbers=True, upper_case=True, lower_case=True, special_chars=True)

        def some_in(str_1, str_2) -> bool:
            for char in str_1:
                if char in str_2:
                    return True
            return False

        for i in range(0, 100):
            pw = generator.password_generator(length=11, numbers=True, upper_case=True, lower_case=True,
                                              special_chars=True)
            print(pw)
            self.assertIsInstance(pw, str)
            self.assertTrue(len(pw) == 11)
            self.assertTrue(some_in(pw, digits_set) and some_in(pw, lower_set) and some_in(pw, upper_set) and
                            some_in(pw, special_set))

        for i in range(0, 100):
            pw = generator.password_generator(length=11, numbers=False, upper_case=True, lower_case=True,
                                              special_chars=True)
            print(pw)
            self.assertTrue(len(pw) == 11)
            self.assertIsInstance(pw, str)
            self.assertTrue(not some_in(pw, digits_set) and some_in(pw, lower_set) and some_in(pw, upper_set) and
                            some_in(pw, special_set))

        for i in range(0, 100):
            pw = generator.password_generator(length=11, numbers=False, upper_case=False, lower_case=True,
                                              special_chars=True)
            print(pw)
            self.assertTrue(len(pw) == 11)
            self.assertIsInstance(pw, str)
            self.assertTrue(not some_in(pw, digits_set) and some_in(pw, lower_set) and not some_in(pw, upper_set) and
                            some_in(pw, special_set))

        for i in range(0, 100):
            pw = generator.password_generator(length=11, numbers=False, upper_case=False, lower_case=True,
                                              special_chars=False)
            print(pw)
            self.assertTrue(len(pw) == 11)
            self.assertIsInstance(pw, str)
            self.assertTrue(not some_in(pw, digits_set) and some_in(pw, lower_set) and not some_in(pw, upper_set) and
                            not some_in(pw, special_set))