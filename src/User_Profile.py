## User profile is a custom class used for containing the information about the user and their prefered choices
# during the search or user input proccesses

class user_profile:
    #user id
    id: str;

    #if we are searching for highest performance
    performance: bool;

    #if we are also searchign for specific industry
    industry: str;

    #for year of establishment parameter
    establishment_year: int;

    #for ESG Parameters search when active
    environment: bool;
    social: bool;
    governance: bool;

    def __init__(self):
        self.id = "000"
        self.performance = False;
        self.industry = ""
        self.establishment_year = 9999;
        self.social = False;
        self.environment = False;
        self.governance = False ;

    def __init__(self, id="000", performance=False, establishment_year=9999,
                 social=False, environment=False, governance=False, industry = ""):
        self.id = id[0:2]

        self.performance = performance
        self.industry = industry;

        self.establishment_year = int(establishment_year);
        self.social = social
        self.environment = environment
        self.governance = governance

    def __setattr__(self, __name, __value):
        super().__setattr__(__name, __value)

