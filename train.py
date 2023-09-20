import requests
from bs4 import BeautifulSoup
import re

from flask import Flask, request, jsonify
#from your_train_status_scraping_script import getLiveTrainStatus  # Replace with the actual name of your scraping script

app = Flask(__name__)

@app.route('/train-status', methods=['GET'])
def train_status():
    try:
        train_no = request.args.get('trainNo')
        date = request.args.get('date')
        data = getLiveTrainStatus(trainNo=train_no, date=date)
        return jsonify({'status': 'success', 'data': data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


def getLiveTrainStatus(trainNo,date):
    response = requests.get(f"https://www.confirmtkt.com/train-running-status/{trainNo}?Date={date}")
    print(f"https://www.confirmtkt.com/train-running-status/{trainNo}?Date={date}")

    soup = BeautifulSoup(response.text, 'html.parser')
    journey_wrapper = soup.find_all('div', attrs={"class": "journey-wrapper"})[0]
    #print(journey_wrapper)
    running_status = journey_wrapper.find_all("div", attrs={"class":"running-status"})[0]

    soup = BeautifulSoup(str(running_status), 'html.parser')
    data_list = []
    div_elements = soup.find_all('div', class_='well well-sm')

    for div in div_elements:
        current = False
        if div.find('div', class_='circle blink') is not None:
            current = True
        station_name = div.find('span', class_='rs__station-name').text.strip()
        date = div.find_all('span')[2].text.strip()
        departure_time = div.find_all('span')[4].text.strip()
        arrival_time = div.find_all('span')[3].text.strip()
        status = div.find('div', class_='rs__station-delay').text.strip()

        station_data = {
            'Station Name': station_name,
            'current': current,
            'Date': date,
            'Departure Time': departure_time,
            'Arrival Time': arrival_time,
            'Status': status
        }

        data_list.append(station_data)
        #print(station_data)
    return data_list

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
