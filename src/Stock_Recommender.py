import pandas as pd
from User_Profile import user_profile
from Stock import stock

from pandas.core.interchange import dataframe


class stock_recommender:
    path: str;
    df: dataframe;
    tdf: dataframe;
    stocks: list;

    def __init__(self):
        self.path = "";
        self.df = None;
        self.tdf = None;
        self.stocks = None;

    def __init__(self, relative_path):
        self.path = relative_path;

        self.df = pd.read_csv(path);
        self.df = self.df.sort_values(self.df["Performance"], ascending=false);
        self.stocks = None;
        self.tdf = None;

    def get_stocks(self, user: user_profile, n: int) -> str:

        # according to my algorythm we are first going to exclude some stocks based on their establishment year
        # if the user did not select a specific year the user_profile is set to selecet year 9999 which is far above the
        # current year

        self.tdf = self.df[self.df["FoundationYear"] <= user.establishment_year];

        # next I am going to sort based on the compound sum of social, environment and governance parameters if they are
        # set to be true as it is per my algorythm. To achieve this I am going to create a new column in the dataframe
        # that takes all parameters that are true and combines them into one. After it just selects N of those left
        # however I will only do so and only if at least one of ESG params is set true

        if (user.governance or user.social or user.environment):

            # this lines of code do the steps descrived earlier
            self.tdf["CompoundScore"] = (self.tdf["Environment"] if user.environment else 0
                                + self.tdf["Social"] if user.social else 0
                                + self.tdf["Governance"] if user.governance else 0);

            self.tdf = self.tdf.sort_values(self.tdf["CompoundScore"], ascending=False);

        # this one just selects the first n entries
        # one beauty of my code is that main dataframe is by default sorted for performance os if the
        # previous conditional statement is not excecuted we will just have n smaple of best performing stocks

        self.tdf = self.tdf.head(n);

        # however we still need to sort for performance if it is also a param of our search that is True
        if(user.performance):
            self.tdf = self.tdf.sort_values(self.tdf["Performance"], ascending=False);


        return f"{self.tdf}";









