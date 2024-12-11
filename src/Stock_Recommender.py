import pandas as pd
from User_Profile import user_profile

from pandas.core.interchange import dataframe


class stock_recommender:
    path: str;
    df: dataframe;
    tdf: dataframe;
    perentile: dataframe;

    def __init__(self):
        self.path = "";
        self.df = None;
        self.tdf = None;

    def __init__(self, relative_path):
        self.path = relative_path;

        self.df = pd.read_csv(self.path);
        self.df = self.df.sort_values(by = "Performance", ascending=False);
        self.tdf = None;


    def sort_by_ESG(self, df: dataframe, user) -> dataframe:
        df["CompoundScore"] = (df["Environment"] if user.environment else 0 +
                               df["Social"] if user.social else 0 +
                               df["Governance"] if user.governance else 0);

        df = df.sort_values(by="CompoundScore", ascending=False);

        df = df.drop(columns=["CompoundScore"]);

        return df;

    def get_unique(self, df: dataframe, n) -> dataframe:

        if n > len(df):
            return df;

        #TODO clean up this code
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

    def is_top_percentile(self, row):
        industry = row["Industry"]
        performance = row["Performance"]

        return performance >= self.percentile[industry]
    def get_top_percentile(self, df: dataframe, n, quan):
        grouped = df.groupby("Industry"); # I group them by industry

        self.percentile = grouped["Performance"].quantile(quan)

        df["TopPercentile"] = df.apply(self.is_top_percentile, axis = 1);

        res = df[df["TopPercentile"]]

        if len(res) < n or quan <= 0:
            return self.get_top_percentile(df, df, n, quan-0.05);

        return res;




    def get_stocks(self, user: user_profile, n: int) -> dataframe:

        # according to my algorythm we are first going to exclude some stocks based on their establishment year
        # if the user did not select a specific year the user_profile is set to selecet year 9999 which is far above the
        # current year

        self.tdf = self.df[self.df["FoundationYear"] <= user.establishment_year];

        # now I should do transformations if I am looking at a specific top percentile of the industry
        if user.performance:
            self.tdf = self.get_top_percentile(self.tdf, n, 0.90)

        #here I filter the top percentile or the non transformed tdf based on the ESG criteria
        if (user.governance or user.social or user.environment):
            # this line of code does it
            self.tdf = self.sort_by_ESG(self.tdf, user);

        else:
            self.tdf = self.tdf.sort_values(by = "Performance", ascending = False);

        # now however I want to include all unique industries at least once as long as it is in confines
        # of number of stocks the user entered

        res = self.get_unique(self.tdf, n)
        res = res.sort_values(by = ["Industry", "Performance"], ascending=[False, False]);

        return res;









