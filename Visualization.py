import pandas as pd
from matplotlib import pyplot as plt

class Visualization():
    df = pd.read_excel("data.xlsx")
    # plt.plot(df.xleft,df.yleft)
    # plt.plot(df.xright,df.yright)
    plt.plot((df.xleft+df.yleft)/2,(df.xright+df.yright)/2)
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.legend(['Left Eye','Right Eye'])
    plt.show()
    print(df.head())