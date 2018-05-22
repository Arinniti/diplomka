#Editable criteria values -> depending on strategy

#score defining if strategy of project
IS_STRATEGIC_POINTS = 5
ISNT_STRATEGIC_POINTS = 1

#project complexity
COMPLEXITY_LOW_POINTS = 3
COMPLEXITY_HIGH_POINTS = 1

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
PROGRESS_LOW_POINTS = 1    # progress 0-34%


#score for CPI (Cost Performance Index) and score for SPI (Schedule Performance Index) Calculated with EVM
NOT_CPI_SPI_POINTS = 1    #value CPI < 1 and SPI > 1
NOT_CPI_NOT_SPI_POINTS = -1   #value CPI < 1 and SPI < 1
CPI_SPI_POINTS = 3    #value CPI > 1 and SPI > 1
CPI_NOT_SPI_POINTS = 2    #value CPI > 1 and SPI < 1



# Number of max point depends on score set on kriterias below
MAX_ATTRACTIVNESS = IS_STRATEGIC_POINTS+COMPLEXITY_LOW_POINTS+\
                     URG_IMP_POINTS+PROGRESS_HIGH_POINTS+CPI_SPI_POINTS

#score separating attractive project from unattractive for portfolio/organization
ATTRACTIVNESS_POINT = 8