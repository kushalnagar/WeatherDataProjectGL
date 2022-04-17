from model import UserModel, DeviceModel, WeatherDataModel
from datetime import datetime


# Shows how to initiate and search in the users collection based on a username
# Question 1.a Test Case 1 : No user passed - treated as non-admin
user_coll = UserModel()
user_document = user_coll.find_by_username('admin')
if (user_document):
    print(user_document)

# Shows a successful attempt on how to insert a user
user_document = user_coll.insert('test_3', 'test_3@example.com', 'default', ['DT003','DT004'], ['DT001'])
if (user_document == -1):
    print(user_coll.latest_error)
else:
    print(user_document)

# Test case for admin user insert
user_document = user_coll.insert('test_4', 'test_4@example.com', 'admin')
if (user_document == -1):
    print(user_coll.latest_error)
else:
    print(user_document)

# Question 1.a Test Case 2 : Non admin user passed
user_coll = UserModel('user_1')
user_document = user_coll.find_by_username('admin')
if (user_document):
    print(user_document)

# Shows a successful attempt on how to insert a user
user_document = user_coll.insert('test_3', 'test_3@example.com', 'default', ['DT003', 'DT004'], ['DT001'])
if (user_document == -1):
    print(user_coll.latest_error)
else:
    print(user_document)

# Test case for admin user insert
user_document = user_coll.insert('test_4', 'test_4@example.com', 'admin')
if (user_document == -1):
    print(user_coll.latest_error)
else:
    print(user_document)


# Question 1.a Test Case 3 : Admin user passed
user_coll = UserModel('admin')
user_document = user_coll.find_by_username('admin')
if (user_document):
    print(user_document)

# Shows a successful attempt on how to insert a user
user_document = user_coll.insert('test_3', 'test_3@example.com', 'default', ['DT003', 'DT004'], ['DT001'])
if (user_document == -1):
    print(user_coll.latest_error)
else:
    print(user_document)

# Test case for admin user insert
user_document = user_coll.insert('test_4', 'test_4@example.com', 'admin')
if (user_document == -1):
    print(user_coll.latest_error)
else:
    print(user_document)

# ----------------Device-----------------------------
# Shows how to initiate and search in the devices collection based on a device id
# Question 1.a - Test case 4 - Non-Admin case for device model
device_coll = DeviceModel('user_2')
device_document = device_coll.find_by_device_id('DT002')
if (device_document):
    print(device_document)

# Shows a successful attempt on how to insert a new device
device_document = device_coll.insert('DT201', 'Temperature Sensor', 'Temperature', 'Acme')
if (device_document == -1):
    print(device_coll.latest_error)
else:
    print(device_document)

# Question 1.a - Test case 5 - Admin case for device model
device_coll = DeviceModel('admin')
device_document = device_coll.find_by_device_id('DT002')
if (device_document):
    print(device_document)

# Shows a successful attempt on how to insert a new device
device_document = device_coll.insert('DT201', 'Temperature Sensor', 'Temperature', 'Acme')
if (device_document == -1):
    print(device_coll.latest_error)
else:
    print(device_document)

# --------------------------WeatherDataModel-----------------------------------
# Shows how to initiate and search in the weather_data collection based on a device_id and timestamp
wdata_coll = WeatherDataModel('user_1')
wdata_document = wdata_coll.find_by_device_id_and_timestamp('DT002', datetime(2020, 12, 2, 13, 30, 0))
if (wdata_document):
    print(wdata_document)

# Shows a failed attempt on how to insert a new data point
wdata_document = wdata_coll.insert('DT002', 12, datetime(2020, 12, 2, 13, 30, 0))
if (wdata_document == -1):
    print(wdata_coll.latest_error)
else:
    print(wdata_document)

wdata_coll = WeatherDataModel('user_2')
wdata_document = wdata_coll.find_by_device_id_and_timestamp('DT002', datetime(2020, 12, 2, 13, 30, 0))
if (wdata_document):
    print(wdata_document)

# Shows a failed attempt on how to insert a new data point
wdata_document = wdata_coll.insert('DT002', 12, datetime(2020, 12, 2, 13, 30, 0))
if (wdata_document == -1):
    print(wdata_coll.latest_error)
else:
    print(wdata_document)


# Admin case
wdata_coll = WeatherDataModel('admin')
wdata_document = wdata_coll.find_by_device_id_and_timestamp('DT002', datetime(2020, 12, 2, 13, 30, 0))
if (wdata_document):
    print(wdata_document)

# Shows a failed attempt on how to insert a new data point
wdata_document = wdata_coll.insert('DT002', 12, datetime(2020, 12, 2, 13, 30, 0))
if (wdata_document == -1):
    print(wdata_coll.latest_error)
else:
    print(wdata_document)