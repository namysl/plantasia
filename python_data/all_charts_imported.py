import chart_bar as bar
import chart_plot as plot
import chart_pie as pie
import days_with_data as days
from colorama import init, Fore, Back, Style

available_columns = ['temp_c', 'air', 'light', 'soil']
available_charts = ['bar', 'plot', 'pie']

init(convert=True)

print('type in :q! to exit')
print('type in days to see dates with data')


def run_bar():
    column = input('column: ')

    if column not in available_columns:
        print(Back.RED + 'error, available data columns:', available_columns)
        print(Style.RESET_ALL)
        return None

    date1 = input('date1: ')
    date2 = input('date2: ')
    last_x_days = input('last_x_days: ')
    with_mean = input('with_mean: y/n? ')

    if with_mean == 'y':
        with_mean = True
    else:
        with_mean = False

    bar.bar_chart(column, date1, date2, int(last_x_days), with_mean)


def run_plot():
    date = input('date: ')
    with_min_max = input('with_min_max: y/n? ')

    if with_min_max == 'y':
        with_min_max = True
    else:
        with_min_max = False

    plot.plot_chart(date, with_min_max)


def run_pie():
    column = input('column: ')

    if column not in available_columns:
        print(Back.RED + 'error, available data columns:', available_columns)
        print(Style.RESET_ALL)
        return None

    day = input('day: ')

    pie.pie_chart(day, column)


def run_days():
    dates = days.unique_days()
    for x in range(0, len(dates), 7):
        print(' '.join(str(y) for y in dates[x:x+7]))
        print(Style.RESET_ALL)


def main():
    print(Fore.GREEN + '\navailable data columns:', available_columns)
    print(Fore.GREEN + 'available charts:', available_charts, '\n')
    print(Style.RESET_ALL)

    while True:
        chart_input = input('type of a chart: ')

        if chart_input == 'bar':
            run_bar()
        elif chart_input == 'plot':
            run_plot()
        elif chart_input == 'pie':
            run_pie()
        elif chart_input == 'days':
            run_days()
        elif chart_input == ':q!':
            exit()
        else:
            print(Back.RED + '\nerror, available types of charts:', available_charts)
            print(Back.RED + ':q! to exit or type in days to see dates with data\n')
            print(Style.RESET_ALL)


if __name__ == '__main__':
    main()
