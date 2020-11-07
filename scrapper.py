# -*- coding: utf-8 -*- 

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import argparse
import csv
import re
import multiprocessing

BASE_URL = 'http://www.noolulagam.com/books'
HEADER = ['நூல் பெயர்', 'வகை', 'எழுத்தாளர்', 'பதிப்பகம்', 'Year', 'விலை']

def get_data(n):
	res_lst = []
	try:
		url = f"{BASE_URL}/{str(n)}"
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		tabs = soup.find_all('table', attrs={ 'style':"border-collapse: collapse; border: 0px solid orange; width :100%"} )
		for t in tabs:
			keys = []
			val = []
			title = {'நூல் பெயர்': t.find('h4').get_text().strip() } #getting title from h4
			cols= t.find('table').findAll('td', align='left')
			cols = [ ele.text.strip() for ele in cols ]
			for c in range(len(cols)):
				if c%2 == 0:
					keys.append(cols[c])
				else:
					val.append(cols[c])
			fin_dict = dict(zip(keys,val))
			fin_dict.update(title)
			res_lst.append(fin_dict)
	except Exception as e:
		print(f"error occurred {str(e)}")
	return res_lst 


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--start', type=int, required=True, help='start page')
	parser.add_argument('--end', type=int, required=True, help='end page')
	parser.add_argument('--out', type=str, default="books.csv", help="output filename")
	args = parser.parse_args()

	with multiprocessing.Pool() as p:
		with open(args.out, 'a') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=HEADER, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			writer.writeheader()
			for n in tqdm(p.imap_unordered(get_data, range(args.start, args.end+1))):
				for item in n:
					writer.writerow(item)
				