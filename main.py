import pandas
from matplotlib import pyplot


def ema(data, current_day, period):
    alfa = 2 / (period + 1)
    denominator = (1 - pow(1 - alfa, period)) / alfa

    nominator = 0
    power = 0
    last_day = current_day - period - 1

    for sample in range(current_day, last_day, -1):
        if type(data) is pandas.DataFrame:
            value = data.at[sample, 'Otwarcie'] # later change to 'Zamkniecie'
        else:
            value = data[sample - 1]
        nominator += value * pow(1 - alfa, power)
        power += 1

    return nominator / denominator


def main():
    data = pandas.read_csv('wig20_d.csv', usecols=['Otwarcie']) # later change to 'Zamkniecie'

    macd = []
    signal = []

    for sample_number in range(26, 1000):
        ema12 = ema(data, sample_number, 12)
        ema26 = ema(data, sample_number, 26)
        macd.append(ema12 - ema26)
        if len(macd) >= 9:
            signal.append(ema(macd, len(macd), 9))

    new_macd = macd[9:]
    pyplot.plot(list(range(len(new_macd))), new_macd)
    pyplot.plot(list(range(len(signal))), signal)
    pyplot.xlabel('Sample number')
    pyplot.ylabel('Opening')
    pyplot.title('MACD trading indicator')
    pyplot.show()


if __name__ == '__main__':
    main()