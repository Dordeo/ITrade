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

        unique_industries = self.tdf["Industry"].unique();
        # unique_ industries is a numpy_array that contains all unique industries

        #this is going to be a list of dataframes containing solely a specific industry
        partition: list[dataframe] = []
        #this list is of integers that track the length of each df in partition
        lengths = [];
        takes = [];
        i = 0;


        for element in unique_industries:
            partition.append(
                self.tdf[self.tdf["Industry"].str.contains(element, case = False)]
            )

        for df in partition:
            lengths.append(len(df));
            takes.append(0);

        i = 0;
        # now we have sorted all those unique industries stocks so that the top contendors are on the top
        # however now we run into another problem, it is not guaranteed that all df in partition are of equal size
        # and we need to include all industries once unless it is out of bound of n.
        # so now I am going to do this. Create variable cycle_tracker -> tracks the main loop cycle
        # I am also going to have a sub loop which is going to parse through partition and select
        # each df in partition once per main loop cycle. in the sub loop, I am going to access an element in each df
        # under index of cycle_tracker. if it is accesible I am going to add that row into ...

        # Actually no. this will lead to multiple redundacies I would rather do formulas
        # Scrap that instead I am going to simplify it into a simple integer problem

        if n > len(self.tdf):
            print("There were not enough stocks, Please lower your requirments of number of stocks")
            return self.tdf;

        # here the problem begins lengths track the number of elements in each df.
        # takes indicate how much elements I take from each df

        # here it goes

        while i < n:

            for j in range(len(lengths)):
                if(i < n):

                    if (lengths[j] != 0):
                        lengths[j] -= 1;
                        takes[j] += 1;
                        i+=1;


        i = 0;
        res = pd.DataFrame();
        for df in partition:
            res = pd.concat([res, df.head(takes[i])], ignore_index=True);
            i+=1;

        res = res.sort_values(by = "Performance", ascending=False);

        return res;









