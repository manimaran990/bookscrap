# -*- coding: utf-8 -*- 

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import argparse
import csv
import re


BASE_URL = 'http://www.noolulagam.com/books'
prohibitedWords = ['வகை', 'பதிப்பகம்', 'எழுத்தாளர்', 'விலை', '(Login for special discount)']
HEADER = ['நூல் பெயர்', 'வகை', 'எழுத்தாளர்', 'பதிப்பகம்', 'விலை']
remove_words = re.compile('|'.join(map(re.escape, prohibitedWords)))

def get_data(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	t = soup.findAll('table')
	for tab in t:
		for line in tab:
			if 'வகை' in str(line) and 'பதிப்பகம்' in str(line) and 'எழுத்தாளர்' in str(line) and 'விலை' in str(line):
				title = line.findAll('a')[-1]['title'].replace('Buy tamil book ','')
				cols = line.find('td', align='left')
				cols = [ ele.text.strip() for ele in cols ]
				vals = remove_words.sub('', str(cols)).replace(': ', ',')[3:].split(',')
				price = vals[-1].replace('\']', '').strip()
				vals.insert(0, title)
				vals[-1] = price
				vals = [ v.strip() for v in vals ] #trim whitespaces
				yield vals
                

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--start', type=int, required=True, help='start page')
	parser.add_argument('--end', type=int, required=True, help='end page')
	parser.add_argument('--out', type=str, default="books.csv", help="output filename")
	args = parser.parse_args()

	with open(args.out, 'a') as csvfile:
		writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(HEADER)
		for n in tqdm(range(args.start, args.end+1)):
			url = f"{BASE_URL}/{str(n)}"
			book_lst = get_data(url)
			for item in book_lst:
				writer.writerow(item)
				