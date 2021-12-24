from google.transit import gtfs_realtime_pb2
import requests
import time
from datetime import datetime
from dotenv import dotenv_values

config = dotenv_values("modify.env") 

# The get train times function takes a station ID on the BDFM line and an API Key and returns two lists of tuples one containing the 
#   arrival times of all north bound trains and the other containing the arrival times of all south bound trains.
def get_train_times(station_id, api_key) -> list:
    headers = {"x-api-key": api_key}
    endpoint = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm"
    train_times_north = []
    train_times_south = []
    # set up request for train times, retreive GTFS data from NYC MTA.
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(endpoint, headers=headers)
    feed.ParseFromString(response.content)

    # parse the northbound and southbound arrival times from the GTFS feed.
    for entity in feed.entity:
        for data in entity.trip_update.stop_time_update:
            if data.stop_id == (station_id+"N"):
                train_times_north.append((data.stop_id, time.strftime('%H:%M:%S', time.localtime(data.arrival.time))))
            if data.stop_id == (station_id+"S"):
                train_times_south.append((data.stop_id, time.strftime('%H:%M:%S', time.localtime(data.arrival.time))))
    
    return(train_times_north, train_times_south)

# this function determines the next train sofia can make and the time she would have to leave to make the following 3 trains.
def sofia_to_work() -> str:
    num_trains = 0
    time_to_walk = config['WALK_TIME'] #13 minute walk to subway. @to-do -> add integration with google maps distance api to determine current walk time.
    north_bound_arrivals, south_bound_arrivals = get_train_times(config['STOP'], config['API_KEY'])

    for each in north_bound_arrivals:
        # update datetime obj from GTFS data to allow for comparison.
        datetime_object = datetime.strptime(each[1], '%H:%M:%S')
        datetime_object = datetime_object.replace(year=datetime.now().year, day=datetime.now().day, month=datetime.now().month)
        current_time_obj = datetime.now()

        if current_time_obj.minute + int(time_to_walk) > 59:
            current_time_obj = current_time_obj.replace(hour=current_time_obj.hour+1, minute=(current_time_obj.minute+time_to_walk)-60)
        else:
            current_time_obj = current_time_obj.replace(minute=(current_time_obj.minute+int(time_to_walk)))

        if current_time_obj >= datetime_object:
            continue
        elif num_trains == 0:
            print("The next available train is at:\n",str(datetime_object.hour)+":"+str(datetime_object.minute))
            print("After that the next arrivals are at:")
            num_trains+=1
        else:
            if num_trains < 4:
                print(" "+str(datetime_object.hour)+":"+str(datetime_object.minute))
                num_trains+=1
            else:
                break

while (1):
    sofia_to_work()
    print("\n~~~~~~~~~~~~\n")
    time.sleep(60)