import logging as log
from turtledemo.chaos import line

import pandas as pd
import numpy as np
import os

log.basicConfig(level=log.INFO, format="%(levelname)s %(asctime)s %(filename)s %(message)s")

class Cleaner:


    def __init__(self, filename):
        self.file_uncleaned_path =  f"{os.getenv("UPLOAD_PATH")}/{filename}"
        log.info(f"File-path: {self.file_uncleaned_path}")
        log.info(f"File-name: {filename}")

        self.df = pd.read_csv(self.file_uncleaned_path)
        self.sensitive_data = ["email", "phone"]


    def originate_column_type(self):
        for col in self.df.columns:
            length_col  = self.df[col].count()
            if pd.api.types.is_string_dtype(self.df[col]) and col not in self.sensitive_data:
                try:
                    converted  = pd.to_numeric(self.df[col].copy(), "coerce")
                    if converted.notna().sum() >= length_col / 2:
                        self.df[col] = converted

                except ValueError as e:
                    log.error(e)



    def clean_string(self):
            self.df.columns = self.df.columns.str.strip()
            self.df = self.df.apply(lambda col : col.str.strip() if col.dtype in ["str", "object"] else col)
            self.df = self.df.apply(lambda col: col.str.lower() if col.dtype in ["str", "object"] and col.name not in self.sensitive_data else col)

            for col in self.df.columns:
                if pd.api.types.is_string_dtype(self.df[col]):
                    self.df[col] = self.df[col].str.replace(r'[^\x00-\x7F]+','', regex=True)
                    self.df[col] = self.df[col].replace(["N/A", "null", "none"], "")
                    self.df.replace(r"^\s*$",np.nan, regex=True, inplace=True)


    def clean_date_column(self):
        for col in self.df.columns:
            if pd.api.types.is_string_dtype(self.df[col]):
                try:
                    converted = pd.to_datetime(self.df[col], format="mixed" , errors="coerce")
                    column_length = converted.notna().sum()
                    if column_length >= len(self.df[col]) /2:

                        self.df[col] = converted
                except Exception as e:
                    log.info(e)


    def csv_summary(self):
        summary = f"""
            Shape: {self.df.shape[0]},
            rows: {self.df.shape[1]}
            columns and type: {self.df.dtypes.to_string()},
            Missing values: {self.df.isnull().sum().to_string()}
            Sample Data: {self.df.head().to_string()}
            Statical summary: {self.df.describe()}
        """
        return summary


def start(filename):
    c = Cleaner(filename)
    print(c.df.to_string())
    log.info("File is uploaded, The process of cleaning has started")
    c.originate_column_type()
    c.clean_string()
    c.clean_date_column()
    file_clean_path = f"{os.getenv("CLEANED_PATH")}/{filename}"
    print("\t")
    print(c.df.to_string())
    c.df.to_csv(file_clean_path, index=False)
    summary  = c.csv_summary()
    return summary
