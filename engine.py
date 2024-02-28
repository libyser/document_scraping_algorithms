
import requests
from bs4 import BeautifulSoup
from libser_engine.utils import payload
from libser_engine.utils.exception import GoogleCaptcha, GoogleCookiePolicies
from googlesearch import search
import urllib
import threading
import random
import re
from queue import Queue
from urllib.parse import unquote


class Extract():

	#____________________________________________
	# duckduckgo.com
	#-------------------------------------------
	def duckduckgo_search(self, qury: str, filetype: str, que):
		
		self.qury = qury
		self.filetype = filetype
		self.paylod, self.cookie = payload.Headers().duckduckgo_parm()
		
		pattern = r'uddg=(.*?)&'

		links = {}
		try:
			self.link = 'https://html.duckduckgo.com/html/?q=' + self.qury + '+filetype%3A'+ self.filetype # + '&ai=software'
			req = requests.get(self.link, headers=self.paylod, allow_redirects=False, timeout=10)
			self.data = req.text
			status = req.status_code

            # Data extrcation from search page
			if status == 200:
				soup = BeautifulSoup(self.data, 'html.parser')

				for link_ in soup.find_all('a', href=True):
					lnks = link_['href']

					try:
						if 'http' in lnks:
							match = re.search(pattern, lnks)

							if match:
								link = match.group(1)
								link = urllib.parse.unquote(link)

								if link not in links and '.pdf' in link:
									name = link.split('/')[-1].replace('.pdf', '')
									links[name] = link
					except: None
				que.put(links)
			else: que.put({})
		except: que.put({})

	#______________________________________
	# google.com
	#-------------------------------------
	def google_search(self, target: str, filetype:str, que):
		self.word = target
		self.filetype = filetype
		#self.counter = 50
		#self.quantity = "100"
		#self.agent = payload.Headers().user_agent()

		links = {}

		try:
			count = 1
			query = self.word + ' filetype:pdf'
			for j in search(query, num=10, stop=10, pause=2):
				links['Document '+str(count)] = j
				count+=1
			
			que.put(links)
		except: que.put(links)

		'''
		urllib3.disable_warnings()

		documents = []
		num = 50 if total > 50 else total

		url_base = f"https://www.google.com"
		#cookies = {"CONSENT": "YES+srp.gws"}

		header = payload.Headers().google_parm()
		
		try:
				
			url = url_base + f"/search?num="+self.quantity+"&start=" + str(self.counter) + "&hl=en&meta=&q=filetype:"+self.filetype+"%20allintext:" + self.word
			
			response = requests.get(url, headers=header, timeout=5, verify=False, allow_redirects=False)
			
			text = response.text
			content = response.content
			
			if response.status_code == 302 and ("htps://www.google.com/webhp" in text or "https://consent.google.com" in text):
				return False #raise GoogleCookiePolicies()
			if "detected unusual traffic" in text:
				return False #raise GoogleCaptcha()
			
			soup = BeautifulSoup(content, features="lxml")
			
			for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
				link = re.split(":(?=http)",link["href"].replace("/url?q=",""))

				filtered_link = link[0].split('&sa=')
				documents.append(filtered_link[0])
			
			return documents

		except: return False #It's left over... but it stays there'''
	'''
	#______________________________________
	# yandex.com 0
	#-------------------------------------
	def yandex_search(self, target, filetype):
		self.target = target
		self.filetype = filetype
		self.paylod = payload.Headers().yandex_parm()

		_link_ = 'https://yandex.com/search/?text=' + self.target + '+filetype+%3A+' + self.filetype
		all_links = {}

		req = requests.get(_link_, headers=self.paylod, timeout=5)

		self.data = req.text
		status = req.status_code
		
		soup = BeautifulSoup(self.data, 'html.parser')

		patt = "^http.*.pdf$"

		if status == 200:
			for link_ in soup.find_all('a', href=True):
				lnks = link_['href']
				print(lnks)
				search_ind = re.search(patt, lnks)
				if search_ind is not None:
					_lnks_ = search_ind[0]
				
					if _lnks_ not in all_links:
						name  = _lnks_.split('/')[-1].replace('pdf', '')
						all_links[name] = _lnks_
		
			return all_links
		else: return False
	'''
	'''
	#______________________________________
	# google.com/search?tbm=bks&q=<book+name>
	#-------------------------------------
	def google_book_search(self, target):
		self.target = target
		self.paylod = payload.Headers().google_parm()

		urllib3.disable_warnings()

		_link_ = 'https://www.google.com/search?tbm=bks&q=' + self.target.replace(' ', '-')
		all_links = []

		req = requests.get(_link_, headers=self.paylod, timeout=5, verify=False, allow_redirects=False)

		self.data = req.text
		status = req.status_code

		soup = BeautifulSoup(self.data, 'html.parser')

		patt = "^https://books.google.co.in/books?.*$"

		if status == 200:
			for link_ in soup.find_all('a', href=True):
				lnks = link_['href']

				search_ind = re.search(patt, lnks)

				if search_ind is not None:
					_lnks_ = search_ind[0]
					all_links.append(_lnks_)
			
			return all_links
		else: return False
	'''
	'''
	#_____________________________________
	# bing.com 1
	#-------------------------------------
	def bing_search(self, target: str, filetype: str, que):

		# https://www.bing.com/search?q=the+mount+everest+filetype%3Apdf

		self.target = target
		self.filetype = filetype
		self.paylod = payload.Headers().google_parm()
		
		try:
			_link_ = 'https://www.bing.com/search?q=' + self.target + '+filetype%3A' + self.filetype + '&form=QBLH&sp=-1'
			all_links = {}

			req = requests.get(_link_, headers=self.paylod, timeout=5)
			
			if req.status_code == 200:
				self.data = req.text

				soup = BeautifulSoup(self.data, 'html.parser')

				# Find all li elements with class "b_algo"
				results = soup.find_all('li', class_='b_algo')
				count = 1

				for result in results:
					check_pdf = result.find('div', class_="b_attribution")

					if "PDF file" in str(check_pdf):

						link = result.find('a')['href']
						name  = 'Document ' + str(count)
						all_links[name] = link
						count+=1

				que.put(all_links)

			else: que.put({})
		except: que.put({})
	'''
	#_____________________________________
	# scholar.archive.org
	#-------------------------------------
	def scholar_search(self, target):

		#https://scholar.archive.org/search?q=economics
	
		self.target = target
		self.paylod = payload.Headers().google_parm()

		pattern = r'^https://web\.archive\.org/web/\d+/(.+)'

		_link_ = 'https://scholar.archive.org/search?q=' + self.target
		output_urls = {}

		try:
			req = requests.get(_link_, headers=self.paylod)

			self.data = req.text
			status = req.status_code
			
			soup = BeautifulSoup(self.data, 'html.parser')

			if status == 200:
				all_links = soup.find_all('a')

				for i in range(0, len(all_links)-10):
					href = all_links[i].get('href')
					if href is not None:
						if '.pdf' in href:
							
							url = re.sub(pattern, r'\1', href)
							index = unquote(url.split('/')[-1])
							output_urls[index] = url
			
			return output_urls
		except: return output_urls


