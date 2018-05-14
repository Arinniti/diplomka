#Editable criteria values -> depending on strategy


#score separating attractive project from unattractive for portfolio/organization
#project can get 1-25 points defining it attractiveness.
ATTRACTIVENESS_POINT = 8

#score defining if strategy of project
IS_STRATEGIC_POINTS = 5
ISNT_STRATEGIC_POINTS = 1

#risk appetite - sets a value (1-16). Above it, risk will be unacceptable
RISK_APPETITE = 11

#risk is acceptable
RISK_OK_POINTS = 3
RISK_NOT_OK_POINTS = 0

#project complexity
COMPLEXITY_LOW_POINTS = 2
COMPLEXITY_HIGH_POINTS = 0

#combination of urgency/importance of project.
URG_IMP_POINTS = 4   #urgent and important
NOT_URG_IMP_POINTS = 3     #not urgent, but important
URG_NOT_IMP_POINTS = 1     #urgent, but not important
NOT_URG_NOT_IMP_POINTS = 0     #neither urgent or important


#progress and CPI affect only ongoing and interrupted projects:

#define project progress limits (in %). Set lowest value for each
PROGRESS_HIGH = 65   # progress 65-99%
PROGRESS_MODERATE = 35    #progress 35-64%,

#score depending on project progress (in %)
PROGRESS_HIGH_POINTS = 4   # progress 65-99%
PROGRESS_MODERATE_POINTS = 3    #progress 35-64%
PROGRESS_LOW_POINTS = 0    # progress 0-34%



#define CPI limits. Set lowest value for each
# CPI = 1 means cost spend on project till one is exactly like planned.
# Higher than 1 means project costs less than planned. Opposite for CPI < 1
CPI_POSITIVE_HIGH = 3
CPI_POSITIVE = 1
CPI_NEGATIVE = -2

#score for CPI (Cost Performance Index). Calculated with EVM
CPI_POSITIVE_HIGH_POINTS = 4    #value CPI > 3
CPI_POSITIVE_POINTS = 3    #value 3 > CPI > 1
CPI_NEGATIVE_POINTS = 1    #value 1 > CPI > -2
CPI_NEGATIVE_HIGH_POINTS = 0   #value CPI < -2

