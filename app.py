from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import telegram
import schedule
from pykrx import stock
import time
import pandas as pd
from datetime import datetime
from datetime import timedelta
import numpy as np
import chromedriver_autoinstaller
#
def Strtofloat(list):
	list_float = []
	for i in range(0, len(list)):
		list_float.append(list[i].strip("%"))
		return list_float
#
def strtodateformat(nalza, format):
	nalza_dateformat = []
	for i in range(0, len(nalza)):
		nalza_dateformat.append(datetime.strptime(nalza[i], format))
	return nalza_dateformat

def make_mv_avg(list, w):
	x = np.array(list, dtype=float)
	mv_avg = np.convolve(x, np.ones(w), 'valid') / w
	return mv_avg
# def Long_short_RATE_DIFFEREnce():

def date_range(start, end):
	start = datetime.strptime(start, "%Y%m%d")
	end = datetime.strptime(end, "%Y%m%d")
	dates = [date.strftime("%Y%m%d") for date in pd.date_range(start, periods=(end - start).days + 1)]
	return dates

def make_mv_avg(list, w):
	x = np.array(list, dtype=float)
	mv_avg = np.convolve(x, np.ones(w), 'valid') / w
	return mv_avg
##################
TodaY_Str = datetime.now().date().strftime("%Y%m%d")



api_key = '5165191702:AAHfSlZy8SnvYBq58VWcfME7GgcENcVgCzM'
bot = telegram.Bot(token=api_key)
telegram_chat_id = '1786134332'
now = datetime.now()

def kkrroling(site, xxppaath):
	path = chromedriver_autoinstaller.install()
	webdriver_options = webdriver.ChromeOptions()
	webdriver_options.add_argument('headless')
	driver = webdriver.Chrome(path, options=webdriver_options)
	driver.get(site)
	time.sleep(1)
	table = driver.find_element(By.XPATH, xxppaath).text
	return table

def make_nalza(year, month, day):
	nalza =[]
	for i in range(0, len(year)):
		nalza.append(year[i] + month[i] + day[i].strip(","))
	return nalza

def CROLING_YCHART_trnsfort(url, xpath, nz_format):
	data_list = kkrroling(url, xpath).split()
	data_sim_sl = data_list[14::]
	value = (data_sim_sl[3:100:4] + data_sim_sl[105::4])
	if type(value[0] != float):
		for i in range(0, len(value)):
			value[i] = float(value[i].strip("%"))
	year = data_sim_sl[2:100:4] + data_sim_sl[104::4]
	month = data_sim_sl[0:100:4] + data_sim_sl[102::4]
	day = data_sim_sl[1:100:4] + data_sim_sl[103::4]
	nalza = make_nalza(year, month, day)
	nalza_dateformat = strtodateformat(nalza, nz_format)
	mv_value = make_mv_avg(value, 3)
	return mv_value

def CROLING_INVES_trnsfort(url, xpath, nz_format):
	data_list = kkrroling(url, xpath).split()
	if (now.day > 15):
		value = data_list[17::7]
		Yyear = data_list[14::7]
		Mmonth = data_list[12::7]
		dday = data_list[13::7]
		nnalza = make_nalza(Yyear, Mmonth, dday)
		if type(value[0] != float):
			for i in range(0, len(value)):
				value[i] = float(value[i].strip("%"))
		nalza_dateformat = strtodateformat(nnalza, nz_format)
		mv_value = make_mv_avg(value, 3)
	return mv_value



url1 = 'https://ycharts.com/indicators/us_pmi'
xpathh1 = "/html/body/main/div/div[4]/div/div/div/div/div[1]/div[2]"
nz_format_ism = '%Y%B%d'
text_pmi = "PMI지수"
url2 = 'https://ycharts.com/indicators/us_retail_and_food_services_sales_yoy'
xpathh2 = "/html/body/main/div/div[4]/div/div/div/div/div[1]/div[2]"
nz_format_sales = '%Y%B%d'
text_sales = "미국소매판매"
url3 = 'https://ycharts.com/indicators/nahb_wells_fargo_us_hmi'
xpathh3 = "/html/body/main/div/div[4]/div/div/div/div/div[1]/div[2]"
nz_format_HOuse = '%Y%B%d'
text_house = "주택지수"
mv_pmi = CROLING_YCHART_trnsfort(url1, xpathh1, nz_format_ism)
mv_sales = CROLING_YCHART_trnsfort(url2, xpathh2, nz_format_sales)
mv_house = CROLING_YCHART_trnsfort(url3, xpathh3, nz_format_HOuse)
# # if ((mv_pmi[0] > mv_pmi[1] > mv_pmi[2]) & (mv_sales[0] > mv_sales[1] > mv_sales[2])& (mv_house[0] > mv_house[1] > mv_house[2])):
# # 	bot.sendMessage(chat_id=telegram_chat_id, text='buy : korean stock // sell : American dollar bond')
# # elif ((mv_pmi[0] < mv_pmi[1] < mv_pmi[2]) & (mv_sales[0] < mv_sales[1] < mv_sales[2])& (mv_house[0] < mv_house[1] < mv_house[2])):
# # 	bot.sendMessage(chat_id=telegram_chat_id, text='buy : American dollar bond // sell : korean stock')
# # else:
# # 	bot.sendMessage(chat_id=telegram_chat_id, text='hold')

tttitle = '{} 일자 매크로 경제지표(3개월 이동평균)'.format((datetime.now().date()).strftime("%Y-%m-%d"))

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
	my_variable = tttitle
	my_variable2 = text_pmi
	my_variable2_1 = [round(mv_pmi[0], 2),round(mv_pmi[1], 2),round(mv_pmi[2], 2)]
	my_variable3 = text_sales
	my_variable3_1 = [round(mv_sales[0], 2),round(mv_sales[1], 2),round(mv_sales[2], 2)]
	my_variable4 = text_house
	my_variable4_1 = [round(mv_house[0], 2),round(mv_house[1], 2),round(mv_house[2], 2)]
	return render_template('index.html', my_variable=my_variable,
						   my_variable2=my_variable2,
						   my_variable2_1=my_variable2_1,
						   my_variable3 = my_variable3,
						   my_variable3_1=my_variable3_1,
						   my_variable4 = my_variable4,
						   my_variable4_1=my_variable4_1)

if __name__ == "__main__":
	app.run(port=8080, debug=True)
