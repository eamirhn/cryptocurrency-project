
import requests , numpy as np ,openpyxl as op 
import matplotlib.pyplot as plt ,datetime
now=datetime.datetime.now()

# get information using API
try :
    r=requests.get('https://api.blockchain.com/v3/exchange/tickers/BTC-USD')
    historicalData = requests.get('https://api.coindesk.com/v1/bpi/historical/close.json').json()
    getETH=requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd').json()
    ethprice=getETH[1]['current_price']
except:
    print('Please Turn off Your VPN !!')


# current bitcoin price

dataCurrent = r.json()
currnetPrice = dataCurrent['price_24h'] 


#making it those info in list format

prices = list(historicalData['bpi'].values()) # for X axe
dates = list(historicalData['bpi'].keys()) # for Y axe 31 items
xItems = list(range(1,32)) # in order to assosiate this with dates with regression

#analiz
variance=np.floor(np.var(prices)*100)/100
meanBitcoin = np.floor(np.mean(prices)*100)/100

# creating Plot
plt.ylabel('Prices')
plt.xlabel('Dates (over last 31 days)')
plt.title('Bitcoin Prices over Last 31 days(USD)')
plt.xticks(rotation = 45)
plt.text(17,44000,s=f"today : {now}\nCurrent Price : {currnetPrice} $USD\nlinear Regression : --\nRegression : ..\nvariance : {variance}\nmean : {meanBitcoin} $")

# regression
coef = np.polyfit(xItems,prices,3)
poly1d_fn = np.poly1d(coef)
plt.plot(dates,prices,color="g")
plt.plot(xItems, poly1d_fn(xItems), ':r',)

# linear regression
coef2 = np.polyfit(xItems,prices,1)
poly1d_fn2 = np.poly1d(coef2)
plt.plot(xItems, poly1d_fn2(xItems), '--k',)
#plt.show()





running = True

text ='''Welcome to Digital Currency News\n\nto see the plot for BTC : 1\n\
to see the current prices of diffrent digital currencies : 2\n\
to save these datas in an excel file enter : 3\nfor see wich one has had the biggest jump in price for the last 24h enter : 4\nto see if you had invested a certain amount\
in a certain date , how much would have you gained or loss : 5\nand for exit enter : -1'''


text2='''to see the current prices of diffrent digital currencies : 2\n\
to save these datas in an excel file enter : 3\nfor see wich digital currency -over top 100 of them- has had the biggest jump in price for the last 24h enter : 4\
\nto see if you had invested a certain amount\
in a certain date , how much would have you gained or loss : 5\nand for exit enter : -1'''
print(text)
print('\n**********************')


#running the program
while running:
    n=eval(input())
    if n==1: #for showing the plot
        plt.show()
        print('\n**********************')

    if n==3: #for inserting to excel
        # importing information into excel
        book=op.Workbook()
        sheet=book.active
        sheet.append(prices)
        sheet.append(dates)
        #book.save("sample.xlsx")
        from openpyxl.chart import BarChart, Reference, Series
        values = Reference(sheet, min_col=1, min_row=1, max_col=30, max_row=1)
        chart = BarChart()
        chart.add_data(values)
        sheet.add_chart(chart, "E15")
        name=input('enter the name of the file : ')
        book.save(f"{name}.xlsx")
        print('the file has been created! (in this directory)')
        print('\n**********************')
    if n==2: #to see 100 digital currency prices
        running2=True
        while running2:
            for i in range(0,100):
                tt=getETH[i]['id']
                print(f'{i}',tt)
            code=eval(input('\nPlease Enter the code in order to get the price info for that digital currency\nFor Quit Enter -1 : '))
            if code==-1: 
                running2=False
                print('\n**********************')

            for j in range(0,100):
                if code==j:
                    currentP=getETH[j]['current_price']
                    name=getETH[j]['id']
                    high=getETH[j]['high_24h']
                    low=getETH[j]['low_24h']
                    change=high-low
                    print('\n**********************')
                    print(f'\ntoday : {now}')
                    print(f'{currentP} $USD for {name}.\nchange for last 24h is {change}$\n(high,low) in last 24h is ({high},{low})')
                    running2=False
                    print('\n**********************')

                    print(text2)


    if n==-1:# for exite
        print('thank you!!')
        running=False
    if n==4:
        max=0
        id=0
        minBOx=[None]*100
        for j in range(0,100):
            
            name=getETH[j]['id']
            high=getETH[j]['high_24h']
            low=getETH[j]['low_24h']
            change=high-low
            minBOx[j]=change
            if change>max:
                id=j
                max=change
            if max>=change:
                pass
            
        theOne=name=getETH[id]['id']
        minID=minBOx.index(min(minBOx))
        nameMin=getETH[minID]['id']
        theOne=getETH[id]['id']
        print(f'the biggest jump for last 24h is \"{theOne}\" and the change was {max} $ \nand the lowest decrease is \"{nameMin}\" with the change {min(minBOx)} $\n!it may change tomorrow!')
        print('\n**********************')

        
    if n==5:
        print('Welcome to Back Test!')
        fromfrom=list(historicalData['bpi'].keys())

        running3=True
        while running3:
            try:
                backDateD=(input(f'now : {now}\nnotice1!! you must use two character for day and month like 09 or 06\nnotice2!!\
you must enter a date for last 31 days (from {fromfrom[0]} to {fromfrom[-1]})\nenter a day in last 31 days :'))
                backDateM=(input('enter the month :'))
                backDateY=(input('enter the year :'))
                backPriceBTC=historicalData['bpi'][backDateY+'-'+backDateM+'-'+backDateD]
                invesment=eval(input('\n--- Well done! ---\nnow Enter the money you had wanted to invest in USD$ : '))
                running3=False
            except:
                print('\n***** Error!! please try again *****\n')
            
        def profitORloss(invest,currentprice,backThenPrice):
            return ((currentprice*invest)/backThenPrice)-invest


        print('\nprosseing....\n')
        pOl=profitORloss(invesment,currnetPrice,backPriceBTC)
        thatTime=backDateY+'-'+backDateM+'-'+backDateD
        if pOl>=0: 
            print(f'you would have gained exacly {pOl} by today if you had bought {invesment}$ BTS in {thatTime}')
            print('\n**********************')

            c=eval(input('to see the previous menu :1 , and for exit type -1 :  '))
            if c==1:
                print(text2)
            if c==-1:
                running=False
        else:
            print(f'you would have lost {pOl} by today if you bought {invesment}$ BTC in {thatTime}')
            print('\n**********************')
            c=eval(input('to see the previous menu :1 , and for exit type -1 :  '))
            if c==1:
                print(text2)
            if c==-1:
                running3=False
                running=False
                

    else:
        if n!=1 and n!=2 and n!=3 and n!=4 and n!=5 and n!=-1:
            print('\n!! Error please try again !!')

        

    