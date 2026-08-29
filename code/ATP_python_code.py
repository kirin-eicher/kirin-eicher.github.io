# Code for: ATP Tournament Winners Project

# Import the necessary packages for analysis

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import the data

set: pd.DataFrame = pd.read_csv("player_data.csv")

#Data cleaning and merging

# Drop redundant and useless columns: 'first_name', 'last_name', 'player_url' , 'residence', 'birthplace', 'birthdate', 'birth_year',
# 'birth_month', 'birth_day', 'height_ft'

set_no_useless: pd.DataFrame = set.drop(['first_name', 'last_name', 'player_url' , 'residence', 'birthplace', 'birthdate',
                                                                'birth_year','birth_month','birth_day','height_ft'],axis=1)

#Drop players for which there is missing data

set_no_missing_no_useless: pd.DataFrame = set_no_useless.dropna(how='any')

#Fix indexing to start from 0
set_no_missing_no_useless.sort_index(axis=0, ascending=True)

index = range(len(set_no_missing_no_useless))
set_final = set_no_missing_no_useless.reset_index(drop=True)

# drop players who have zero values for numerical columns

mask = (set_final["turned_pro"] != 0) & (set_final["weight_lbs"] != 0) & (set_final["weight_kg"] != 0) & (set_final["height_inches"] != 0) & (set_final["height_cm"] != 0)

unwanted_rows = set_final[~mask]

set_final = set_final.drop(unwanted_rows.index)


set_final = set_final.reset_index(drop = True)

# preview
set_final.head()

# Getting tourney count totals from each player
# Import tournament data

tourney: pd.DataFrame = pd.read_csv("tournament_data.csv")

# tourney.head()

# tourney.columns

#Drop unnecessary vars: 'tourney_order', 'tourney_location', 'tourney_dates', 'tourney_month', 'tourney_day', 'tourney_fin_commit', 'tourney_url_suffix', 'singles_winner_url', 'weight_lbs', 'weight_kg', 'height_ft', 'height_inches', 'height_cm', 'handedness', 'backhand'
tourney_edit: pd.DataFrame = tourney.drop(['tourney_order', 'tourney_location', 'tourney_dates', 'tourney_month', 'tourney_day', 
                                           'tourney_fin_commit', 'tourney_url_suffix', 'singles_winner_url', 'weight_lbs', 'weight_kg', 
                                           'height_ft', 'height_inches', 'height_cm', 'handedness', 'backhand'], axis = 1)

#Create function to generate title count totals for each player

def title_ct(set_player: pd.DataFrame, set_tourney: pd.DataFrame) -> np.ndarray:
    title_list: np.ndarray = np.zeros(len(set_player))
    for i in range(len(set_player)):
        store: int = 0
        for j in range(len(set_tourney)):
            if set_player.iloc[i,0] == set_tourney.iloc[j,8]:
                store = store + 1
        title_list[i] = store
    return title_list


# Preview (uncomment)
# print(title_ct(set_final, tourney_edit))

# new_column: pd.DataFrame = pd.DataFrame(title_ct(set_final, tourney_edit), columns = ["Title Count"])

# set_merged = pd.concat([set_final,new_column], axis = 1)

# set_merged.head()
                
# Merge in data on player height, weight, handedness, backhand, and when they turned pro

tourney_edit = tourney_edit.rename(columns = {"singles_winner_player_id" : "player_id"})

tourney_final = pd.merge(tourney_edit,set_final,
                        on = 'player_id',
                        how = 'inner',
                        suffixes = ('','_drop'))


tourney_final = tourney_final.sort_values(by = "singles_winner_name")

tourney_final = tourney_final.drop(['flag_code','singles_winner_player_slug','singles_winner_name'] ,axis = 1)

tourney_final = tourney_final[['tourney_year','tourney_name', 'tourney_id', 
       'tourney_singles_draw', 'tourney_conditions', 'tourney_surface', 
       'player_slug', 'player_id', 'player_nationality','player_title_count', 
       'turned_pro', 'weight_lbs', 'weight_kg', 'height_inches', 'height_cm', 
       'handedness', 'backhand']]

tourney_final.head()

# Table of descriptive stats for players in dataset

set_final.describe()

# Descriptive statistics of the players in the dataset
# Using set_final so that every player is counted only once

# Player height

