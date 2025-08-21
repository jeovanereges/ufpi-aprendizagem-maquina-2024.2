# Módulo de conversão de tipos de dados


# Imports
import numpy as np
import pandas as pd


def convertToString(df, columns):
    for col in columns:
        df[col] = df[col].astype("string")


def convertToInt(df, columns):
    for col in columns:
        df[col] = df[col].astype("int64")


def convertToDatetime(df, columns):
    for col in columns:
        df[col] = pd.to_datetime(df[col])


def multiplyByFactor(df, columns, factor):
    for col in columns:
        df[col] = df[col] * factor
    return df[col]

