import pandas as pd
import matplotlib.pyplot as plt


def flat_list(list_of_lists):
    flat = []
    for sublist in list_of_lists:
        for item in sublist:
            flat.append(item)

    return flat


def convert_time(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "{}h : {}m : {}s".format(hour, minutes, seconds)


def read_data(day, column):
    day_pd = pd.to_datetime(day, dayfirst=True)

    plant = pd.read_csv('example_plant_data.csv')

    plant['date'] = pd.to_datetime(plant['date'], dayfirst=True).dt.date

    mask_time = (plant['date'] >= day_pd) & (plant['date'] <= day_pd)
    plant = plant.loc[mask_time]

    std = plant[['date', column]].groupby('date').std().values[0][0]

    # min/max values +/- std
    min_val = plant[['date', column]].groupby('date').min().values[0][0]
    min_val += std
    min_val = round(min_val, 2)

    max_val = plant[['date', column]].groupby('date').max().values[0][0]
    max_val -= std
    max_val = round(max_val, 2)

    list_of_values = [min_val, max_val]

    # masked data -> values -> len
    mask_le = (plant[column] <= min_val)
    len_le = len(plant.loc[mask_le])

    mask_between = (plant[column] > min_val) & (plant[column] < max_val)
    len_between = len(plant.loc[mask_between])

    mask_ge = (plant[column] >= max_val)
    len_ge = len(plant.loc[mask_ge])

    return len_le, len_between, len_ge, list_of_values, day, column


def plotting(data):
    len_less = data[0]
    len_between = data[1]
    len_more = data[2]
    measure_s = (data[0] + data[1] + data[2]) * 10  # all rows are 10 seconds apart

    list_val = data[3]
    day = data[4]
    column = data[5]

    if column == 'temp_c':
        unit = 'C'
    else:
        unit = '%'

    labels = '≤{} {}'.format(list_val[0], unit), \
             '({} {}, {} {})'.format(list_val[0], unit, list_val[1], unit), \
             '≥{} {}'.format(list_val[1], unit)

    sizes = [len_less, len_between, len_more]
    explode = (0, 0.05, 0)
    colors = ['lightblue', 'gray', 'orange']

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(sizes, explode=explode, labels=labels, autopct='%1.2f%%', colors=colors, startangle=90)
    ax.axis('equal')

    plt.title(column + '\n' + r'$\bf{' + day + '}$' + '\n time of measurment: ' + convert_time(measure_s) + '\n')
    plt.legend(title='{} intervals:'.format(column), loc='upper right')
    plt.tight_layout()
    plt.show()


def pie_chart(day, column):
    assert isinstance(day, str), 'day must be a string'
    assert isinstance(column, str), 'column must be a string'

    try:
        plotting(read_data(day, column))
    except IndexError:
        print('\nno data for that day\n')


# pie_chart('20-05-2021', 'temp_c')
