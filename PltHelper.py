import matplotlib.pyplot as plt
import numpy

def draw_xy(xs,ys, title=None):
    fig = plt.figure()
    plt.plot(xs,ys)
    # plt.axis("equal")

    if title is not None:
        plt.title(title)
    plt.rcParams['font.sans-serif'] = ['Kaitt', 'SimHei']
    plt.show()