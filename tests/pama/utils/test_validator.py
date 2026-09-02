import unittest

from sqlmodel import SQLModel, Field

from pama.models.account import Account
from pama.utils.validator import is_valid


class TestValidator(unittest.TestCase):

    def test_is_valid(self):
        class TestModel(SQLModel):
            test_field_1: str = Field(max_length=127, unique=True)
            test_field_2: int = Field(lt=5)

        self.assertFalse(is_valid(TestModel, "test_field_1", "a"*128))
        self.assertTrue(is_valid(TestModel, "test_field_1", "a"*127))
        self.assertFalse(is_valid(TestModel, "test_field_2", 5))
        self.assertTrue(is_valid(TestModel, "test_field_2", 4))
