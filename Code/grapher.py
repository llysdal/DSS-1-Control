import matplotlib.pyplot as plt
import matplotlib as mpl

def showGraph(data, start):
    xtick = []
    for i in range(start, start+len(data), int(len(data)/16)):
        xtick.append(i)
    ytick = [-2048, -1024, 0, 1024, 2048]

    plt.figure(figsize = (15,3))

    plt.plot(data)
    plt.xticks(xtick)
    plt.yticks(ytick)
    plt.ylim(ymin = -2048, ymax = 2048)
    plt.xlim(xmin = 0, xmax = len(data))

    plt.ion()
    plt.show()


def saveGraph(name, data):
    pass