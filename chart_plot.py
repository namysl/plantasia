import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


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


def min_max(column, data):
    plant = data

    max_val = plant[['time', column]].groupby(column).max()
    max_val = flat_list(max_val.values.tolist())[-1]

    max_time = plant[column].max()

    min_val = plant[['time', column]].groupby(column).min()
    min_val = flat_list(min_val.values.tolist())[0]

    min_time = plant[column].min()

    return max_val, max_time, min_val, min_time


def read_data(day, with_min_max):
    day_pd = pd.to_datetime(day, dayfirst=True)

    plant = pd.read_csv('example_plant_data.csv')

    plant['date'] = pd.to_datetime(plant['date'], dayfirst=True).dt.date

    mask = (plant['date'] >= day_pd) & (plant['date'] <= day_pd)
    plant = plant.loc[mask]

    temp_c_list = flat_list(plant[['temp_c']].values.tolist())
    air_list = flat_list(plant[['air']].values.tolist())
    light_list = flat_list(plant[['light']].values.tolist())
    soil_list = flat_list(plant[['soil']].values.tolist())
    time_list = flat_list(plant[['time']].values.tolist())

    if len(time_list) == 0:
        raise IndexError

    if with_min_max is True:
        mm_temp_c = min_max('temp_c', plant)
        mm_air = min_max('air', plant)
        mm_light = min_max('light', plant)
        mm_soil = min_max('soil', plant)

        mm_list = [mm_temp_c, mm_air, mm_light, mm_soil]
        return temp_c_list, air_list, light_list, soil_list, time_list, day, mm_list
    else:
        return temp_c_list, air_list, light_list, soil_list, time_list, day


def plotting(data, with_min_max):
    temp_c, air, light, soil = data[0], data[1], data[2], data[3]
    time = data[4]
    day = data[5]

    measure_s = len(time) * 10  # each row is 10 seconds apart

    x_axis_ticks = int(len(time) / 10)

    fig = plt.figure(figsize=(15, 7))

    sub1 = fig.add_subplot(411)
    sub1.set_title(r'$\bf{' + day + '}$' + '\ntime of measurment: ' + convert_time(measure_s) + '\n\ntemp_c')
    sub1.plot(time, temp_c, '-')
    sub1.grid(True)
    plt.xticks(np.arange(0, len(time) + 1, x_axis_ticks))

    sub2 = fig.add_subplot(412)
    sub2.set_title('air')
    sub2.plot(time, air, '-')
    sub2.grid(True)
    plt.xticks(np.arange(0, len(time) + 1, x_axis_ticks))

    sub3 = fig.add_subplot(413)
    sub3.set_title('light')
    sub3.plot(time, light, '-')
    sub3.grid(True)
    plt.xticks(np.arange(0, len(time) + 1, x_axis_ticks))

    sub4 = fig.add_subplot(414)
    sub4.set_title('soil')
    sub4.plot(time, soil, '-')
    sub4.grid(True)
    plt.xticks(np.arange(0, len(time) + 1, x_axis_ticks))

    if with_min_max is True:
        mm = data[6]  # list of lists
        mm_temp_c, mm_air, mm_light, mm_soil = mm[0], mm[1], mm[2], mm[3]

        print('min/max values:')
        print('temp_c:', mm_temp_c)
        sub1.plot(mm_temp_c[0], mm_temp_c[1], 'ro')
        sub1.plot(mm_temp_c[2], mm_temp_c[3], 'bo')

        print('air:', mm_air)
        sub2.plot(mm_air[0], mm_air[1], 'ro')
        sub2.plot(mm_air[2], mm_air[3], 'bo')

        print('light:', mm_light)
        sub3.plot(mm_light[0], mm_light[1], 'ro')
        sub3.plot(mm_light[2], mm_light[3], 'bo')

        print('soil:', mm_soil)
        sub4.plot(mm_soil[0], mm_soil[1], 'ro')
        sub4.plot(mm_soil[2], mm_soil[3], 'bo')

    plt.tight_layout()
    plt.show()


def plot_chart(day, with_min_max=False):
    assert isinstance(day, str), 'day must be a string'
    assert isinstance(with_min_max, bool), 'with_min_max must be True or False'

    try:
        plotting(read_data(day, with_min_max), with_min_max)
    except IndexError:
        print('\nno data for that day\n')


# plot_chart('2021-05-20', True)
# plot_chart('2021-01-01')
