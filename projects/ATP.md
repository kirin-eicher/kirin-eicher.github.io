---
layout: project
type: project
image: img/project_images/surface_timeline.png
title: "ATP Tennis Tournament Winner Analysis"
date: 2023
published: true
labels:
  - Python
  - Pandas
  - Numpy
  - Matplotlib
  - Excel
  - Visualization
summary: "Using data on professional tournament wins to determine which characteristics set players up for success."
---

## Introduction

Tennis is one the world's most popular sports, with nearly one billion people tuning in annually to watch the greatest players contend for titles and glory. Many cite the diversity of play styles as tennis' greatest appeal; the different game plans, techniques, and body types of tennis players makes for endless combinations to create unique plays and strategies. With so many ways to compete, an age-old concern has been determining how play styles compare against each other. And since these play styles are determined in part by the players' physical characteristics, it's worth considering what the most desirable physical attributes are. Do left-handed players have an advantage over right-handed players? Is a two-handed backhand really that much better than the classic one-hander? Do the tallest players dominate the professional tour?

This project aims to find answers to these questions using data on tournament winners from the Association of Tennis Professionals (ATP), the premier international men's tennis tour. 

The data for this project are found in `tournaments_1877-2017_unindexed.csv` and `player_overviews_unindexed.csv`. The data are taken from the DataHub.io page on ATP World Tour tennis data. A link to page with data used for this project, as well as other datasets, can be found [here](https://datahub.io/sports-data/atp-world-tour-tennis-data)

## Data preparation

`tournaments_1877-2017_unindexed.csv` contains data on all tournaments held on the ATP World Tour between 1877 and 2017, including the four majors. The data describe tournament date, location, playing surface, whether the tournament is indoors, and tournament winner, among other things. `player_overviews_unindexed.csv` contains information on players born in 1864 and after. The dataset contains player nationality, birth date, the year in which the player turned pro, height (in inches and centimeters), weight (in pounds and kilograms), handedness (whether they play left- or right-handed), and backhand type (whether they use a one- or two-handed backhand).

Using excel, the data on relevant player characteristics (i.e. height, weight, handedness, backhand, nationality) were merged into the tournament dataset by joining on the name of the tournamnet winner. We also need a measure of how successful players are. To get this, I created an excel function which would count the number of times that a player's name appears in the tournament data set and return the value for each player in the player dataset. This will allow us to compare the success of all players in the dataset. A python function performing the same process is given in the code as `title_ct`, but this is not used in creating the analysis datasets.

The data as given contain many columns which contain mostly missing values or which are not relevant to analyzing player performance characteristics. There are also many players in `player_overviews_unindexed.csv` that have little to no information in the dataset. Removing all of these instances will simplify our analysis, albeit with drawbacks related to how well the dataset represents the ATP tour population. In particular, players with little to no data tend to be older players who competed at a time when record keeping was less robust, meaning our final dataset heavily overrepresents recent players.

```python
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
```
<img class="img-fluid" src="../img/project_images/set_final_head.png" width="80%">

With data on both the tournaments played and the players who competed, we can create a cleaned and merged dataset which displays player data for each champion at the annual tournament level:

```python
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

```

> image here

# Summary stats

First, let's look at some summary statistics on the players in the data set:

> image here

The table above provides some interesting insights into the sample of 550 players in the dataset:
 - The median year turned pro is 2004. Since the range of years is 1969 to 2017, this is an indication that the dataset over-represents modern players.
 - Perhaps as expected, the distribution of heights and weights illustrates a relatively fit group of players. Player weights range between 141 and 238 lbs, and the shortest and tallest players are 5'6" and 6'11, respectively.

Next, let's use some visualiztions to understand the players more thoroughly:

> image here
> image here
> image here
> image here

Height:
 - Player height is predictably skewed to the right, with a median at 73 inches. There is, however, a clear mode in the bin just below 75 in (6ft 3in). Half of all players are between 70 and 75 inches, and there are far more players below this range than above.

Weight:
 - Player weight seems right-skewed with a mean at 176.4 lbs. The highest weight in here is 238 lbs, and the lowest is 141 lbs.
Half of all players in the data set are between 165 and 185, with more below this weight than above.

Handedness:
 - The pie chart shows that the overwhelming majority of players (85.12%) are right-handed.

Backhand style:
 - The pie chart shows that roughly 75% of players use a two-handed backhand.

Now, a look at some basic tournament characteristics:

> image here
> image here
> image here
> image here

Some notes from these figures:
 - The first pie chart provides strong insight into the prevalence of each tennis court surface for the past 50 years. Hard courts are used at nearly half of all tournaments, while clay courts make up roughly a third. Grass and carpet tournaments are comparatively rare.
 - It is also clear that most tournaments are played outside. In fact, virtually all indoor tournaments are played on hard and carpet courts, while outdoor tournaments are always on hard, grass, or clay with few exceptions.
 - The bar graph shows that hard and clay have together been the predominant surfaces for play since at least the early 90's.
 - However, the relative shares of hard, clay, and grass tournaments every year does not show a clear trend.
 - If anything, the number of grass court tournaments has increased steadily as a share of all tournaments played.
 - Carpet tournamnets used to be the most common, but have gradually been phased out. Now there are currently no professional events
held on carpet.

# What makes a good tennis player?

## Height

First, let's examine the attribute which is most commonly associated with advantage in tennis: height. Taller players have longer limbs are are able to more easily cover areas of the court than shorter players. Taller players also have better angles to hit offensive serves and take high balls early. Most people believe taller players have an advantage over smaller players.

> image here

But what do the data say? Looking at the heights of tournament winners in the dataset, this advantage isn't apparent. Comparing the distribution of wins with the distribution of player heights overall, there is not any indication that the tallest players are most likely to win. Rather, the players winning a disproportionately large amount of tournaments are those between 6'1" and 6'3". This goldilocks zone suggests that the optimal height is one that is just above average.

```python
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
```

> image here

But this advantage depends on the type of tennis that players are playing. As tennis points have become longer and less focused on serve-and-volley tactics, the importance of the serve has decreased slightly. Such a shift could neutralize the advantage of taller players. To illustrate this, I created a function to calculate the fraction of tournaments every year that were won by players with heights 6'2" or above. The resulting time series indicates that the height advantage has not been constant over time. Being tall was a huge advantage in the 80s, with over 80% of tournaments being won by tall players in those years. As baseline styles evloved in the 90s and 2000s, however, the dominance of tall players dipped, and tall players won only roughly half of annual tournaments.

We see an interesting uptick in tall wins in the 2010s. It's possible that tall players who grew up playing modern tennis are now better able to combine the best aspects of modern baseline tennis with the service advantages of their height. Regardless, it's clear that the ideal tennis height is not fixed, but rather changes as the sport itself changes.

We can also examine how height helps players on different surfaces and in different conditions:

> image here

This breakdown provides some analytical clarity on a common discussion among tennis fans: do different surfaces favor people of different heights?
The concensus is that the fast, low bounce of a grass court makes big serves even more potent, giving the edge to tall players.
Meanwhile, the slow, high bounce of clay courts favors shorter players who are able to netrualize powerful shots and extend rallies,
beating bigger players with their superior endurance. Hard and carpet courts are somewhere in-between.

The data suggest that this may be the case. The first graph shows the distribution of winner heights broken out into the four surfaces. Comparing clay results to hard and grass, players just under 6'0" have almost as many clay court wins as players in the goldilocks zone. Hard and grass court wins still strongly favor players between 6'1" and 6'3". The opposite advantage on grass for taller players is not borne out in the data.

There does seem to be a disproportionate share of tournaments won by players around 82.5 inches tall.
Only two players in this dataset -- John Isner and Ivo Karlovic -- are this tall, and yet they have a combined 21 titles.

> image here

Focusing on their title wins, it is clear that their titles are disporportionately skewed to hard and grass courts.
Even though grass tournaments have been far less common during their careers than clay tournaments, both players have more grass court
titles. Although there are too few data points to make a conclusive judgment, the titles of these extremely tall players are evidence suggesting that extreme height may be an advantage, but primarily on hard and grass courts. On clay courts, being nearly 7 feet tall seems to do more harm than good.

## Handedness

> image here
> image here

Handedness also plays a large role in determining how players match up against each other. Most believe that left-handed players, who are far less common than righties, have an advantage since other players will not be used to the unique spins generated by playing with the other hand. Is this true?

The title count data seems to suggest that left-handed players win a slightly disproportionately higher share of tournaments than right-handed players, although this margin is quite small. 

We also have to acknowledge that there is a notable left-handed outlier: Rafael Nadal. Nadal, who holds 75 of the titles in this dataset, may single-handedly be inflating the share of lefty victories. To check this, I reran the analysis, excluding Nadal from the dataset.

After excluding Nadal, the proportion of titles won by left-handed players falls to a level very similar to the propotion of left-handed
players in the dataset (14.88 of players vs 13.73 of titles). Most would agree that Rafa Nadal's immense success as a professional player
is not due mainly to the his left-handed shots but instead his excellent fitness and competitive spirit. The data show that, overall, left-handed players are roughly just as successful as right-handed players when it comes to winning tournaments.

Finally, let's look at the importance of backhand type.

>image here
>image here

The debate between one- and two-handed backhands is intense, and there is no one concensus on which is better. One-handers generally are able to generate more top-spin and therefore more versatility, while two-handed backhands are more consistent and reliable. Two-handed backhands are also generally easier to learn and master. Can the data settle this debate once and for all?

These first two charts above indicate that one-handed backhands have a clear advantage over two-handed ones. Despite only making up 26% of players in the dataset, one-handed backhand users have won more than 38% of the titles. This could be due to the increased range of motion, topspin, and variety that is afforded to people with one-handed backhands. 

But wait! Before you go switch to one-hander yourself, note that there is a very significant outlier in the population of one-handers: Roger Federer.

As of 2017, Federer has captured 95 titles on the ATP tour, trailing only Jimmy Connors in the number of titles held. That is roughly 14%
of all titles won by one-handed players and 5% of all titles in the dataset. Even excluding Federer from the analysis, one-handers seem to win an outsize share of the titles on tour (over 35%). Perhaps having a one-handed backhand is the best physical advantage you can give yourself, at least according to the data.

```python
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
```

> image here
> image here

The first purple graph shows the share of titles won every year by one- and two-handed players. What's immediately clear is that, despite the one-handed backhand declining in popularity, one-handers manage to win more than their fair share of titles on tour even at points in the 2010s. Although two-handers have dominated at times, one-handers have never been completely shut out of the winners' circle. At the very least, an effective one-hander is certainly not a disadvantage.

The changing share of one-handed backhands in recent years may shed some light on the success of one-handed players. The second graph shows the backhand style breakdown of players who have turned pro in every year from 1986 to 2013. Early on one-handers seemed to be slightly more popular, until the 2000s when two-handed backhands began to dominate the tour. Therefore, part of the overrepresentation of one-handers in the winners dataset may be due to the fact that many of the younger two-handers have not yet finished their career and thus have not had the chance to accumulate as many titles. Nevertheless, the success of one-handers is a notable trend in the data across all years.

