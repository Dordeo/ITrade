class stock:
    #stock ID
    id: str;

    #how good the stocks is based on the prior evaluation
    performance: float;

    #stocks industry
    industry: str;

    #stocks foundation year
    foundation_year: int;

    ## Types of rating the stocks get
    environment: float;
    social: float;
    governance: float;

    def __init__(self):
        self.id = "000"
        self.performance = 0;
        self.foundation_year = 0;
        self.industry = "";
        self.social = 0;
        self.environment = 0;
        self.governance = 0;

    def __init__(self, id="000", performance=0, foundation_year=0, industry="", social=0, environment=0, governance=0):
        self.id = id[0:2]
        self.performance = float(performance)
        self.foundation_year = int(foundation_year)
        self.industry = industry
        self.social = float(social)
        self.environment = float(environment)
        self.governance = float(governance)

    def __str__(self):
        return f"""{self.id} | {self.industry} | {self.performance} | {self.foundation_year} |"""

    def __setattr__(self, __name, __value):
        super().__setattr__(__name, __value)
