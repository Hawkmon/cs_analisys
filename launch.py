import sys
import pandas as pd

from defs import player_choice
from defs import table_counter
from defs import visualising
from defs import visualising2

df = pd.read_excel('cs.xlsx')
df1, chosen_player = player_choice(df)
df1, values, categories = table_counter(df1)

print('1. Средние показатели игрока')
print('2. Динамика показателя игрока')
option2 = input('Выберите опцию: ')
if option2 == '1':
    print(df1.to_string())

    visualising(values, categories, chosen_player)

elif option2 == '2':
    stats_seria = pd.Series(['k','d','swing','adr','kast','rating','kd','kpr','dpr','surv'])
    print(stats_seria)
    chosen_stat = int(input('Выберите показатель: '))
    stat = stats_seria[chosen_stat]
    chosen_stat_seria = pd.Series(df1[stat])

    visualising2(df1, chosen_player, stat)

else:
    sys.exit(0)