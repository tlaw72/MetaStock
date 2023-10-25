import pandas as pd
import matplotlib.pyplot as plt


stock_data_file = "METAStockPrices.csv"

def loadData(file):
    return pd.read_csv(file)


def findAvgCloseByMonth(df):
    df['Date'] = pd.to_datetime(df["Date"]).dt.strftime('%Y-%m')
    df_avg = df.groupby('Date')['Close'].mean().reset_index(name='Average_Close')
    return df_avg

def plotAvgs(df):
    df.plot(kind='scatter', x="Date", y="Average_Close", title='Avg monthly META stock closing price')

    plt.savefig('monthlyStockAvg.png')
    plt.show()
    # df.plot()

def main():
    df = loadData(stock_data_file)
    df = findAvgCloseByMonth(df)
    print(df.head())
    plotAvgs(df)

main()