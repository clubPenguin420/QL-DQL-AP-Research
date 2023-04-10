import matplotlib.pyplot as plt
import json

data = {}

with open("graphing_data4.json", "r") as file:
    data = json.load(file)
file.close()
x_axis = list(data)
y_axis = []

for i in range(1, 25001):
    y_axis.append(data[str(i)][0])


plt.plot(x_axis[:25000:100], y_axis[:25000:100])

plt.xlabel('Episode #')

plt.ylabel('Maze Wins')
  
plt.title('Cumulative Maze Wins')

plt.xticks(x_axis[:25000:1000])

plt.show()