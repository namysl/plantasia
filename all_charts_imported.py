import chart_bar as bar
import chart_plot as plot
import chart_pie as pie
import days_with_data as days
from colorama import init, Fore, Back, Style

init(convert=True)

print('type in :q! to exit')
print('type in days to see dates with data')

while True:
    print(Fore.GREEN + '\navailable data columns: temp_c, air, light, soil')
    print(Fore.GREEN + 'available charts: bar, plot, pie\n')

    print(Style.RESET_ALL)
    chart_input = input('type of a chart: ')

    if chart_input == 'bar':
        column = input('column: ')
        date1 = input('date1: ')
        date2 = input('date2: ')
        last_x_days = input('last_x_days: ')
        with_mean = input('with_mean: ')

        bar.bar_chart(column, date1, date2, int(last_x_days), bool(with_mean))

    elif chart_input == 'plot':
        date = input('date: ')
        with_min_max = input('with_min_max: ')

        plot.plot_chart(date, bool(with_min_max))

    elif chart_input == 'pie':
        day = input('day: ')
        column = input('column: ')

        pie.pie_chart(day, column)

    elif chart_input == 'days':
        dates = days.unique_days()
        print(', '.join(dates))
        print(Style.RESET_ALL)
                
    elif chart_input == ':q!':
        exit()
        
    else:
        print(Back.RED + '\nerror, available types of charts: bar, plot, pie')
        print(Back.RED + 'or :q! to exit\n')
        print(Style.RESET_ALL)
