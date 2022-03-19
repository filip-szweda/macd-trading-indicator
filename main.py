import pandas
import numpy
from matplotlib import pyplot


def ema(wig20, i, n):
    alfa = 2 / (n + 1)
    denominator = (1 - pow(1 - alfa, n)) / alfa
    nominator = 0
    power = 0

    if i - n < 0:
        bottomRange = 0
    else:
        bottomRange = i - n

    for sample in range(i + 1, bottomRange, -1):
        if type(wig20) is pandas.DataFrame:
            value = wig20.at[sample - 1, 'Najwyzszy']
        else:
            value = wig20[sample - 1]
        nominator += value * pow(1 - alfa, power)
        power += 1

    return nominator / denominator


def main():
    wig20 = pandas.read_csv('wig20_d.csv', usecols=['Najwyzszy'])

    ema12 = []
    ema26 = []
    macd = []
    signal = []

    for i in range(1000):
        ema12.append(ema(wig20, i, 12))
        ema26.append(ema(wig20, i, 26))
        macd.append(ema12[i] - ema26[i])
        signal.append(ema(macd, i, 9))

    pyplot.plot(list(range(1000)), macd)
    pyplot.plot(list(range(1000)), signal)
    pyplot.show()


if __name__ == '__main__':
    main()