plt.figure(num = "Player Heights")

player_height_hist = pd.DataFrame(
    {"Height (in)" : set_final.iloc[:,6]}
)

player_height_hist.hist(bins = 15, grid = False)

# Player weight

plt.figure(num = "Player Weights")

player_weight_hist = pd.DataFrame(
    {"Weight (lbs)" : set_final.iloc[:,4]}
)

player_weight_hist.hist(bins = 15, grid = False)

# Player handedness

count_righthand = len(set_final[set_final["handedness"] == "Right-Handed"])

count_lefthand = len(set_final[set_final["handedness"] == "Left-Handed"])

player_handedness = pd.DataFrame(
    {
        "Handedness": np.array([count_righthand, count_lefthand])
    }
)

player_handedness.plot.pie(
    y = "Handedness",
    labels = ["Right-Handed", "Left-Handed"],
    colors = ["dodgerblue", "yellow"],
    figsize = ([6,6]),
    autopct = "%.2f",
    title = "Player handedness"
    )

# Player backahnd style

count_onehand = len(set_final[set_final["backhand"] == "One-Handed Backhand"])

count_twohand = len(set_final[set_final["backhand"] == "Two-Handed Backhand"])

player_backhand = pd.DataFrame(
    {
        "Backhand": np.array([count_twohand, count_onehand])
    }
)

player_backhand.plot.pie(
    y = "Backhand",
    labels = ["Two-Handed", "One-Handed"],
    colors = ["dodgerblue", "yellow"],
    figsize = ([6,6]),
    autopct = "%.2f",
    title = "Player backhand style"
    )

# Descriptive stats for tourneys
# Tourney_final has one entry for each time a tournament is held. Not every tournament is held every year in the data set

# Tourneys by surface

plt.figure(num = "Surfaces")

count_hard = len(tourney_final[tourney_final["tourney_surface"] == "Hard"])

count_clay = len(tourney_final[tourney_final["tourney_surface"] == "Clay"])

count_grass = len(tourney_final[tourney_final["tourney_surface"] == "Grass"])

count_carpet = len(tourney_final[tourney_final["tourney_surface"] == "Carpet"])

surface_table = pd.DataFrame(
    {
        "Surface (%)" : np.array([count_hard, count_clay, count_grass, count_carpet])
    }
)

surface_table.plot.pie(
    y = "Surface (%)",
    labels = ["Hard", "Clay", "Grass", "Carpet"],
    colors = ["dodgerblue", "chocolate", "yellowgreen", "darkred"],
    figsize = ([6,6]),
    autopct="%.1f",
    title = "Court surfaces for tournaments"
)

# Tourneys by conditions

plt.figure(num = "Conditions")

count_indoor = len(tourney_final[tourney_final["tourney_conditions"] == "Indoor"])

count_outdoor = len(tourney_final[tourney_final["tourney_conditions"] == "Outdoor"])

conditions_table = pd.DataFrame(
    {
        "Conditions (%)" : np.array([count_indoor, count_outdoor])
    }
)

conditions_table.plot.pie(
    y = "Conditions (%)",
    labels = ["Indoor", "Outdoor"],
    colors = ["darkslategray", "skyblue"],
    figsize = ([6,6]),
    autopct="%.1f",
    title = "Conditions (indoor vs outdoor) for tournaments"
)

# ADDITIONAL: Change in proportion of tournaments on four surfaces over time

# DataFrame with surface as columns, years as rows

def ann_surface_breakdown(table: pd.DataFrame) -> pd.DataFrame:
    store_proto: np.ndarray = np.zeros(shape=(len(range(1972,2018,1)),4))
    store: pd.DataFrame = pd.DataFrame(store_proto)
    index: int = 0
    for i in range(1972,2018,1):
        hard_tally : int = 0
        clay_tally : int = 0
        grass_tally : int = 0
        carpet_tally : int = 0
        for j in range(len(table)):
            if table.iloc[j,0] == i and table.iloc[j,5] == "Hard":
                hard_tally = hard_tally + 1
            elif table.iloc[j,0] == i and table.iloc[j,5] == "Clay":
                clay_tally = clay_tally + 1
            elif table.iloc[j,0] == i and table.iloc[j,5] == "Grass":
                grass_tally = grass_tally + 1
            elif table.iloc[j,0] == i and table.iloc[j,5] == "Carpet":
                carpet_tally = carpet_tally + 1
        store.iloc[index,0] = hard_tally
        store.iloc[index,1] = clay_tally
        store.iloc[index,2] = grass_tally
        store.iloc[index,3] = carpet_tally
        index = index + 1
    return store

