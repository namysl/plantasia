import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def flat_list(list_of_lists):
    flat = []
    for sublist in list_of_lists:
        for item in sublist:
            flat.append(item)
    return flat


def read_data(column, date1='', date2='', last_x_days=0):
    plant = pd.read_csv('example_plant_data.csv')
    plant['date'] = pd.to_datetime(plant['date'], dayfirst=True).dt.date

    if date1 and date2:
        date1 = pd.to_datetime(date1, dayfirst=True)
        date2 = pd.to_datetime(date2, dayfirst=True)

        mask = (plant['date'] >= date1) & (plant['date'] <= date2)
        plant = plant.loc[mask]

    min_val = plant[['date', column]].groupby('date').min()
    max_val = plant[['date', column]].groupby('date').max()
    mean_val = plant[['date', column]].groupby('date').mean()

    min_list = flat_list(min_val.values.tolist())
    max_list = flat_list(max_val.values.tolist())
    mean_list = flat_list(mean_val.values.tolist())
    mean_list = list(np.around(np.array(mean_list), 2))

    days = plant.date.unique().tolist()

    if len(days) == 0:
        raise IndexError

    if last_x_days > 0:
        min_list = min_list[-last_x_days:]
        max_list = max_list[-last_x_days:]
        mean_list = mean_list[-last_x_days:]
        days = days[-last_x_days:]

    return min_list, max_list, mean_list, days, column


def plotting(data, with_mean):
    min_val, max_val, mean_val = data[0], data[1], data[2]
    days = data[3]
    column = data[4]

    x = np.arange(len(days))
    width = 0.15

    fig, ax = plt.subplots(figsize=(13, 8))
    min_subplot = ax.bar(x - width / 2, min_val, width, label='min', color='lightblue')
    max_subplot = ax.bar(x + width / 2, max_val, width, label='max', color='orange')
    if with_mean is True:
        mean_subplot = ax.bar(x + width * 2 - width / 2, mean_val, width, label='mean', color='gray')

    ax.bar_label(min_subplot, padding=5, size='x-small', rotation='vertical')
    ax.bar_label(max_subplot, padding=5, size='x-small', rotation='vertical')
    if with_mean is True:
        ax.bar_label(mean_subplot, padding=5, size='x-small', rotation='vertical')

    ax.set_title('min/max values of ' + column)
    ax.set_xlabel('days')
    ax.set_ylabel(column)

    plt.xticks(fontsize='small', rotation='vertical')
    ax.set_xticks(x)
    ax.set_xticklabels(days)

    ax.grid(axis='y', linestyle=':', linewidth=0.8)
    ax.legend(loc='best', fontsize='x-small')

    fig.tight_layout()
    plt.show()


def bar_chart(column, date1='', date2='', last_x_days=0, with_mean=False):
    assert column in ['temp_c', 'air', 'light', 'soil']
    assert isinstance(date1, str), 'date1 must be a string'
    assert isinstance(date2, str), 'date2 must be a string'
    assert isinstance(last_x_days, int), 'last_x_days must be an integer'

    try:
        plotting(read_data(column, date1, date2, last_x_days), with_mean)
    except IndexError:
        print('\nno data for that day\n')


# bar_chart('temp_c', '2021/6/01', '2021-06-10', last_x_days=20, with_mean=True)
# bar_chart('temp_c', last_x_days=1, with_mean=True)
# bar_chart('temp_c', '2021/5/01', '2021/05/20')
