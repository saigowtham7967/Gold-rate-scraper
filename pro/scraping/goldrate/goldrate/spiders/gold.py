import scrapy
from datetime import date
import sqlite3
from twilio.rest import Client


class GoldSpider(scrapy.Spider):
    name = 'gold'
    allowed_domains = ['https://www.goodreturns.in/gold-rates/']
    start_urls = ['https://www.goodreturns.in/gold-rates/visakhapatnam.html']

    def parse(self, response):
        # connecting to the database
        con = sqlite3.connect('newgoldrate.sqlite')
        # creating a cursor
        cur = con.cursor()
        # creating a table for storing the values of the gold information
        cur.execute("""CREATE TABLE IF NOT EXISTS newgoldrate(
            date TEXT PRIMARY KEY ,
            goldcaret TEXT ,
            costtoday TEXT,
            costyesterday TEXT)""")

        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        rate = response.css('section.gr-listicle-content div.gold_silver_table.right-align-content')
        cost = rate.css('tr.odd_row')
        lst = cost.css('td::text').getall()
        # creating a dictionary to store the values of the gold information
        dictionary = {
            'date': d1,
            'goldcaret': lst[0],
            'cost_today': lst[1],
            'cost_yesterday': lst[2],
        }
        print(dictionary)
        # inserting values into the table when a new primary key is accessed
        cur.execute("""INSERT OR IGNORE INTO newgoldrate(date,goldcaret,costtoday,costyesterday) VALUES(?,?,?,?)
                """, (
        dictionary['date'], dictionary['goldcaret'], dictionary['cost_today'], dictionary['cost_yesterday']))
        # committing the changes
        con.commit()
        print('data committed')
        account_sid = 'ACae0379a57e5593820dc76a52a4b9561a'
        auth_token = '622a593bb6a107b646bf1b11879d7756'
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body='date:{}      goldcaret:{}        gold new cost:₹{}       gold old cost₹{}'.format(
                dictionary['date'], dictionary['goldcaret'], dictionary['cost_today'], dictionary['cost_yesterday']),
            from_='+19123784845',
            to='+917893883109'
        )

        print(message.sid)
