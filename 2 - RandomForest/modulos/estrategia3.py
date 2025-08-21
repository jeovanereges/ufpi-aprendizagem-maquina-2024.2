# Módulo de tratamento de outliers


# Imports
import numpy as np
import pandas as pd


# Classe
class TrataOutlier:

    # Construtor
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def countOutliers(self, Q1, Q3, IQR, columns):
        cutOff = IQR * 1.5
        tempDf = (self.df[columns] < (Q1 - cutOff)) | (self.df[columns] > (Q3 + cutOff))
        return [len(tempDf[tempDf[col] == True]) for col in tempDf]

    def calcSkew(self, columns=None):
        if columns is None:
            columns = self.df.columns
        # return [(col, round(self.df[col].skew(), 2)) for col in columns]
        return [round(self.df[col].skew(), 2) for col in columns]


    def percentage(self, values):
        return [str(round(((value / self.df.shape[0]) * 100), 2)) + '%' for value in values]

    def removeOutliers(self, columns):
        for col in columns:
            Q1, Q3 = self.df[col].quantile(0.25), self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            cutOff = IQR * 1.5
            lower, upper = Q1 - cutOff, Q3 + cutOff
            self.df = self.df.drop(self.df[self.df[col] > upper].index)
            self.df = self.df.drop(self.df[self.df[col] < lower].index)


    def replaceOutliersWithFences(self, columns):
        for col in columns:
            Q1, Q3 = self.df[col].quantile(0.25), self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            cutOff = IQR * 1.5
            lower, upper = Q1 - cutOff, Q3 + cutOff

            self.df[col] = np.where(self.df[col] > upper, upper, self.df[col])
            self.df[col] = np.where(self.df[col] < lower, lower, self.df[col])


    def getOverview(self, columns) -> None:
        minValues = self.df[columns].min()
        Q1 = self.df[columns].quantile(0.25)
        medianValues = self.df[columns].quantile(0.5)
        Q3 = self.df[columns].quantile(0.75)
        maxValues = self.df[columns].max()
        IQR = Q3 - Q1
        skewValues = self.calcSkew(columns)
        outliers = self.countOutliers(Q1, Q3, IQR, columns)
        cutOff = IQR * 1.5
        lower, upper = Q1 - cutOff, Q3 + cutOff

        newColumns = ['Coluna', 'Min', 'Q1', 'Median', 'Q3', 'Max', 'IQR', 'Lower fence', 'Upper fence', 'Skew', 'NumOutliers', 'PercentOutliers']

        data = zip(
            [column for column in self.df[columns]],
            minValues, Q1, medianValues, Q3, maxValues, IQR, lower, upper, skewValues, outliers, self.percentage(outliers)
        )

        newDf = pd.DataFrame(data=data, columns=newColumns)

        newDf.set_index('Coluna', inplace=True)

        return newDf.sort_values('NumOutliers', ascending=False).transpose()