ann_surface_table = pd.DataFrame(ann_surface_breakdown(tourney_final))

ann_surface_table.rename(columns=
    {
        0: "Hard",
        1: "Clay",
        2: "Grass",
        3: "Carpet",
    },
    inplace = True
)

# Add in a column for the year

ann_surface_table_final = pd.DataFrame(
    {
        "Year" : np.array(range(1972,2018,1)),
        "Hard" : np.array(ann_surface_table.iloc[:,0]),
        "Clay" : np.array(ann_surface_table.iloc[:,1]),
        "Grass" : np.array(ann_surface_table.iloc[:,2]),
        "Carpet" : np.array(ann_surface_table.iloc[:,3]),
    }
)

ann_surface_table_final.head()

# Stacked bar chart of surface type by year

ann_surface_table_final.plot.bar(stacked=True,
                             x = "Year",
                             figsize = ([10,6])
                             )

# Intersection of surface and conditions

def surface_and_condition(set : pd.DataFrame):
    surface_list = ["Hard", "Clay", "Grass", "Carpet"]
    conditions_list = ["Indoor", "Outdoor"]
    column_index = 0
    table = pd.DataFrame(
        {
            "Indoor" : np.zeros(4),
            "Outdoor" : np.zeros(4)
        }
    )
    for i in conditions_list:
        row_index = 0
        for j in surface_list:
            table.iloc[row_index,column_index] = len(set[(set["tourney_surface"] == j) & (tourney_final["tourney_conditions"] == i)])
            row_index += 1
        column_index += 1
    return table
            

surface_condition_table = surface_and_condition(tourney_final)

surface_condition_table.plot.pie(
    subplots = True,
    title = "Share of tournament surfaces in indoor and outdoor conditions",
    labels = ["Hard", "Clay", "Grass", "Carpet"],
    colors = ["dodgerblue", "chocolate", "yellowgreen", "darkred"],
    figsize = ([15,10]),
    autopct="%.1f"
)

#Analysis code
#Analyzing title counts based on player characteristics

## Tournament wins by height in cm, in

wins_height_in = pd.DataFrame(
    {"Wins" : tourney_final.iloc[:,13]}
)

wins_height_cm = pd.DataFrame(
    {"Wins" : tourney_final.iloc[:,14]}
)

plt.figure()

wins_height_in.plot.hist(
    ylabel = "Wins",
    xlabel = "Height (in)",
    bins = 15
    )

# wins_height_cm.plot.hist(
#     ylabel = "Wins",
#     xlabel = "Height(cm)",
#     bins = 15
#     )


## Has height distribution of tournament winners changed over time?

wins_height_in.describe() # avg winner height over all years in time period is approx 73 in i.e. 6' 1"

# Analyze by finding percentage of wins by players with height >= 74 in (one inch above the approx average) for each year, then plot this series

def ann_tall_ratio(table: pd.DataFrame) -> pd.DataFrame:
    store_proto: np.ndarray = np.zeros(shape=(len(range(1972,2018,1)),1))
    store: pd.DataFrame = pd.DataFrame(store_proto)
    index: int = 0
    for i in range(1972,2018,1):
        all_titles: int = 0
        titles_tall_winner: int = 0
        for j in range(len(table)):
            if table.iloc[j,0] == i and table.iloc[j,13] < 74:
                all_titles = all_titles + 1
            elif table.iloc[j,0] == i and table.iloc[j,13] >= 74:
                all_titles = all_titles + 1
                titles_tall_winner = titles_tall_winner + 1
        title_ratio: float = titles_tall_winner / all_titles
        store.iloc[index] = title_ratio
        index = index + 1
    return store

ratio_table = pd.DataFrame(
    {
        "Year" : np.array(range(1972,2018,1)),
        "Pct of tourney wins" : np.array(ann_tall_ratio(tourney_final).iloc[:,0])
    }
)

# Fix the index to have x-axis as years from 1972 to 2017

ratio_table.plot(ylabel = "Share of annual tourneys won by players 6ft 2in or taller",
                 x = "Year",
                 legend = False)         

