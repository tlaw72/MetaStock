import pandas as pd
import matplotlib.pyplot as plt


stock_data_file = "METAStockPrices.csv"

def loadData(file):
    return pd.read_csv(file)


def findAvgCloseByMonth(df):
    df['Date'] = pd.to_datetime(df["Date"]).dt.strftime('%Y-%m')
    df_avg = df.groupby('Date')['Close'].mean().reset_index(name='Average_Close')
    df_avg["Year"] = pd.to_datetime(df_avg['Date'], format='%Y-%m').dt.year
    return df_avg


def plotYearlyAvgs(df):
    for year, group in df.groupby('Year'):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.plot(range(len(group['Date'])), group['Average_Close'], 'bo')
        plt.xticks(range(len(group['Date'])), pd.to_datetime(group['Date'], format='%Y-%m').dt.strftime('%B').tolist(), rotation=30)
        # group.plot(kind='scatter', x='Date', y='Average_Close', title=f'Avg {year} monthly META stock closing price')
        # plt.xticks(ticks=group['Date'], labels=pd.to_datetime(group['Date'], format='%Y-%m').dt.strftime('%B').tolist(), rotation=30)

        for i, v in enumerate(group['Average_Close']):
            ax.text(i, v+0.45, "%.2f" %v, ha="center", rotation=0)
        plt.title(f'Meta\'s {year} Monthly Stock Average')
        plt.savefig(f'plots/{year}monthlyStockAvg.png')
        # plt.show()
        plt.close()

def plotOctNovDifference(df):
    df["Month"] = pd.to_datetime(df['Date'], format='%Y-%m').dt.month
    print(df)
    df_fall = df[df["Month"].isin([10,11])]
    df_fall = df_fall[df_fall['Year']<2023]
    print(df_fall)
    print(df_fall.count())
    df_fall_diff = df_fall.groupby('Year')['Average_Close'].diff().dropna().reset_index(name='Difference')
    df_fall_diff["index"] = [2012+i for i in range(11)]
    # df_fall_diff = df_fall_diff.set_index("index")
    print(df_fall_diff)
    plt.bar(df_fall_diff["index"], df_fall_diff["Difference"])
    plt.show()
 

def main():
    df = loadData(stock_data_file)
    df = findAvgCloseByMonth(df)
    # plotOctNovDifference(df)
    plotYearlyAvgs(df)

if __name__=="__main__": 
    main()