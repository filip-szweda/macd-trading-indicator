import pandas
from matplotlib import pyplot


def ema(data, current_sample, period):
    alpha = 2 / float(period + 1)
    last_sample = current_sample - period
    nominator = 0
    denominator = 0
    power = 0

    for sample in range(current_sample, last_sample, -1):
        denominator += pow(1 - alpha, power)
        nominator += data[sample] * pow(1 - alpha, power)
        power += 1

    if denominator == 0:
        return

    return nominator / denominator


def main():
    data = pandas.read_csv('wig20_d.csv')['Otwarcie'].values.tolist()

    macd = []
    for sample_number in range(25, len(data)):
        ema12 = ema(data, sample_number, 12)
        ema26 = ema(data, sample_number, 26)
        macd.append(ema12 - ema26)

    signal = []
    for sample_number in range(8, len(macd)):
        signal.append(ema(macd, sample_number, 9))

    fig, (ax1, ax2) = pyplot.subplots(2)

    data = data[35:]
    ax1.plot(data[35:])
    ax1.set_ylabel('Opening exchange')
    ax1.set_title('Input data and MACD trading indicator')

    macd = macd[9:]
    ax2.plot(macd[9:], label='MACD')
    ax2.plot(signal, label='Signal')
    ax2.set_xlabel('Sample number')
    ax2.set_ylabel('Indicator')
    ax2.legend()

    pyplot.show()


if __name__ == '__main__':
    main()
