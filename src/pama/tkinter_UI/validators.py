from pama.models.account import Account
from pama.utils import validator
import tkinter as tk

validators = dict()
"""Dict containing validators linked to root component."""

def create_validators(root: tk.Tk):
    """
    Fill dictionary with validators linked to root component.
    :param root:
    :return:
    """
    validators["account name"] = (root.register(lambda value: validator.is_valid(Account, "name", value)), "%P")
    validators["account comments"] = (root.register(lambda value: validator.is_valid(Account, "comments", value)), "%P")
    validators["account url"] = (root.register(lambda value: validator.is_valid(Account, "url", value)), "%P")