## Is the distribution of champion heights different for different surfaces?

# Columns are surface, rows are tournament winners with height for each

surface_height_pivot: pd.DataFrame = tourney_final.pivot(columns = "tourney_surface", values = "height_inches")
# surface_height_pivot.head()

surface_height_pivot.plot.hist(
    stacked = True,
    bins = 15,
    color = ["darkred", "chocolate", "yellowgreen", "dodgerblue"],
    title = "Wins on the four surfaces by height (in)"
)

# Just for Izzy and Dr. Ivo

tall_boys: pd.DataFrame = tourney_final[tourney_final["height_inches"] >= 82]

surface_tall_pivot: pd.DataFrame = tall_boys.pivot(columns = "tourney_surface", values = "height_inches")

surface_tall_pivot.plot.hist(
    stacked = True,
    bins = 2,
    color = ["chocolate", "yellowgreen", "dodgerblue"],
    title = "Isner and Karlovic title breakdown by surface"
)

# Conditions

# Is indoors/outdoors an advantage for players of different heights?

conditions_pivot: pd.DataFrame = tourney_final.pivot(columns = "tourney_conditions", values = "height_inches")

conditions_pivot.plot.hist(
    stacked = True,
    bins = 15,
    color = ["darkslategray", "skyblue"]
)

# Handedness

# Do lefties have an advantage overall?

player_handedness.plot.pie(
    y = "Handedness",
    labels = ["Right-Handed", "Left-Handed"],
    colors = ["darkorchid", "plum"],
    figsize = ([6,6]),
    autopct = "%.2f",
    title = "Player handedness"
    )


title_count_righthand = len(tourney_final[tourney_final["handedness"] == "Right-Handed"])

title_count_lefthand = len(tourney_final[tourney_final["handedness"] == "Left-Handed"])

title_count_handedness = pd.DataFrame(
    {
        "Handedness": np.array([title_count_righthand, title_count_lefthand])
    }
)

title_count_handedness.plot.pie(
    y = "Handedness",
    labels = ["Right-Handed", "Left-Handed"],
    colors = ["royalblue", "lightskyblue"],
    figsize = ([6,6]),
    autopct = "%.2f",
    title = "Share of titles won by handedness"
)

tourney_norafa = tourney_final[tourney_final["player_slug"] != "rafael-nadal"]

title_count_lefthand_norafa: pd.DataFrame = len(tourney_norafa[tourney_norafa["handedness"] == "Left-Handed"])

title_handedness_norafa = pd.DataFrame(
    {
        "Handedness" : np.array([title_count_righthand, title_count_lefthand_norafa])
    }
)

title_handedness_norafa.plot.pie(
    y = "Handedness",
    labels = ["Right-Handed", "Left-Handed"],
    colors = ["royalblue", "lightskyblue"],
    figsize = ([6,6]),
    autopct = "%.2f",
    title = "Share of titles won by handedness, excluding Nadal"
)

# Backhand style

# Does one backhand style have a particular advantage?

player_backhand.plot.pie(
    y = "Backhand",
    labels = ["Two-Handed", "One-Handed"],
    colors = ["pink", "salmon"],
    figsize = ([6,6]),
    autopct = "%.2f",
    title = "Backhand type among male professionals"
    )

title_count_twohand: pd.DataFrame = len(tourney_final[tourney_final["backhand"] == "Two-Handed Backhand"])

title_count_onehand: pd.DataFrame = len(tourney_final[tourney_final["backhand"] == "One-Handed Backhand"])

title_backhand = pd.DataFrame(
    {
        "backhand" : np.array([title_count_twohand, title_count_onehand])
    }
)

title_backhand.plot.pie(
    y = "backhand",
    labels = ["Two-Handed", "One-Handed"],
    colors = ["palegreen", "mediumseagreen"],
    figsize = ([6,6]),
    autopct = "%.2f",
    title = "Titles won by backhand type"
)

# Remove Roger -- a clear outlier

tourney_noroger = tourney_final[tourney_final["player_slug"] != "roger-federer"]

title_count_twohand_noroger: pd.DataFrame = len(tourney_noroger[tourney_noroger["backhand"] == "Two-Handed Backhand"])

title_count_onehand_noroger: pd.DataFrame = len(tourney_noroger[tourney_noroger["backhand"] == "One-Handed Backhand"])

