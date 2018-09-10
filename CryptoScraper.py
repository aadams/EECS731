# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 12:12:50 2018

@author: Austin
"""
import datetime
import time
import pandas as pd
#Using REST API w/ crypto watch to get order data from two different exchanges. This is growable by simply adding more dfs.
df1 = pd.read_json('https://api.cryptowat.ch/markets/kraken/btcusd/orderbook')
df2 = pd.read_json('https://api.cryptowat.ch/markets/binance/btcusdt/orderbook')

#Create Columns Headers
H1 = 'Price @ ' + str(datetime.datetime.now())
H2 = 'Amount @ ' + str(datetime.datetime.now())
col = [H1, H2]

#Create Pandas DF that will be joined with others
dfKA = pd.DataFrame(df1['result']['asks'], columns = col)
dfKB = pd.DataFrame(df1['result']['bids'], columns = col)

dfBA = pd.DataFrame(df2['result']['asks'], columns = col)
dfBB = pd.DataFrame(df1['result']['bids'], columns = col)

#I can only call this method while the reamining in df1 is not zero. I would like to get constant info
remaining = df1['allowance']['cost'] + df2['allowance']['cost'] + df1['allowance']['remaining']
costs = (df1['allowance']['cost'] + df2['allowance']['cost']) / 2

#This will create the amount of time that I can iterate every hour. There will be added wiggle room by process time
sleep = (remaining / costs / 3600)

#Because I do not have SQL setup just yet, I just will iterate for proof purposes. I will eventually write to SQL
for x in range(1, 1000):
    if df2['allowance']['remaining'] > 0: 
        df1 = pd.read_json('https://api.cryptowat.ch/markets/kraken/btcusd/orderbook')
        df2 = pd.read_json('https://api.cryptowat.ch/markets/binance/btcusdt/orderbook')
        
        H1 = 'Price @ ' + str(datetime.datetime.now())
        H2 = 'Amount @ ' + str(datetime.datetime.now())
        col = [H1, H2]
        
        dfKA1 = pd.DataFrame(df1['result']['asks'], columns = col)
        dfKB1 = pd.DataFrame(df1['result']['bids'], columns = col)
        
        dfBA1 = pd.DataFrame(df2['result']['asks'], columns = col)
        dfBB1 = pd.DataFrame(df1['result']['bids'], columns = col)

        #Join the old and the new to create a larger frame
        dfKA = dfKA.join(dfKA1)
        dfKB = dfKB.join(dfKB1)
        dfBA = dfBA.join(dfBA1)
        dfBB = dfBB.join(dfBB1)
        time.sleep(sleep)
dfKA.to_csv('KA.csv', encoding = 'utf-8', index = False)
dfKB.to_csv('KB.csv', encoding = 'utf-8', index = False)
dfBA.to_csv('BA.csv', encoding = 'utf-8', index = False)
dfBB.to_csv('BB.csv', encoding = 'utf-8', index = False)


        
    