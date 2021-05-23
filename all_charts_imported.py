import chart_bar as bar
import chart_plot as plot
import chart_pie as pie
import days_with_data as days


print('type in :q! to exit')
print('type in days to see dates with data')

while True:
    print('\navailable data columns: temp_c, air, light, soil')
    print('available charts: bar, plot, pie\n')
    
    chart_input = input('type of chart: ')

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
                
    elif chart_input == ':q!':
        exit()
    else:
        print('\nerror, available types of charts: bar, plot, pie')
        print('or :q! to exit\n')