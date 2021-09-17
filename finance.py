import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import smtplib
from email.message import EmailMessage
from config import *

transaction_data_df = pd.read_csv(PATH,header=None,names=["Date", "Transaction", "Out", "In"])
transaction_data_df = transaction_data_df.fillna(0)
transaction_data_df['Transaction_ID'] = ''
for i in transaction_data_df.index:
    if "PURCHASE" in transaction_data_df['Transaction'][i]:
        transaction = transaction_data_df['Transaction'][i]
        transaction = transaction.partition('PURCHASE')[2].lstrip(' ')
        transaction = transaction.split(' ', 1)
        transaction_id = transaction[0]
        transaction_data_df['Transaction_ID'][i] = transaction_id
        transaction_data_df['Transaction'][i] = transaction[1]
        
transaction_data_df = transaction_data_df[['Date','Transaction_ID','Transaction','Out','In']]
#This data is for total expenses of the month
total_expenses = abs(transaction_data_df['Out'].sum() - transaction_data_df['In'].sum())
total_expenses = "{:.2f}".format(total_expenses)
#This data is for total City Market Spending of the month
city_market = transaction_data_df[transaction_data_df['Transaction'] == "MIKE'S INDEPEND"]
city_market_sum = city_market['Out'].sum()
#This data is for total Starbucks Spending of the month
starbucks = transaction_data_df[transaction_data_df['Transaction'] == "STARBUCKS COFFE"]
starbucks_sum = starbucks['Out'].sum()


def send_email(month):
    msg = EmailMessage()
    msg.set_content(f'Your total expense for the month of {month} is ${total_expenses}\nYour total City Market spending for the month of {month} is ${city_market_sum}\nYour total Starbucks spending for the month of {month} is ${starbucks_sum}')

    msg['Subject'] = 'Monthly Spending for Denis Kuznetsov'
    msg['From'] = "MyExpenses"
    msg['To'] = PERSONAL_EMAIL

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(EMAIL, PASSWORD)
    server.send_message(msg)
    server.quit()
    
send_email('August')
