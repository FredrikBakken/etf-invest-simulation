
import matplotlib.pyplot as plt

from datetime import date, datetime, timedelta

from database import select_db

def rate_etfs(etf_ticker, method):
    # Variables
    monthly_investment = 500
    check_dates = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
    results = []
    d1 = []
    d2 = []
    all_ds = []
    all_dd = []
    difference_list = 0

    # Getting all historical values for etf
    data = select_db(etf_ticker)

    # Setting the time frame
    s_date = str(data[-1][0])
    first_date = datetime(year=int(s_date[0:4]), month=int(s_date[4:6]), day=int(s_date[6:8]))
    today_date = datetime.today()

    # Preparing dates for loop
    d1 = date(first_date.year, first_date.month, first_date.day)
    d2 = date(today_date.year, today_date.month, today_date.day)
    delta = d2 - d1


    # Rating method selection
    if method == 'trade_days':
        trade_days(method, check_dates, d1, delta, data, monthly_investment, etf_ticker, results)
    elif method == 'weekends':
        weekends(method, check_dates, d1, delta, all_ds, all_dd, data, monthly_investment, etf_ticker, results)
    else:
        print('That method does not exist.')


# Rating based on the specified date being a trade date
def trade_days(method, check_dates, d1, delta, data, monthly_investment, etf_ticker, results):
    # Loop through designated dates
    for x in range(len(check_dates)):
        counter = 0
        number_of_etfs = 0.00
        for i in range(delta.days + 1):
            all_dates = '%04d%02d%02d' % ((d1 + timedelta(days=i)).year, (d1 + timedelta(days=i)).month, (d1 + timedelta(days=i)).day)
            for j in range(len(data)):
                if all_dates == str(data[j][0]):
                    number = 0.00
                    checking_date = '%02d' % (data[j][0] % 100)
                    if checking_date == check_dates[x]:
                        number = monthly_investment / data[j][4]
                        number_of_etfs = number_of_etfs + number
                        print(etf_ticker + ' ' + check_dates[x] + ' ' + str(data[j][0]))
                        counter = counter + 1

        total_val = number_of_etfs
        avg_total = total_val / counter

        total = [check_dates[x], avg_total, counter]
        results.append(total)

    sorted_list = sorted(results, key=lambda x: x[1], reverse=True)

    plot_results(method, sorted_list, check_dates, etf_ticker)


# Rating based on trade days and weekends, if date is a weekend => Trade on the next tradeable day
def weekends(method, check_dates, d1, delta, all_ds, all_dd, data, monthly_investment, etf_ticker, results):

    # List all dates between start and end
    for i in range(delta.days + 1):
        all_ds.append('%04d%02d%02d' % ((d1 + timedelta(days=i)).year, (d1 + timedelta(days=i)).month, (d1 + timedelta(days=i)).day))

    # List all active trading dates
    for j in range(len(data)):
        all_dd.append(str(data[j][0]))

    # Find dates where no trades has happened
    difference_list = sorted(list(set(all_ds).difference(all_dd)))


    # Go through dates and start rating
    for x in range(len(check_dates)):
        counter = 0
        number_of_etfs = 0.00
        previous_trade = []

        for i in range(len(all_ds)):
            for j in range(len(difference_list)):
                dl = int(difference_list[j])
                checking_date = '%02d' % (dl % 100)

                if check_dates[x] == checking_date:
                    if all_ds[i] == difference_list[j]:
                        try:
                            if all_ds[i + 1] in all_dd:
                                previous_trade.append(all_ds[i + 1])
                            elif all_ds[i + 2] in all_dd:
                                previous_trade.append(all_ds[i + 2])
                            elif all_ds[i + 3] in all_dd:
                                previous_trade.append(all_ds[i + 3])
                            elif all_ds[i + 4] in all_dd:
                                previous_trade.append(all_ds[i + 4])
                            elif all_ds[i + 5] in all_dd:
                                previous_trade.append(all_ds[i + 5])
                            elif all_ds[i + 6] in all_dd:
                                previous_trade.append(all_ds[i + 6])
                            elif all_ds[i + 7] in all_dd:
                                previous_trade.append(all_ds[i + 7])
                        except:
                            print('Date does not exist.')

            for j in range(len(data)):
                if all_ds[i] == str(data[j][0]):
                    number = 0.00
                    checking_date = '%02d' % (data[j][0] % 100)
                    if checking_date == check_dates[x]:
                        number = monthly_investment / data[j][4]
                        number_of_etfs = number_of_etfs + number
                        counter = counter + 1


                for k in range(len(previous_trade)):
                    if previous_trade[k] == str(data[j][0]):
                        number = monthly_investment / data[j][4]
                        number_of_etfs = number_of_etfs + number
                        counter = counter + 1
                        print(etf_ticker + ' ' + check_dates[x] + ' ' + previous_trade[k])
                        previous_trade.remove(str(data[j][0]))


        total_val = number_of_etfs
        avg_total = 0
        try:
            avg_total = total_val / counter
        except:
            print(etf_ticker + ' does not work.')

        total = [check_dates[x], avg_total, counter]
        results.append(total)

    sorted_list = sorted(results, key=lambda x: x[1], reverse=True)

    plot_results(method, sorted_list, check_dates, etf_ticker)


# Plot the results into a graph
def plot_results(method, sorted_list, check_dates, etf_ticker):
    avg = 0.00

    for i in range(len(sorted_list)):
        print('Date of month: ' + sorted_list[i][0] + ', and average number of etf-stocks per. month: {0:.6f}'.format(
            sorted_list[i][1]) + ', number of total trades: ' + str(sorted_list[i][2]))

        x = float(sorted_list[i][0])
        y = float(sorted_list[i][1])

        avg = avg + float(sorted_list[i][1])

        plt.scatter(x, y)

    avg = (avg / len(check_dates))

    plt.axhline(y=avg, xmin=0, xmax=1, hold=None)
    plt.savefig('data/results/' + method + '/' + etf_ticker + '.png')

    plt.show()

    return True