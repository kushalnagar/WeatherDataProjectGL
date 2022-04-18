from datetime import datetime
from sqlite3 import Date

import constants
# Imports Database class from the project to provide basic functionality for database access
from database import Database
# Imports ObjectId to convert to the correct format before querying in the db
from bson.objectid import ObjectId

# User document contains username (String), email (String), and role (String) fields
class UserModel:
    USER_COLLECTION = 'users'

    def __init__(self, username=None):
        self._db = Database()
        self._latest_error = ''
        self._username = username
        self._isAdmin = True
        self._user = self.find_by_username(username)
        if self._user is not None:
            self._isAdmin = True if self._user.get(constants.ROLE) == constants.ADMIN else False
        else:
            self._isAdmin = False

    def is_user_admin(self):
        #temp = self._isAdmin
        #self._isAdmin = True
        #user = self.find_by_username(username)
        #self._isAdmin = temp
        #if (user != None):
        #    return True if self._user.get(constants.ROLE) == constants.ADMIN else False
        #else:
        #    return False
        return self._isAdmin

    def get_read_accessed_devices(self):
        devices = set(self._user.get('devices').get('rw'))
        devices.update(self._user.get('devices').get('r'))
        return devices

    def get_write_accessed_devices(self):
        devices = set(self._user.get('devices').get('rw'))
        return devices

    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Since username should be unique in users collection, this provides a way to fetch the user document based on the username
    def find_by_username(self, username):
        key = {'username': username}
        return self.__find(key)
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        if not self._isAdmin:
            print(f'Search operation on user not allowed for {self._username}!')
            return
        user_document = self._db.get_single_data(UserModel.USER_COLLECTION, key)
        return user_document
    
    # This first checks if a user already exists with that username. If it does, it populates latest_error and returns -1
    # If a user doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, username, email, role, rwdevices=None, rdevices=None):
        self._latest_error = ''

        if(self._isAdmin == False):
            print(f'Insert operation on user not allowed for {self._username}!')
            return

        user_document = self.find_by_username(username)
        if (user_document):
            self._latest_error = f'Username {username} already exists'
            return -1

        user_data = {'username': username, 'email': email, 'role': role,
                         'devices': {'rw': rwdevices, 'r': rdevices}}
        user_obj_id = self._db.insert_single_data(UserModel.USER_COLLECTION, user_data)
        return self.find_by_object_id(user_obj_id)


# Device document contains device_id (String), desc (String), type (String - temperature/humidity) and manufacturer (String) fields
class DeviceModel:
    DEVICE_COLLECTION = 'devices'

    def __init__(self, username=None):
        self._db = Database()
        self._latest_error = ''
        self._username = username
        if(username != None):
            self._userModel = UserModel(username)
            self._isAdmin = self._userModel.is_user_admin()
        else:
            self._isAdmin = False
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Since device id should be unique in devices collection, this provides a way to fetch the device document based on the device id
    def find_by_device_id(self, device_id):
        key = {'device_id': device_id}
        return self.__find(key)
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        devices = self._userModel.get_read_accessed_devices()
        device_document = self._db.get_single_data(DeviceModel.DEVICE_COLLECTION, key)
        if self._isAdmin or (device_document is not None and device_document.get('device_id') in devices):
            return device_document
        else:
            print(f'Search operation on device not allowed for {self._username}!')
    
    # This first checks if a device already exists with that device id. If it does, it populates latest_error and returns -1
    # If a device doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, device_id, desc, type, manufacturer):
        self._latest_error = ''

        if (self._isAdmin == False):
            print(f'Insert operation on device not allowed for {self._username}!')
            return -1

        device_document = self.find_by_device_id(device_id)
        if device_document:
            self._latest_error = f'Device id {device_id} already exists'
            return -1
        
        device_data = {'device_id': device_id, 'desc': desc, 'type': type, 'manufacturer': manufacturer}
        device_obj_id = self._db.insert_single_data(DeviceModel.DEVICE_COLLECTION, device_data)
        return self.find_by_object_id(device_obj_id)


