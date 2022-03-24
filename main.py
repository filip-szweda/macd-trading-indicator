import pandas
from matplotlib import pyplot


def main():
    data = pandas.read_csv('wig20_d.csv', usecols=['Otwarcie'])  # later change to 'Zamkniecie'

    ema12 = data.ewm(span=12).mean()
    ema26 = data.ewm(span=26).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9).mean()

    fig, (ax1, ax2) = pyplot.subplots(2)

    ax1.plot(data)
    ax1.set_ylabel('Opening exchange')
    ax1.set_title('Input data and MACD trading indicator')
    ax2.plot(macd, label='MACD')
    ax2.plot(signal, label='Signal')
    ax2.set_xlabel('Sample number')
    ax2.set_ylabel('Indicator')
    ax2.legend()

    pyplot.show()


if __name__ == '__main__':
    main()
