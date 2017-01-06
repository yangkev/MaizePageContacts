# /usr/local/bin

"""
 script for scraping organization information off of Maize Pages
 Written by Kevin Yang

"""

import requests
import csv
import math
import re
import sys
from bs4 import BeautifulSoup	
from urlparse import urljoin

BASE_URL = 'https://maizepages.umich.edu'

class UserSession(object):
	"""Class that authenticates a user for access to Maize Pages, and provides
	methods for parsing and writing data to csv.

	Attributes:
		session: requests session to persist cookies/authentication things
	"""
	def __init__(self, username, password):
		self.session = requests.Session()
		# Get cookie
		response = self.session.get("https://maizepages.umich.edu/account/logon")

		# Get input fields and create payload with username/password
		payload ={}
		soup = BeautifulSoup(response.text, 'html.parser')
		for input in soup.find_all("input"):
			payload[input.get("name")] = input.get("value")
		payload['login'] = username
		payload['password'] = password

		# Post to weblogin and subsequently go through all authentication steps
		try:
			self.send_post("https://weblogin.umich.edu/cosign-bin/cosign.cgi", payload)
		except ValueError as e:
			print "Error logging in with credentials"
			sys.exit()

		try:
			self.check_auth
		except ValueError as e:
			print e
			sys.exit()

	# Description: Checks that authentication worked by searching for "Sign in"
	#	in the HTTP response
	def check_auth(self):
		response = self.session.get("https://maizepages.umich.edu")
		if(not 'Sign in' in response.text):
			print "Logged in successfully"
		else:
			raise ValueError

	# Description: Recursive function for jumping through all the authentication
	#	steps 
	def send_post(self, url, payload):
		# Send HTTP POST request
		response = self.session.post(url, data=payload)
		response.raise_for_status()
		
		# Base case for returning after the appropriate post requests have been entered
		if response.url == BASE_URL + '/':
			return

		soup = BeautifulSoup(response.text, 'html.parser')

		# Construct the next url to recurse into
		relative_url = soup.find('form').get('action')
		absolute_url = urljoin(response.url, relative_url)
		# Checks that recursion doesn't enter infinite loop
		if absolute_url == url:
			raise ValueError

		# Gather input fields into payload
		payload.clear()
		for input in soup.find_all("input"):
			payload[input.get("name")] = input.get("value")

		self.send_post(absolute_url, payload)

	# Description: Takes in an organization's page url and 
	#	returns a tuple containing (name, email, org name)
	def parse_for_name_and_email(self, org_page_url):
		response = self.session.get(org_page_url)
		response.raise_for_status()
		soup = BeautifulSoup(response.text, 'html.parser')
		tag = soup.find(class_ = "member-modal")
		
		# Get name
		name = tag.string
		# Get email
		email = ''
		try:
			email_resp = self.session.get(BASE_URL + tag['href'])
			email_resp.raise_for_status()
			email_soup = BeautifulSoup(email_resp.text, 'html.parser')
			email_tag = email_soup.find(class_ = "email")
			m = re.search('mailto:(.+)', email_tag['href'])
		except:
			# do nothing
			pass
		else:
			if m:
				email = m.group(1)
		# Get org name
		orgname = soup.find(class_='h2__avatarandbutton').get_text().encode('utf-8').strip()

		return (name, email, orgname)

	# Description: Visits each organization page on maizepages and calls
	#	parse_for_name_and_email on each. Takes the results and outputs them
	#	to a csv file.
	def run_all(self):
		csvfile = open('org_data.csv', 'wb')
		datawriter = csv.writer(csvfile)

		# Get the number of pages to iterate through
		index_resp = self.session.get(BASE_URL + '/organizations?CurrentPage=1')
		index_resp.raise_for_status()
		soup = BeautifulSoup(index_resp.text, 'html.parser')
		num_pages_tag = soup.find(class_ = "pageHeading-count")
		num_pages = int(math.ceil(float(num_pages_tag.findAll('strong')[1].string) / 10))
		
		for i in range(1, num_pages + 1):
			response = self.session.get(BASE_URL + '/organizations?CurrentPage=' + str(i))
			response.raise_for_status()
			soup = BeautifulSoup(response.text, 'html.parser')
			for page in soup.find_all('h5'):
				url = page.a['href'] 
				try:
					datawriter.writerow(self.parse_for_name_and_email(BASE_URL + url))
				except Exception as e:
					print e
					sys.exit()
				
				
			print '{}/{} completed'.format(i, num_pages)

def main():
	username = raw_input('Uniqname: ')
	password = raw_input('Password: ')
	maize = UserSession(username, password)
	maize.run_all()

if __name__ == "__main__":
	main()
