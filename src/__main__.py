from Stock_Recommender import *
from tabulate import tabulate

# just a regular function to call during times when console user input is needed
# for filtered search, return user_profile obj
def user_input()->user_profile:

    user = user_profile();

    a: str = input("Would you like to prioritize performance of the establishments? -> Yes or No\n");

    if "yes" in a.lower():
        user.performance = True;

    a = input("Would you like to search for establishments created before a certain year? Yes or No\n");

    if "yes" in a.lower():
        a = input("Type a year -> ");
        try:
            user.establishment_year = int(a);
        except:
            user.establishment_year = 9999;

    a = input("Would you like to search for establishments created of a certain industry? Yes or No\n");

    if "yes" in a.lower():
        a = input("Type an industry -> ");
        user.industry = a;

    a = input("Would you like to search for establishments with high enviornment score? Yes or No\n");

    if "yes" in a.lower():
        user.environment = True;

    a = input("Would you like to search for establishments with high social score? Yes or No\n");

    if "yes" in a.lower():
        user.social = True;

    a = input("Would you like to search for establishment with high governance score? Yes or No\n");

    if "yes" in a.lower():
        user.governance = True;

    return user;

def main():
    path = "../rescs/stocks.csv";

    user = user_input();

    n = 15;

    try:
        n = int(input("Please enter the amount of stocks you want to us to recommend -> "));
    except:
        n = 15;

    recommender = stock_recommender(path);

    df = recommender.get_stocks(user, n)

    table = tabulate(df, headers = "keys", tablefmt = "grid", showindex=False);

    print(table)

if __name__ == "__main__":
    main();

