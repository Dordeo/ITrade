class user_profile:
    #user id
    id: str;

    #if we are searching for highest performance
    performance: bool;

    #for year of establishment parameter
    establishment_year: int;

    #for ESG Parameters search active
    environment: bool;
    social: bool;
    governance: bool;

    def __init__(self):
        self.id = "000"
        self.performance = False;
        self.establishment_year = 9999;
        self.social = False;
        self.environment = False;
        self.governance = False ;

    def __init__(self, id="000", performance=False, establishment_year=9999,
                 social=False, environment=False, governance=False):
        self.id = id[0:2]

        self.performance = performance

        self.establishment_year = int(establishment_year);

        self.social = social
        self.environment = environment
        self.governance = governance

