# import csv

# with open("weather_data.csv", "r") as weather_file:
#     data = csv.reader(weather_file)
#     temperatures = []
#     for row in data:
#         if row[1] != "temp":
#             temperatures.append(int(row[1]))
#     print(temperatures)

import pandas

data = pandas.read_csv("weather_data.csv")
# print(data["temp"])

data_dict = data.to_dict()
# print(data_dict)

temp_list = data["temp"].to_list()
# print(temp_list)

average = data["temp"].mean()
# print(average)

maxTemp = data["temp"].max()
# print(maxTemp)
index = data[data.temp == maxTemp].index
# print(index)

monday = data[data.day == "Monday"]
monday_temperature_Fah = monday.temp * 9 / 5 + 32
# print(monday_temperature_Fah)

# Create a data frame from scratch
data_dict = {
    "students": ["Amy", "James", "Angela"],
    "scores": [76, 56, 65]
}

dataP = pandas.DataFrame(data_dict)
# print(dataP)
dataP.to_csv("data.csv")

#
# Central Park squirrel census
#

squirrel_data = pandas.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data_20260130.csv")

# squirrel_list = squirrel_data["Primary Fur Color"].to_list()
#
# grey_color = squirrel_list.count('Gray')
# red_color = squirrel_list.count('Cinnamon')
# black_color = squirrel_list.count('Black')
grey_color = len(squirrel_data[squirrel_data["Primary Fur Color"] == "Gray"])
red_color = len(squirrel_data[squirrel_data["Primary Fur Color"] == "Cinnamon"])
black_color = len(squirrel_data[squirrel_data["Primary Fur Color"] == "Black"])

squirrel_dict = {
    "Fur Color": ["grey", "red", "black"],
    "Count": [grey_color, red_color, black_color]
}

squirrel_count = pandas.DataFrame(squirrel_dict)
squirrel_count.to_csv("squirrel_count.csv")