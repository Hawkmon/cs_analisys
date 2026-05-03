import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta

def table_counter(df1):
    try:
        df1['kd'] = (df1['k'] / df1['d']).round(2)
        df1['kpr'] = (df1['k'] / (df1['rounds_win'] + df1['rounds_loss'])).round(2)
        df1['dpr'] = (df1['d'] / (df1['rounds_win'] + df1['rounds_loss'])).round(2)
        df1['surv%'] = (((df1['rounds_win'] + df1['rounds_loss'] - df1['d']) / (df1['rounds_win'] + df1['rounds_loss'])) * 100).round(2)

        avg_rating = df1['rating'].mean().round(2)
        avg_kd = df1['kd'].mean().round(2)
        avg_kpr = df1['kpr'].mean().round(2)
        avg_dpr = df1['dpr'].mean().round(2)
        avg_surv = df1['surv%'].mean().round(2)
        avg_k = df1['k'].mean().round(2)
        avg_d = df1['d'].mean().round(2)
        #avg_swing = df1['swing'].mean().round(2)
        avg_adr = df1['adr'].mean().round(2)
        avg_kast = df1['kast'].mean().round(2)
        values = pd.Series([avg_rating, avg_kd, avg_kpr, avg_dpr, avg_surv, avg_k, avg_d, avg_adr, avg_kast])
        categories = pd.Series(
            ['avg_rating', 'avg_kd', 'avg_kpr', 'avg_dpr', 'avg_surv', 'avg_k', 'avg_d', 'avg_adr',
             'avg_kast'])
        return df1, values, categories
    except:
        print('нет матчей, подходящих под выбранный критерий')
        sys.exit()

def visualising(values, categories, player):
    ref_values = [1.0, 0.8, 0.5, 0.7, 50, 12, 14, 50, 60]

    normalized = [(v / ref) * 100 for v, ref in zip(values, ref_values)]
    colors = []
    for norm in normalized:
        if norm > 110:
            colors.append('#2E8B57')
        elif norm < 90:
            colors.append('#DC143C')
        else:
            colors.append('#FFD700')
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='white')
    ax.set_facecolor('white')
    x = np.arange(len(categories))
    width = 0.6
    bars = ax.bar(x, normalized, width, color=colors)
    ax.axhline(y=100, linestyle='--', color='black', alpha=0.3)
    ax.axhline(y=0, color='black')
    for bar, val, norm, cat in zip(bars, values, normalized, categories):
        if cat in ['avg_rating', 'avg_kd', 'avg_kpr', 'avg_dpr']:
            value_text = f'{val:.2f}'
        elif cat in ['avg_surv', 'avg_swing']:
            value_text = f'{val:.2f}%'
        elif cat in ['avg_k', 'avg_d', 'avg_adr', 'avg_kast']:
            value_text = f'{val:.1f}'
        else:
            value_text = f'{val:.2f}'
        if cat != 'avg_swing':
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3, f'{value_text}\n({norm:.1f}%)', ha='center',
                    va='bottom', fontsize=9)
        else:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3, f'{value_text}', ha='center',
                    va='bottom', fontsize=9)

    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylim(min(normalized) - 50, max(normalized) + 50)
    ax.set_title(f'Статистика {player}')
    plt.show()

