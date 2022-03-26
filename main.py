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


def plot(data, macd, signal, buys, sells):
    fig, (ax1, ax2) = pyplot.subplots(2)

    ax1.plot(macd, label='MACD')
    ax1.plot(signal, label='Signal')
    ax1.set_ylabel('Indicator')
    ax1.set_title('MACD trading indicator and input data')
    ax1.legend()

    ax2.plot(data)
    ax2.scatter(*zip(*buys), c='g', s=25, label='Buy')
    ax2.scatter(*zip(*sells), c='r', s=25, label='Sell')
    ax2.set_xlabel('Sample number')
    ax2.set_ylabel('Opening stock quotes')
    ax2.legend()

    pyplot.show()


def calc_macd_signal_data(entry):
    macd = []
    for sample_number in range(26, len(entry)):
        ema12 = ema(entry, sample_number, 12)
        ema26 = ema(entry, sample_number, 26)
        macd.append(ema12 - ema26)

    signal = []
    for sample_number in range(9, len(macd)):
        signal.append(ema(macd, sample_number, 9))

    return macd[9:], signal, entry[35:]


def calc_buys_sells(data, macd, signal):
    buys = []
    sells = []
    for i in range(len(macd)):
        if i + 1 < len(macd):
            if signal[i] > macd[i] and signal[i + 1] < macd[i + 1]:
                buys.append((i, data[i]))
            elif signal[i] < macd[i] and signal[i + 1] > macd[i + 1]:
                sells.append((i, data[i]))

    return buys, sells


def calc_profit(data, buys, sells):
    exchanges = []
    for buy in buys:
        exchanges.append((buy[0], buy[1], 1))
    for sell in sells:
        exchanges.append((sell[0], sell[1], 0))
    exchanges = sorted(exchanges, key=lambda tup: tup[0])

    capital = 1000
    wallet = 0

    for exchange in exchanges:
        if exchange[2] == 1:
            if wallet >= exchange[1]:
                how_many = int(wallet / exchange[1])
                wallet -= how_many * exchange[1]
                capital += how_many
        else:
            wallet += capital * exchange[1]
            capital = 0

    return (capital * data[len(data) - 1] + wallet) * 100 / (capital * data[0])


def main():
    entry = pandas.read_csv('wig20_d.csv')['Otwarcie'].values.tolist()

    macd, signal, data = calc_macd_signal_data(entry)
    buys, sells = calc_buys_sells(data, macd, signal)
    profit = calc_profit(data, buys, sells)

    print("Profit: " + "%.2f" % profit + "%")

    plot(data, macd, signal, buys, sells)


if __name__ == '__main__':
    main()
