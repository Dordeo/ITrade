import pandas as pd
from User_Profile import user_profile
# I use tabulate for output as it is one of the best in my opinion for output in a console
from tabulate import tabulate
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

    # this function will sort based on Enviornmental, Social and Governance parameters separately
    def sort_by_ESG(self, df: dataframe, user) -> dataframe:
        # to do this I am going to create a new column with pandas df method, and assign it such values
        # equal to previously stated parameters, if their counterpart in the user_profile is active - True
        df["CompoundScore"] = (df["Environment"] if user.environment else 0 +
                               df["Social"] if user.social else 0 +
                               df["Governance"] if user.governance else 0);

        # Here I just sort based on these parameters and remove the column afterwards
        df = df.sort_values(by="CompoundScore", ascending=False);

        df = df.drop(columns=["CompoundScore"]);

        return df;

    #this function ensures equal inclusion to the maximum for each industry for the output
    def get_unique(self, df: dataframe, n) -> dataframe:
        # There is no need to go trhough this function if the length of the dataframe is less or equal to n
        if n >= len(df):
            return df;

        # unique_ industries is a numpy_array that contains all unique industries
        unique_industries = df["Industry"].unique();

        # this is going to be a list of dataframes containing solely a specific industry
        partition: list[dataframe] = []

        # this list 'lengths' is of integers that track the length of each df in partition
        lengths = [];
        #this list will track how much elements we take from each df in partition
        takes = [];
        #i is just an index
        i = 0;

        # here I make it so partition has all instances fully filled for each industry
        # what it is in result and array of dataframes where each dataframe has only one type of industry
        for element in unique_industries:
            partition.append(
                df[df["Industry"].str.contains(element, case=False)]
            )

        # in this loop I initialize all elements in lengths and take
        for dfa in partition:
            lengths.append(len(dfa));
            takes.append(0);

        #while i is less than n
        while i < n:

            # I go through each element in length
            # and if it is not 0 I transfer 1 from lengths to takes
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

    # function that I am going to pass onto pandas df apply method wich basically goes through each row
    # in the dataframe and applies a function to that row, in this case it is going to check if that row
    # is within the looked for percentile and returns True if it is within the precentile or false if not
    def is_top_percentile(self, row):
        industry = row["Industry"]
        performance = row["Performance"]

        return performance >= self.percentile[industry]

    # this is a recursive function that dynamically adjust its needed percentile for each industry
    def get_top_percentile(self, df: dataframe, n, quan):
        grouped = df.groupby("Industry"); # I group them by industry

        # and from each grouped variant, I get something call quantile, which is a method in pandas dataframe
        # that returns a float representing a percentile we gave to quantile method, for each unique instances
        # in a dataframe, which is in this case each indsutry
        self.percentile = grouped["Performance"].quantile(quan)

        # now I just apply a function from above, and store the boolean value in a column TopPercentile
        # I use lamda row to avoid a specific copy warning during the slicing proccess when panda uses apply method
        # took a while to find out I should do this as .apply method is not really that safe
        df["TopPercentile"] = df.apply(lambda row: self.is_top_percentile, axis = 1);

        #res is just a list right now that stores only a row with TopPercentile column set to True,
        # I use it to count the amount of True values in the column to see
        # if I have enough stocks to fulfill users request
        res = df[df["TopPercentile"]]

        # here if the result does not have enough numbers I lower the percentile parameter by a margin of 0.05 and call
        # the function again, with an updated parameter
        if len(res) < n or quan <= 0:
            return self.get_top_percentile(df, n, quan-0.05);

        # however If the dataframe has enough stocks it will just return
        res = res.drop(columns = ["TopPercentile"])
        return res;

    # this function is a recursive function that ensures only stocks before certain year will be included
    # if there are not enough stocks, the year parameter will be adjusted to fit in at least N number of stocks
    def sort_year(self, df: dataframe, n: int, year: int):
        res = df[df["FoundationYear"] <= year];

        if len(res) < n:
            # incrementing the year by a decade as an increasing margin
            return sort_year(df, n, year + 10);

        # otherwise I am just going to preint a message that will print out a year and return res
        print(f"Including stocks from year up to {year} to fit user parameters");
        return res;


    def get_stocks(self, user: user_profile, n: int) -> dataframe:

        # according to my algorythm we are first going to exclude some stocks based on their establishment year
        # if the user did not select a specific year the user_profile is set to select year 9999 which is far above the
        # current year

        self.tdf = self.sort_year(self.df, n, user.establishment_year);

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

        # and now I just sort the table to show all indsutries close to each other for easy comparison
        res = res.sort_values(by = ["Industry", "Performance"], ascending=[False, False]);

        return res;









