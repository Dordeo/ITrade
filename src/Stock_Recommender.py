import pandas as pd
from User_Profile import user_profile

from pandas.core.interchange import dataframe


class stock_recommender:
    path: str;
    df: dataframe;
    tdf: dataframe;

    def __init__(self):
        self.path = "";
        self.df = None;
        self.tdf = None;

    def __init__(self, relative_path):
        self.path = relative_path;

        self.df = pd.read_csv(self.path);
        self.df = self.df.sort_values(by = "Performance", ascending=False);
        self.tdf = None;


    def sort_by_ESG(self, df, user) -> dataframe:
        df["CompoundScore"] = (df["Environment"] if user.environment else 0 +
                               df["Social"] if user.social else 0 +
                               df["Governance"] if user.governance else 0);

        df = df.sort_values(by="CompoundScore", ascending=False);

        df = df.drop(columns=["CompoundScore"]);

        return df;

    def get_unique(self, df, n) -> dataframe:

        if n > len(df):
            return df;

        unique_industries = df["Industry"].unique();
        # unique_ industries is a numpy_array that contains all unique industries

        # this is going to be a list of dataframes containing solely a specific industry
        partition: list[dataframe] = []

        # this list is of integers that track the length of each df in partition
        lengths = [];
        #this list will track how much elements we take from each df in partition
        takes = [];
        #i is just an index
        i = 0;

        for element in unique_industries:
            partition.append(
                df[df["Industry"].str.contains(element, case=False)]
            )

        for dfa in partition:
            lengths.append(len(dfa));
            takes.append(0);

        #while i is less than n
        while i < n:

            # I go through each element in length
            # and if it is not 0 i transfer 1 from lengths to takes
            for j in range(len(lengths)):
                if (i < n):

                    if (lengths[j] != 0):
                        lengths[j] -= 1;
                        takes[j] += 1;
                        i += 1;


        i = 0;
        res = pd.DataFrame();

        # now I go thorugh each df in partition and add respective amount of elements determined in takes[i] to
        # res dataframe

        for dfa in partition:
            res = pd.concat([res, dfa.head(takes[i])], ignore_index=True);
            i += 1;

        return res

    def get_stocks(self, user: user_profile, n: int) -> dataframe:

        # according to my algorythm we are first going to exclude some stocks based on their establishment year
        # if the user did not select a specific year the user_profile is set to selecet year 9999 which is far above the
        # current year

        self.tdf = self.df[self.df["FoundationYear"] <= user.establishment_year];

        # This is a function that will select entries only from certain industry if user did not want to select
        # any industry user_profile automatically sets industry to "" which in turn makes str.contains() useless

        self.tdf = self.tdf[self.tdf["Industry"].str.contains(user.industry, case = False)];

        # next I am going to sort based on the compound sum of social, environment and governance parameters if they are
        # set to be true as it is per my algorythm. To achieve this I am going to create a new column in the dataframe
        # that takes all parameters that are true and combines them into one. After it just selects N of those left
        # however I will only do so and only if at least one of ESG params is set true

        if (user.governance or user.social or user.environment):

            # this line of code does the steps descrived earlier
            self.tdf = self.sort_by_ESG(self.tdf, user);
        else:
            self.tdf = self.tdf.sort_values(by="Performance", ascending=False);

        # this one just selects the first n entries
        # one beauty of my code is that main dataframe is by default sorted for performance os if the
        # previous conditional statement is not excecuted we will just have n smaple of best performing stocks

        # if the user has previously selected a specific industry if is useless to conitue forward so I am just going
        # return current tdf as the code next will only work for a case if the user did not select an industry
        if user.industry != "":
            self.tdf = self.tdf.head(n);
            self.tdf = self.tdf.sort_values(by="Performance", ascending=False);
            return self.tdf;

        # now however I want to include all unique industries at least once as long as it is in confines
        # of number of stocks the user entered


        res = res.sort_values(by = "Performance", ascending=False);

        return res;









