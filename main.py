import pandas
from matplotlib import pyplot


def main():
    data = pandas.read_csv('wig20_d.csv', usecols=['Otwarcie'])  # later change to 'Zamkniecie'

    ema12 = data.ewm(span=12).mean()
    ema26 = data.ewm(span=26).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9).mean()


    pyplot.plot(macd, label='MACD')
    pyplot.plot(signal, label='Signal')
    pyplot.xlabel('Sample number')
    pyplot.ylabel('Opening')
    pyplot.title('MACD trading indicator')
    pyplot.legend()
    pyplot.show()


if __name__ == '__main__':
    main()
