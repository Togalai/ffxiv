import pandas as pd
import requests
import time

####                                                            ####
####    Creation Date: 05/20/2021                               ####
####    Author: Togalai                                         ####
####    Purpose: Attempting to give officers of the FC          ####
####    an easier method to track members progress so events    ####
####    are easier to schedule and run.                         ####
####                                                            ####     


# Starting a timer to tell me how long the script takes to run
start = time.time()
# Pulling list of free company members from the XIV API
d = requests.get('https://xivapi.com/freecompany/9233645873504835968?data=FCM')

# Establishing a blank dictionary that will eventually become the output table
m_achieve = {"Name":[],"Rank":[],"AchievePublic":[],"LatestCompleted":[]}
# Converting the raw pull from the API to json format for easier use
item = d.json()
# Pulling the list of members from the json 
members = item['FreeCompanyMembers']
# establishing a blank list for FC member IDs
mem_ids = []

# Loops over all the members in the FC and adds their lodestone ID's to the blank list established earlier
for n in range(len(members)):
    mem_ids.append(members[n]['ID']) 

# Function to loop over that takes an individual lodestone ID and checks their achievement info
def mem_progression(ID):
    try:
        # Pulls the specific member given their lodestone ID
        mem = requests.get('https://xivapi.com/character/{}?data=AC'.format(ID))
        # Converts their info into json format
        member = mem.json()
        # establishes a list for the member's achievements (starts with a 0 so we never have a blank list)
        prog_list = [0]
        # Adds the FC member's Achievement status. This is set to False by default on Lodestone, denying access to look at achievements. 
        m_achieve["AchievePublic"].append(member['AchievementsPublic'])
    except Exception as e:
        print(e)
        pass
    try:
        # Checking their achievement status, if access is allowed then pulling their achievement list.
        if member['AchievementsPublic'] == True:
            print(member['Character']['Name']+ ' True')
            mem_ach = member['Achievements']['List']
            # Iterates through the achievement list looking for the specific IDs of the achievements that note the end of major MSQ milestones.
            for n in range(len(mem_ach)):
                if mem_ach[n]['ID'] in [788,1129,1139,1691,1794,2233,2298,2850]:
                    prog_list.append(mem_ach[n]['ID']) # If the achievement milestones exist in the FC member's achievement list it appends all that are available to this list.
        # Checking their achievement status, if not allowed simply noting so and moving to the next FC user
        elif member['AchievementsPublic'] == False:
            print(member['Character']['Name']+ ' False')
            m_achieve["LatestCompleted"].append('Not Available')
    except Exception as e:
        print(e)
        pass
    try:
        # Looks for the latest MSQ achievement and sets the "LatestCompleted" equal to that completed achievement
        if max(prog_list) == 2850 and member['AchievementsPublic'] == True:
            m_achieve["LatestCompleted"].append('Finished Post-Shadowbringers (5.5)')
        elif max(prog_list) == 2298 and member['AchievementsPublic'] == True:
            m_achieve["LatestCompleted"].append('Finished Shadowbringers (5.0)')
        elif max(prog_list) == 2233 and member['AchievementsPublic'] == True:
            m_achieve["LatestCompleted"].append('Finished Legend Returns (4.56)')                
        elif max(prog_list) == 1794 and member['AchievementsPublic'] == True:
            m_achieve["LatestCompleted"].append('Finished Stormblood (4.0)')
        elif max(prog_list) == 1691 and member['AchievementsPublic'] == True:
            m_achieve["LatestCompleted"].append('Finished Dragonsong War(3.56)')
        elif max(prog_list) == 1139 and member['AchievementsPublic'] == True:
            m_achieve["LatestCompleted"].append('FInished Heavansward (3.0)')
        elif max(prog_list) == 1129 and member['AchievementsPublic'] == True:
            m_achieve["LatestCompleted"].append('Finished Seventh Umbral Era (2.55)')
        elif max(prog_list) == 788 and member['AchievementsPublic'] == True:
            m_achieve["LatestCompleted"].append('Finished ARR (2.0)')
        # If the FC member's achievements are public but there are no MSQ achievements the assumption is that they are not finished with A Realm Reborn
        elif max(prog_list) == 0 and member['AchievementsPublic'] == True:
            m_achieve["LatestCompleted"].append('Pre-ARR')
    except Exception as e:
        print(e)
        pass

# Iterates through the FC members and adds all their Names and Ranks to the output table
for n in range(len(members)):
    m_achieve['Name'].append(members[n]['Name']) 
    m_achieve['Rank'].append(members[n]['Rank']) 

# Iterates through the FC members and inputs each FC member's lodestone ID into the function above to get their achievement information
for m in mem_ids:
    mem_progression(m)
try:
    # Converts final full dictionary into a Dataframe and outputs dataframe to a csv file.
    df = pd.DataFrame.from_dict(m_achieve)
    df.to_csv(r'C:\Users\Sam\Documents\Python Scripts\FC_Prog.csv')
except Exception as e:
    print(e)

# Notes the end time of the script
end = time.time()
# Subtracts end time from start time to give total seconds elapsed
tot_time = round((end-start),2)
# Converts seconds into minutes and outputs the total time elapsed 
print(str(tot_time/60) + ' minutes elapsed')

print(df)
print(len(m_achieve["Name"]))
print(len(m_achieve["Rank"]))
print(len(m_achieve["AchievePublic"]))
print(len(m_achieve["LatestCompleted"]))
