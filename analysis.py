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

        for i, v in enumerate(group['Average_Close']):
            ax.text(i, v+0.45, "%.2f" %v, ha="center", rotation=0)
        plt.title(f'Meta\'s {year} Monthly Stock Average')
        plt.savefig(f'plots/{year}monthlyStockAvg.png')
        plt.close()


def plotMonthDifference(df, monthRange):

    # Calculate the difference between average monthly closing stock prices
    # for Oct and Nov and store in new Column
    df["Month"] = pd.to_datetime(df['Date'], format='%Y-%m').dt.month
    df_fall = df[df["Month"].isin(monthRange)]
    df_fall = df_fall[df_fall['Year']<2024]
    df_fall_diff = df_fall.groupby('Year')['Average_Close'].diff().dropna().reset_index(name='Difference')
    df_fall_diff["index"] = [2012+i for i in range(12)]

    # Plot results
    plt.bar(df_fall_diff["index"], df_fall_diff["Difference"])
    for i, v in enumerate(df_fall_diff["Difference"]):
        sign = -1.5 if v<0 else 0.75
        plt.text(i+2012, v + sign, "%.2f" %v, ha="center")
    plt.ylim(min(df_fall_diff["Difference"])-3, max(df_fall_diff["Difference"])+3)

    month1, month2 = "InvalidMonth", "InvalidMonth"
    match monthRange[0]:
        case 10:
            month1, month2 = "Oct", "Nov"
        case 11:
            month1, month2 = "Nov", "Dec"
        case default:
            print("Pick a valid month range")
    plt.title(f'Meta\'s Difference in Average Closing Stock Price Between {month1} and {month2}')
    plt.savefig(f'plots/{month1}{month2}DifferenceGraph.png')
    plt.close()
 

def main():
    df = loadData(stock_data_file)
    df = findAvgCloseByMonth(df)
    plotMonthDifference(df, [11,12])
    plotMonthDifference(df, [10,11])
    plotYearlyAvgs(df)

if __name__=="__main__": 
    main()
