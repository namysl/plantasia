import pandas as pd


def unique_days():
    plant = pd.read_csv('example_plant_data.csv')

    days = plant.date.unique().tolist()
    return days
