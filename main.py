import pandas
import pandas as pd


def ema(wig20, i, N):
    alfa = 2 / (N + 1)
    denominator = (1 - pow(1 - alfa, N)) / alfa
    nominator = 0
    power = N
    if i - N >= 0:
        for sample in range(i - N, i):
            nominator += wig20.at[sample, 0] * pow(1 - alfa, power)
            power -= 1
    else:
        for sample in range(0, i):
            nominator += wig20.at[sample, 0] * pow(1 - alfa, power)
            power -= 1
    return nominator / denominator


def main():
    wig20 = pandas.read_csv('wig20_d.csv', usecols=['Najwyzszy'])
    ema9 = []
    ema12 = []
    ema26 = []
    for i in range(1000):
        ema9.append(ema(wig20, i, 9))
        ema12.append(ema(wig20, i, 12))
        ema26.append(ema(wig20, i, 26))


if __name__ == '__main__':
    main()
