import datetime

import requests
import numpy as np
import matplotlib.pyplot as plt


results = []
start = str(datetime.date.today() - datetime.timedelta(hours=4380))
API_URI = 'http://marsweather.ingenology.com/v1/archive/?terrestrial_date_start=%s' % start


def gather_payload(uri):
    r = requests.get(uri)
    if r.status_code != 200:
        return [], None

    payload = r.json()
    return payload['results'], payload['next']


def get_average(data, key):
    return np.mean([i[key] for i in data])


def plot_graph(data):
    fig, ax1 = plt.subplots()
    min_temp = [i.get('min_temp', 0) for i in data]
    max_temp = [i.get('max_temp', 0) for i in data]
    dates_range = [datetime.datetime.strptime(i.get('terrestrial_date'), '%Y-%m-%d') for i in data]
    ax1.plot(dates_range, min_temp, 'b-')

    ax1.set_xlabel('Time')
    ax1.set_ylabel('Minimum temperature', color='b')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')

    ax2 = ax1.twinx()
    ax2.plot(dates_range, max_temp, 'g')
    ax2.set_ylabel('Maximum temperature', color='g')
    for tl in ax2.get_yticklabels():
        tl.set_color('g')

    plt.title('Mars weather', loc='center')
    plt.title('Average min_temp: %.3f' % get_average(results, 'min_temp'), loc='left')
    plt.title('Average max_temp: %.3f' % get_average(results, 'max_temp'), loc='right')
    plt.show()

if __name__ == '__main__':
    while API_URI:
        res, API_URI = gather_payload(API_URI)
        results.extend(res)

    plot_graph(results)
