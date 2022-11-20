from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
from player_performance import PlayerPerformance

#Player performance over all seasons - Strike rate and Seasonal runs
batsman_1_name = "MS Dhoni"
player = PlayerPerformance(batsman_1_name)
years, strike_rate, max_runs, average, total_runs = player.get_player_performance() 
fig, ax1 = plt.subplots()
plt.title(f'{batsman_1_name} Performance')
ax2 = ax1.twinx()
ax1.bar(years, total_runs)
ax2.plot(years, strike_rate, '-o', color='red')
ax1.set_xlabel('Year')
ax1.set_ylabel('Total Runs', color='b')
ax2.set_ylabel('Strike Rates', color='r')
plt.show()
plt.close()

# Player performance over all seasons - Strike rate and Seasonal runs
batsman_2_name = "RG Sharma"
player = PlayerPerformance(batsman_2_name)
years, strike_rate, max_runs, average, total_runs = player.get_player_performance() 
fig, ax1 = plt.subplots()
plt.title(f'{batsman_2_name} Performance')
ax2 = ax1.twinx()
ax1.bar(years, total_runs, color = 'grey')
ax2.plot(years, strike_rate, '-o', color='purple')
ax1.set_xlabel('Year')
ax1.set_ylabel('Total Runs', color='grey')
ax2.set_ylabel('Strike Rates', color='purple')
plt.show()
plt.close()


# Compare form of 2 players through IPL. 
# Compares run distribution of each player per season
batsman_1_name = "V Kohli"
player1 = PlayerPerformance(batsman_1_name)
runs_per_match_p1 = player1.get_runs_per_match()

batsman_2_name = "RG Sharma"
player2 = PlayerPerformance(batsman_2_name)
runs_per_match_p2 = player2.get_runs_per_match()

# ames = ['year', 'batsman', 'runs']
data = []
for year in runs_per_match_p1:
    for run in runs_per_match_p1[year]:
        data.append({'year':year, 'batsman':batsman_1_name, 'run':run})


for year in runs_per_match_p2:
    for run in runs_per_match_p2[year]:
        data.append({'year':year, 'batsman':batsman_2_name, 'run':run})

df = pd.DataFrame(data)
sns.violinplot(data=df, x="year", y="run", hue="batsman",
               split=True, inner="quart", linewidth=1)
sns.despine(left=True)
plt.show()


# Plotting max runs of various players througout out IPL
sns.set_theme(style="whitegrid")

batsman_name = "V Kholi"
player = PlayerPerformance(batsman_name)
years, _, max_runs, _, _ = player.get_player_performance() 
data = []
for i in range(len(max_runs)):
    data.append({'year':years[i], 'batsman':batsman_name, 'max_runs':max_runs[i]})


batsman_name = "CH Gayle"
player = PlayerPerformance(batsman_name)
years, _, max_runs, _, _ = player.get_player_performance()
for i in range(len(max_runs)):
        data.append({'year':years[i], 'batsman':batsman_name, 'max_runs':max_runs[i]})

batsman_name = "RG Sharma"
player = PlayerPerformance(batsman_name)
years, _, max_runs, _, _ = player.get_player_performance()
for i in range(len(max_runs)):
        data.append({'year':years[i], 'batsman':batsman_name, 'max_runs':max_runs[i]})

batsman_name = "SR Watson"
player = PlayerPerformance(batsman_name)
years, _, max_runs, _, _ = player.get_player_performance()
for i in range(len(max_runs)):
        data.append({'year':years[i], 'batsman':batsman_name, 'max_runs':max_runs[i]})

df = pd.DataFrame(data)

sns.lineplot(data=data, palette="tab10", linewidth=2.5)
plt.show()

