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
    ax2.set_ylabel('Close stock quotes')
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
        if i + 2 < len(macd):
            if signal[i] > macd[i] and signal[i + 1] < macd[i + 1]:
                buys.append((i, data[i + 2]))
            elif signal[i] < macd[i] and signal[i + 1] > macd[i + 1]:
                sells.append((i, data[i + 2]))

    return buys, sells


def calc_end_actions_wallet(buys, sells, start_actions, start_wallet):
    exchanges = []
    for buy in buys:
        exchanges.append((buy[0], buy[1], True))
    for sell in sells:
        exchanges.append((sell[0], sell[1], False))
    exchanges = sorted(exchanges, key=lambda tup: tup[0])

    actions = start_actions
    wallet = start_wallet

    for exchange in exchanges:
        print("Sample #" + str(exchange[0]))
        print("\tWallet: " + "%.2f" % wallet + " Actions: " + str(actions))
        if exchange[2]:
            if wallet >= exchange[1]:
                how_many = int(wallet / exchange[1])
                wallet -= how_many * exchange[1]
                actions += how_many
                print("\tBuying " + str(how_many) + " actions")
            else:
                print("\tCan't buy")
        else:
            if actions > 0:
                wallet += actions * exchange[1]
                print("\tSelling " + str(actions) + " actions")
                actions = 0
            else:
                print("\tCan't sell")

    return actions, wallet


def main():
    entry = pandas.read_csv('wig20_d.csv')['Zamkniecie'].values.tolist()

    macd, signal, data = calc_macd_signal_data(entry)
    buys, sells = calc_buys_sells(data, macd, signal)

    start_actions = 1000
    start_wallet = 0
    start_capital = start_actions * data[0] + start_wallet

    end_actions, end_wallet = calc_end_actions_wallet(buys, sells, start_actions, start_wallet)
    end_capital = end_actions * data[len(data) - 1] + end_wallet

    print("Start capital: " + str(start_actions) + " * " + "%.2f" % data[
        0] + " + " + "%.2f" % start_wallet + " = " + "%.2f" % start_capital)
    print("End capital: " + str(end_actions) + " * " + "%.2f" % data[
        len(data) - 1] + " + " + "%.2f" % end_wallet + " = " + "%.2f" % end_capital)

    profit = end_capital - start_capital
    profit_percent = 100 - start_capital * 100 / end_capital

    print("Total profit: " + "%.2f" % profit + " or " + "%.2f" % profit_percent + "%")

    plot(data, macd, signal, buys, sells)


if __name__ == '__main__':
    main()
