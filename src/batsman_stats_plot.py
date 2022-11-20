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
        data.append({'year':year, 'batsman':batsman_1_name, 'runs':run})

for year in runs_per_match_p2:
    for run in runs_per_match_p2[year]:
        data.append({'year':year, 'batsman':batsman_2_name, 'runs':run})

df = pd.DataFrame(data)
sns.violinplot(data=df, x="year", y="runs", hue="batsman",
               split=True, inner="quart", linewidth=1)
sns.despine(left=True)



# Plotting max runs of various players througout out IPL
max_runs_data = {}

batsman_name = "V Kohli"
player = PlayerPerformance(batsman_name)
years, _, max_runs, _, _ = player.get_player_performance() 
max_runs_data[batsman_name] =  max_runs

batsman_name = "CH Gayle"
player = PlayerPerformance(batsman_name)
years, _, max_runs, _, _ = player.get_player_performance()
max_runs_data[batsman_name] =  max_runs

batsman_name = "RG Sharma"
player = PlayerPerformance(batsman_name)
years, _, max_runs, _, _ = player.get_player_performance()
max_runs_data[batsman_name] =  max_runs

batsman_name = "SR Watson"
player = PlayerPerformance(batsman_name)
years, _, max_runs, _, _ = player.get_player_performance()
max_runs_data[batsman_name] =  max_runs

plt.figure(figsize=(10, 7))
plt.title("Max runs over many seasons")
for key, value in max_runs_data.items():
    plt.plot(value, label=key, marker="o")

plt.xticks(range(len(years)), years)
plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.0),
    fancybox=True, shadow=True, ncol=4)