class accumulate:

	def __init__(self, query: str, filetype: str):
		self.query = re.sub(' ', '+', query)

		self.filetype = filetype
		self.extract = Extract()

	'''
	def google_books(self):
		self.link = {}
		try: 
			self.links =  Extract().google_book_search(self.query)
			for sno in range(0, len(self.links)):
				self.link['Book '+str(sno)] = self.links[sno]

		except: None
		
		return self.link
	'''
	
	def all(self):

		self.g_data = Queue()
		self.d_data = Queue()
		#self.b_data = Queue()

		self.google_ = threading.Thread(target=self.extract.google_search, args=(self.query, self.filetype, self.g_data))
		self.duck_ = threading.Thread(target=self.extract.duckduckgo_search, args=(self.query, self.filetype, self.d_data))
		#self.bing_ = threading.Thread(target=self.extract.bing_search, args=(self.query, self.filetype, self.b_data))

		self.google_.start()
		self.duck_.start()
		#self.bing_.start()

		self.google_.join()
		self.duck_.join()
		#self.bing_.join()

		# Combine dictionaries
		combined_dict = {**self.g_data.get(), **self.d_data.get()}

		if combined_dict:
			# Shuffle items in the combined dictionary
			items = list(combined_dict.items())
			random.shuffle(items)
			shuffled_dict = dict(items)

			return shuffled_dict
		else: return {}


class Academics:

	def researches(self, query):
		self.query = re.sub(' ', '+', query)

		return Extract().scholar_search(self.query)
