import urllib.request as req
import sqlite3
url = "https://www.cwb.gov.tw/V8/C/W/Observe/MOD/24hr/46757.html?T=17118382711"

request = req.Request(url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
})
with req.urlopen(request) as response:
    data = response.read().decode("utf-8") 
    
import bs4
root = bs4.BeautifulSoup(data, "html.parser") #讓BeautifulSoup協助我們解析HTML格式文件
time = root.find("th", class_="is_show") 
temp = root.find("span", class_="tem-C is-active")
time_content = list(time.stripped_strings)
date_part = time_content[0] #Date
time_part = time_content[1] #Time
#print(date_part, time_part, temp.string)


'''  
#To list all date , time and temperature

times = root.find_all("th", class_="is_show") 
temps = root.find_all("span", class_="tem-C is-active")
i = 0
for time in times:
    time_content = list(time.stripped_strings)
    date_part = time_content[0] #Date
    time_part = time_content[1] #Time
    print(date_part, time_part, temps[i].string)
    i = i + 1
'''


'''temps = root.find_all("span", class_="tem-C is-active") 
for temp in temps:
    print(temp.string)
'''

conn = sqlite3.connect('weather.db')
cursor = conn.cursor()
cursor.execute("INSERT INTO weather (w_date, w_time, w_temp) VALUES (?, ?, ?)",(date_part, time_part, temp.string))

cursor.execute("SELECT * FROM weather")
records = cursor.fetchall() 
print(records)

cursor.close()
conn.commit()
conn.close()