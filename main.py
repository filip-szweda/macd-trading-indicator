import pandas
from matplotlib import pyplot


def ema(data, current_day, period):
    alfa = 2 / (period + 1)
    denominator = (1 - pow(1 - alfa, period)) / alfa

    if current_day - period < 0:
        last_day = -1
    else:
        last_day = current_day - period - 1

    nominator = 0
    power = 0

    for sample in range(current_day, last_day, -1):
        if type(data) is pandas.DataFrame:
            value = data.at[sample, 'Otwarcie'] # later change to 'Zamkniecie'
        else:
            value = data[sample]
        nominator += value * pow(1 - alfa, power)
        power += 1

    return nominator / denominator


def main():
    data = pandas.read_csv('wig20_d.csv', usecols=['Otwarcie']) # later change to 'Zamkniecie'

    ema12 = []
    ema26 = []
    macd = []
    signal = []

    for i in range(1000):
        ema12.append(ema(data, i, 12))
        ema26.append(ema(data, i, 26))
        macd.append(ema12[i] - ema26[i])
        signal.append(ema(macd, i, 9))

    pyplot.plot(list(range(1000)), macd)
    pyplot.plot(list(range(1000)), signal)
    pyplot.xlabel('Sample number')
    pyplot.ylabel('Opening')
    pyplot.title('MACD trading indicator')
    pyplot.show()


if __name__ == '__main__':
    main()
