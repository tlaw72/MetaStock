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


def plotAvgs(df):
    for year, group in df.groupby('Year'):
        plt.figure()
        group.plot(kind='scatter', x='Date', y='Average_Close', title=f'Avg {year} monthly META stock closing price')
        plt.xticks(ticks=group['Date'], labels=pd.to_datetime(group['Date'], format='%Y-%m').dt.strftime('%B').tolist(), rotation=30)
        plt.savefig(f'{year}monthlyStockAvg.png')
        plt.close()
 

def main():
    df = loadData(stock_data_file)
    df = findAvgCloseByMonth(df)
    plotAvgs(df)

if __name__=="__main__": 
    main()