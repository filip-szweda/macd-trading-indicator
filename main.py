import pandas
from matplotlib import pyplot


def eman(data, current_day, period):
    alpha = 2 / float(period + 1)
    nominator = 0
    denominator = 0
    power = 0
    last_day = current_day - period - 1

    for sample in range(current_day, last_day, -1):
        if type(data) is pandas.DataFrame:
            value = data.at[sample]
        else:
            value = data[sample - 1]
        denominator += pow(1 - alpha, power)
        nominator += value * pow(1 - alpha, power)
        power += 1

    if denominator == 0:
        return

    return nominator / denominator


def ema(data, current_day, period):
    alpha = 2 / float(period + 1)
    nominator = 0
    denominator = 0
    power = 0
    last_day = current_day - period - 1

    for sample in range(current_day, last_day, -1):
        if type(data) is pandas.DataFrame:
            value = data.at[sample]
        else:
            value = data[sample - 1]
        denominator += pow(1 - alpha, power)
        nominator += value * pow(1 - alpha, power)
        power += 1

    if denominator == 0:
        return

    return nominator / denominator


def main():
    data = pandas.read_csv('wig20_d.csv', usecols=['Otwarcie']).values

    macd = []
    signal = []

    for sample_number in range(26, 1000):
        ema12 = ema(data, sample_number, 12)
        ema26 = ema(data, sample_number, 26)
        macd.append(ema12 - ema26)
        if len(macd) >= 9:
            signal.append(ema(macd, len(macd), 9))

    fig, (ax1, ax2) = pyplot.subplots(2)

    ax1.plot(data.tolist()[35:])
    ax1.set_ylabel('Opening exchange')
    ax1.set_title('Input data and MACD trading indicator')

    ax2.plot(macd[9:], label='MACD')
    ax2.plot(signal, label='Signal')
    ax2.set_xlabel('Sample number')
    ax2.set_ylabel('Indicator')
    ax2.legend()

    pyplot.show()


if __name__ == '__main__':
    main()
