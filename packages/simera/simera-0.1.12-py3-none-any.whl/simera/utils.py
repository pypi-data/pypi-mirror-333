import pandas as pd
import numpy as np
import yaml


class DataInputError(Exception):
    """Exception raised for errors in Excel file input.

    Attributes:
        message (str): Description of the error.
        file (str, optional): The file path of the Excel document.
        worksheet (str, optional): The worksheet where the error occurred.
        column (str, optional): The column that caused the issue.
        values (list, optional): The specific values that generated the error.
    """

    def __init__(self, message, file=None, worksheet=None, column=None, values=None):
        super().__init__(message)
        self.file = file
        self.worksheet = worksheet
        self.column = column
        self.values = values

    def __str__(self):
        details = [
            f"File: {self.file}" if self.file else None,
            f"Worksheet: {self.worksheet}" if self.worksheet else None,
            f"Column: {self.column}" if self.column else None,
            f"Values: {repr(self.values)}" if self.values else None
        ]
        details_str = "\n".join(filter(None, details))  # Remove None values
        return f"{self.args[0]}\n{details_str}" if details_str else self.args[0]