title_backhand_noroger = pd.DataFrame(
    {
        "backhand" : np.array([title_count_twohand_noroger, title_count_onehand_noroger])
    }
)

title_backhand_noroger.plot.pie(
    y = "backhand",
    labels = ["Two-Handed", "One-Handed"],
    colors = ["palegreen", "mediumseagreen"],
    figsize = ([6,6]),
    autopct = "%.2f",
    title = "Share of titles won by backhand styles, excluding Federer"
)

# How has the share of one-handed backhand victories changed over time?

def ann_backhand_breakdown(table: pd.DataFrame) -> pd.DataFrame:
    store_proto: np.ndarray = np.zeros(shape=(len(range(1972,2018,1)),2))
    store: pd.DataFrame = pd.DataFrame(store_proto)
    index: int = 0
    for i in range(1972,2018,1):
        one_tally : int = 0
        two_tally : int = 0
        for j in range(len(table)):
            if table.iloc[j,0] == i and table.iloc[j,16] == "One-Handed Backhand":
                one_tally = one_tally + 1
            elif table.iloc[j,0] == i and table.iloc[j,16] == "Two-Handed Backhand":
                two_tally = two_tally + 1
        store.iloc[index,0] = two_tally
        store.iloc[index,1] = one_tally
        index = index + 1
    return store

winners_by_backhand = ann_backhand_breakdown(tourney_final)
# winners_by_backhand.head(10)

winners_by_backhand = winners_by_backhand.rename(
    columns = {
        0 : "Two-Handed Backhand",
        1 : "One-Handed Backhand"
    }
)

# Fix the indexing

years_col = winners_by_backhand["Two-Handed Backhand"].index + 1972

years_col = years_col.to_numpy()
years_col = pd.DataFrame({"Year" : years_col})

winners_by_backhand = winners_by_backhand.reset_index(drop = True)

winners_by_backhand = pd.concat([years_col, winners_by_backhand], axis = 1, join = "inner")

colors = ["indigo", "mediumpurple"]

winners_by_backhand.plot.bar(
    stacked = True,
    x = "Year",
    figsize = ([10,6]),
    color = colors,
    title = "How good is the one-hander?"
)

# Is the one-handed backhand declining in popularity over time?

# Find the faction of players who turned pro in a given year with one-handed backhands, for every year turned pro
# Assuming that turned pro is an adequate proxy for age, since the vast majority of players turn pro in their late-teens/early twenties.

def backhand_func(table : pd.DataFrame) -> pd.DataFrame:
    store_proto: np.ndarray = np.zeros(shape=(len(range(1972,2015,1)),2))
    store: pd.DataFrame = pd.DataFrame(store_proto)
    index: int = 0
    for i in range(1972,2015,1):
        two_tally : int = 0
        one_tally : int = 0
        for j in range(len(table)):
            if table.iloc[j,3] == i and table.iloc[j,9] == "Two-Handed Backhand":
                two_tally = two_tally + 1
            elif table.iloc[j,3] == i and table.iloc[j,9] == "One-Handed Backhand":
                one_tally = one_tally + 1
        store.iloc[index, 0] = two_tally
        store.iloc[index, 1] = one_tally
        index = index + 1
    return store

backhand_table = backhand_func(set_final)

backhand_table = backhand_table.rename(
    columns = {
        0 : "Two-Handed Backhand",
        1 : "One-Handed Backhand"
    }
)

# Remove years where there are no players in the dataset who turned pro in that year

mask = (backhand_table["Two-Handed Backhand"] != 0) & (backhand_table["One-Handed Backhand"] != 0)

unwanted_rows = backhand_table[~mask]

backhand_table = backhand_table.drop(unwanted_rows.index)

# Fix the indexing

years_col = backhand_table["Two-Handed Backhand"].index + 1972

years_col = years_col.to_numpy()

years_col = pd.DataFrame({"Year" : years_col})

backhand_table = backhand_table.reset_index(drop = True)

backhand_table = pd.concat([years_col, backhand_table], axis = 1, join = "inner")

colors = ["indigo", "mediumpurple"]

backhand_table.plot.bar(
    stacked = True,
    x = "Year",
    figsize = ([10,6]),
    color = colors,
    title = "Backhand type among new pros"
)