# Weather data document contains device_id (String), value (Integer), and timestamp (Date) fields
class WeatherDataModel:
    WEATHER_DATA_COLLECTION = 'weather_data'

    def __init__(self, username=None):
        self._db = Database()
        self._latest_error = ''
        self._username = username
        if username != None:
            self._userModel = UserModel(username)
            self._isAdmin = self._userModel.is_user_admin()
        else:
            self._isAdmin = False
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Since device id and timestamp should be unique in weather_data collection, this provides a way to fetch the data document based on the device id and timestamp
    def find_by_device_id_and_timestamp(self, device_id, timestamp):
        key = {'device_id': device_id, 'timestamp': timestamp}
        return self.__find(key)
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        devices = self._userModel.get_read_accessed_devices()
        wdata_document = self._db.get_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, key)
        if self._isAdmin or (wdata_document is not None and wdata_document.get('device_id') in devices):
            return wdata_document
        else:
            print(f'Search operation on weather data with given criteria not allowed for {self._username}!')
    
    # This first checks if a data item already exists at a particular timestamp for a device id. If it does, it populates latest_error and returns -1.
    # If it doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, device_id, value, timestamp):
        self._latest_error = ''
        devices = self._userModel.get_write_accessed_devices()
        if self._isAdmin == False and device_id not in devices:
            print(f'Insert operation on weather data not allowed for {self._username}!')
            return -1
        wdata_document = self.find_by_device_id_and_timestamp(device_id, timestamp)
        if (wdata_document):
            self._latest_error = f'Data for timestamp {timestamp} for device id {device_id} already exists'
            return -1
        
        weather_data = {'device_id': device_id, 'value': value, 'timestamp': timestamp}
        wdata_obj_id = self._db.insert_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, weather_data)
        return self.find_by_object_id(wdata_obj_id)

    def get_aggregated_date(self):
        pipeline4 = [
		{
			'$group': {'_id': {
								'device_id': '$device_id',
								'day': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$timestamp'}},
								},
							'avg_value': {"$avg": "$value"},
							'min_value': {"$min": "$value"},
							'max_value': {"$max": "$value"},
							'total_count': {"$sum": 1}
						}
		},
		{
			'$project': {
				'device_id': '$_id.device_id',
				'date': '$_id.day',
				'avg': '$avg_value',
                'min': '$min_value',
                'max': '$max_value',
				'count': '$total_count',
				'_id': 0
				}
			}
	    ]
        return self._db.aggregate_data(WeatherDataModel.WEATHER_DATA_COLLECTION,pipeline4)

class DailyReportModel:
    DAILY_REPORT_DATA_COLLECTION = 'daily_report_data'

    def __init__(self, username=None):
        self._db = Database()
        self._latest_error = ''
        self._username = username
        if username != None:
            self._userModel = UserModel(username)
            self._isAdmin = self._userModel.is_user_admin()
        else:
            self._isAdmin = False

    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)

    def __find(self, key):
        #devices = self._userModel.get_read_accessed_devices()
        drdata_document = self._db.get_single_data(DailyReportModel.DAILY_REPORT_DATA_COLLECTION, key)
        #if self._isAdmin or (wdata_document is not None and wdata_document.get('device_id') in devices):
        return drdata_document
        #else:
        #    print(f'Search operation on weather data with given criteria not allowed for {self._username}!')

    def __find_all(self, key):
        #devices = self._userModel.get_read_accessed_devices()
        drdata_document = self._db.get_multiple_data(DailyReportModel.DAILY_REPORT_DATA_COLLECTION, key)
        #if self._isAdmin or (wdata_document is not None and wdata_document.get('device_id') in devices):
        return drdata_document

    # find by device id and date range inclusive
    def find_by_device_id_date_range(self, device_id, fromdate, todate):
        devices = self._userModel.get_read_accessed_devices()
        key = {'device_id': device_id, 'date': {'$gte': fromdate}, 'date': {'$lte': todate}}
        if self._isAdmin or (device_id in devices):
            return self.__find_all(key)
        else:
            print(f'Search operation on daily report data with given criteria not allowed for {self._username}!')

    def insert(self, device_id, date, average, minimum, maximum, count):
        self._latest_error = ''
        devices = self._userModel.get_write_accessed_devices()
        if self._isAdmin == False and device_id not in devices:
            print(f'Insert operation on daily report data not allowed for {self._username}!')
            return -1
        #wdata_document = self.find_by_device_id_and_timestamp(device_id, day)
        #if (wdata_document):
        #    self._latest_error = f'Data for timestamp {day} for device id {device_id} already exists'
        #    return -1

        daily_report_data = {'device_id': device_id, 'date': date, 'average': average, 'minimum': minimum, 'maximum': maximum, 'count': count}
        daily_report_obj_id = self._db.insert_single_data(DailyReportModel.DAILY_REPORT_DATA_COLLECTION, daily_report_data)
        return self.find_by_object_id(daily_report_obj_id)

    def drop(self):
        self._db.drop_collection(DailyReportModel.DAILY_REPORT_DATA_COLLECTION)

    def create_daily_report_bulk_entries(self):
        self._latest_error = ''
        if self._isAdmin == False:
            print(f'Bulk operation on daily report data data not allowed for {self._username}!')
            return -1

        self.drop()

        weatherDataModel = WeatherDataModel(self._username)
        entries = weatherDataModel.get_aggregated_date()
        bulk_data = []
        for entry in entries:
            date = datetime.strptime(entry.get('date'),'%Y-%m-%d')
            data = {'device_id': entry.get('device_id'),
                    'date': date,
                    'average': entry.get('avg'),
                    'minimum': entry.get('min'),
                    'maximum': entry.get('max'),
                    'count': entry.get('count')}
            bulk_data.append(data)

        self._db.insert_multiple(DailyReportModel.DAILY_REPORT_DATA_COLLECTION, bulk_data)