def player_choice(df):
    a = input('1. Выбрать временной промежуток\n2. Выбрать турнир\nВыберите опцию:')
    if a == '1':
        time = pd.Series(['месяц','3 месяца','полгода','год','все время','произвольный промежуток'])
        print(time)
        chosen_time = int(input('Выберите временной промежуток: '))
        cur_date = datetime.now()
        if chosen_time == 0:
            start_date = cur_date - relativedelta(months=1)
        elif chosen_time == 1:
            start_date = cur_date - relativedelta(months=3)
        elif chosen_time == 2:
            start_date = cur_date - relativedelta(months=6)
        elif chosen_time == 3:
            start_date = cur_date - relativedelta(years=1)
        elif chosen_time == 4:
            start_date = df['date'].min()
        else:
            start_date = input('Введите начало периода (дд.мм.гг): ')
            start_date = datetime.strptime(start_date, '%d.%m.%y')
            cur_date =  input('Введите конец периода (дд.мм.гг): ')
            cur_date = datetime.strptime(cur_date, '%d.%m.%y')
        df = df[df['date'].between(start_date,cur_date)]
    else:
        tournaments_seria = pd.Series(df['tournament'].unique())
        tournaments_seria = pd.concat([pd.Series(['all']), tournaments_seria], ignore_index=True)
        print(tournaments_seria)
        chosen_tournament = input('Выберите турнир: ')
        chosen_tournament = tournaments_seria[int(chosen_tournament)]
        if chosen_tournament != 'all':
            df = df[df['tournament'] == chosen_tournament]

        stages_seria = pd.Series(df['stage'].unique())
        stages_seria = pd.concat([pd.Series(['all']), stages_seria], ignore_index=True)
        print(stages_seria.to_string())
        chosen_stage = input('Выберите стадию: ')
        chosen_stage = stages_seria[int(chosen_stage)]
        if chosen_stage != 'all':
            df = df[df['stage'] == chosen_stage]

    teams_seria = pd.Series(df['team'].unique())
    print(teams_seria.to_string())
    chosen_team = input('Выберите команду: ')
    chosen_team = teams_seria[int(chosen_team)]

    players_df = df[df['team'] == chosen_team]
    players_seria = pd.Series(players_df['player'].unique())
    print(players_seria)
    chosen_player = input('Выберите игрока: ')
    chosen_player = players_seria[int(chosen_player)]
    team_df = df[df['team'] == chosen_team]

    opponent_seria = pd.Series(team_df['opponent'].unique())
    opponent_seria = opponent_seria[opponent_seria != chosen_team].reset_index(drop=True)
    opponent_seria = pd.concat([pd.Series(['all']), opponent_seria], ignore_index=True)
    print(opponent_seria)
    chosen_opponent = input('Выберите оппонента: ')
    chosen_opponent = opponent_seria[int(chosen_opponent)]

    if chosen_opponent != 'all':
        player_df = df[(df['player'] == chosen_player) & (df['opponent'] == chosen_opponent)]
    else:
        player_df = df[(df['player'] == chosen_player)]
    maps = pd.Series(player_df['map'].unique())
    maps = pd.concat([pd.Series(['all']), maps], ignore_index=True)
    print(maps.to_string())
    chosen_map = input('Выберите карту: ')
    chosen_map = maps[int(chosen_map)]

    mask = (df['player'] == chosen_player)

    if chosen_opponent != 'all':
        mask &= (df['opponent'] == chosen_opponent)
    if chosen_map != 'all':
        mask &= (df['map'] == chosen_map)

    df1 = df[mask].copy()

    return df1, chosen_player

def visualising2(df1, chosen_player, stat):
    df1['date'] = pd.to_datetime(df1['date'], format='%d.%m.%Y')
    df1_sorted = df1.sort_values('date').reset_index(drop=True)
    df1_sorted['match_num'] = range(1, len(df1_sorted) + 1)

    fig, ax = plt.subplots(figsize=(15, 7))

    ax.plot(df1_sorted['match_num'], df1_sorted[stat], marker='o', linestyle='-', linewidth=2, markersize=8,
            color='steelblue')
    ax.set_xticks(df1_sorted['match_num'])
    ax.axhline(0, color='black', linewidth=1)

    x_labels = []

    for idx, row in df1_sorted.iterrows():
        date_str = row['date'].strftime('%d.%m.%Y')
        x_labels.append(date_str)

    ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=8)
    for idx, row in df1_sorted.iterrows():
        annotation_text = f"{stat}: {row[stat]}\n{row['map']}\n{row['opponent']}"

        xytext_offset = (10, -12)
        ha = 'left'
        va = 'top'

        ax.annotate(annotation_text, xy=(row['match_num'], row[stat]),
                    xytext=xytext_offset,
                    textcoords='offset points',
                    ha=ha, va=va,
                    fontsize=7,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.8, edgecolor='gray'),
                    arrowprops=dict(arrowstyle='->', color='gray', alpha=0.6, lw=0.5))

    ax.set_xlabel('Дата матча', fontsize=12)
    ax.set_ylabel(stat, fontsize=12)
    ax.set_title(f"{chosen_player} - {stat} динамика", fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim(0.5, len(df1_sorted) + 1)
    ax.set_ylim(min(df1_sorted[stat]) - 2.5, max(df1_sorted[stat]) + 2.5)

    plt.tight_layout()
    plt.show()
