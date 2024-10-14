import requests
from bs4 import BeautifulSoup
import re
import math
import pandas as pd
import numpy as np

def get_stat_categories(soup):
    categories_html = soup.find_all("th")
    categories = []
    for i in range(len(categories_html)):
        if i == 0:
            categories.append("Player Name")
        else:
            categories.append(categories_html[i].get("title"))
    return categories

# returns the 2-3 primary agents/heroes used by a player
def get_agents(soup):
    agent_list = []
    agent_links = soup.find("div").find_all("img")
    for agents in agent_links:
        src = agents.get("src")
        agent_name = src[21: -4]
        agent_list.append(agent_name.capitalize())
    return agent_list

# breaks a vlr.gg event page into components, including:
# html of full stat table
# a list of html elements corresponding to each player in the event,
# a list of stat categories
# a list of players participating in the event
# a 2D array representation of the table 

class Event:
    def __init__(self, event_id):
        self.id_number = event_id
        self.url = "https://www.vlr.gg/stats/?event_group_id={}&event_id=all&region=all&country=all&min_rounds=200&min_rating=1550&agent=all&map_id=all&timespan=all".format(event_id)
        response = requests.get(self.url)
        self.soup = BeautifulSoup(response.content, "html.parser")
        self.full_table = self.soup.find("table", class_="wf-table mod-stats mod-scroll")
        self.player_info_html = []
        self.get_player_info_html()
        self.player_tracker = self.get_player_list()
        self.stat_table = self.get_event_stats()
        self.stat_categories = get_stat_categories(self.full_table)
        
    def get_player_info_html(self):
        for child in self.full_table.find("tbody").children:
            tr = []
            for td in child:
                if td == "\n":
                    continue
                else:
                    tr.append(td)
            if tr != []:
                self.player_info_html.append(tr)

    def get_player_list(self):
        player_list = []
        for players in self.player_info_html:
            link = players[0].find("a").get("href")
            player_list.append((link.split("/")[-1]))
        return player_list

# reads html corresponding to each player + appends a row containing player's information to 2D array
    def get_event_stats(self): 
        all_stats = []
        for j in self.player_info_html:
            row = []
            for i in j:
                try:
                    if "mod-player" == i.get("class")[0]:
                        stat = i.find("a").find("div").find("div").get_text()
                    elif "mod-agents" == i.get("class")[0]:
                        stat = ", ".join(get_agents(i))
                    else:
                        stat = i.get_text().strip()
                except(TypeError):
                    stat = i.get_text().strip()
                row.append(stat)
            all_stats.append(row)
        return all_stats


event1 = Event(45)
headers = event1.stat_categories[0:]
all_stats = event1.stat_table

# convert 2D array to a pandas dataframe and csv
mydata = pd.DataFrame( np.array(all_stats), columns = headers)
mydata.to_csv("val.csv")


# defines a player class to be used in future implementation of data analysis
# next steps could include training a win prediction model, player/team ELO rating system
"""
class Player:
    def __init__(self, n, id=False):
        try:
            self.name = n
            self.player_stats = []
            self.has_event = id
            if type(id) == int:
                self.event = Event(id)
                self.player_info_index = self.event.player_tracker.index((self.name).lower())
                self.player_profile = self.event.stat_table[self.player_info_index]
        except(ValueError):
            print("This player is not in the database for this event!")

    def __repr__(self):
        str = ""
        for i in range(len(self.event.stat_categories)):
            str += self.event.stat_categories[i] + ": " + self.player_profile[i] + "\n"
        return str

"""











    











    







    










        
    
        
            
        





        








    
        







