import h5py
import pytz
import datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt

FILENAME = "1541962108935000000_167_838.h5"
file = h5py.File(FILENAME, 'r')

utcTimeStamp = datetime.datetime.utcfromtimestamp(int(FILENAME[0:10]) + float("."+FILENAME[10:19]))
utcTime = utcTimeStamp # .strftime("%Y-%m-%d %H:%M:%S")
cernTime = pytz.timezone("Europe/Zurich").fromutc(utcTimeStamp) # .strftime("%Y-%m-%d %H:%M:%S")

print("Task 1:")
print(utcTime)
print(cernTime)
print("")

print("Task 2:")
print("Wait...")

with open("path.csv", "w") as f:
        f.truncate()
        f.write("Path,DataType,Size,Shape"+"\n")

def appendToCSV(string, clear):
    with open("path.csv", "a") as f:
        f.write(string + "\n")

def recurExplore(name, Object):
    string = name
    if isinstance(Object, h5py.Dataset):
        try:
            string += Object.dtype.__str__()+"," + Object.size.__str__()+"," + Object.shape.__str__()
        except TypeError:
            # print("Dataset not NumPy compatible.")
            string += ",Uncompatible DataType,,"
    else:
        string += ",,,"
    appendToCSV(string, False)

file.visititems(recurExplore)
print("Done!\n")

print("Task 3:")
image1D = np.array(file["/AwakeEventData/XMPP-STREAK/StreakImage/streakImageData"])
height = list(file["/AwakeEventData/XMPP-STREAK/StreakImage/streakImageHeight"])[0]
width = list(file["/AwakeEventData/XMPP-STREAK/StreakImage/streakImageWidth"])[0]
image2D = np.reshape(image1D, (height, width))
finalImage = medfilt(image2D)

plt.imshow(finalImage)
plt.savefig("image.png")
