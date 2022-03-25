import pandas
from matplotlib import pyplot


def ema(data, current_sample, period):
    alpha = 2 / float(period + 1)
    last_sample = current_sample - period - 1
    nominator = 0
    denominator = 0
    power = 0

    for sample in range(current_sample, last_sample, -1):
        value = pow(1 - alpha, power)
        denominator += value
        nominator += data[sample] * value
        power += 1

    return nominator / denominator


def main():
    data = pandas.read_csv('wig20_d.csv')['Otwarcie'].values.tolist()

    macd = []
    for sample_number in range(26, len(data)):
        ema12 = ema(data, sample_number, 12)
        ema26 = ema(data, sample_number, 26)
        macd.append(ema12 - ema26)

    signal = []
    for sample_number in range(9, len(macd)):
        signal.append(ema(macd, sample_number, 9))

    data = data[35:]
    macd = macd[9:]
    buy = []
    sell = []
    for i in range(len(macd)):
        if i + 1 < len(macd):
            if signal[i] > macd[i] and signal[i + 1] < macd[i + 1]:
                buy.append((i, data[i]))
            elif signal[i] < macd[i] and signal[i + 1] > macd[i + 1]:
                sell.append((i, data[i]))

    fig, (ax1, ax2) = pyplot.subplots(2)

    ax1.plot(macd, label='MACD')
    ax1.plot(signal, label='Signal')
    ax1.set_ylabel('Indicator')
    ax1.set_title('MACD trading indicator and input data')
    ax1.legend()

    ax2.plot(data)
    ax2.scatter(*zip(*buy), c='g', label='Buy')
    ax2.scatter(*zip(*sell), c='r', label='Sell')
    ax2.set_xlabel('Sample number')
    ax2.set_ylabel('Opening stock quotes')
    ax2.legend()

    pyplot.show()


if __name__ == '__main__':
    main()
