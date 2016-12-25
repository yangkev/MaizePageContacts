# /usr/local/bin

"""
 script for scraping organization information off of Maize Pages
 Written by Kevin Yang

"""

import requests
from bs4 import BeautifulSoup	

session = requests.Session()

# Login information
payload = {
		'login': username,
		'password': password }

# Get cookie
res = session.get("https://maizepages.umich.edu/account/logon")
res.raise_for_status()

# Find hidden input fields
soup = BeautifulSoup(res.text, "html.parser")

for input in soup.find_all("input"):
	payload[input.get("name")] = input.get("value")

# Login to CAS
res = session.post("https://weblogin.umich.edu/cosign-bin/cosign.cgi", data=payload)

# Verify login 
page_res = session.get("https://maizepages.umich.edu")
page_res.raise_for_status()

# "Sign in" should not be on the resulting page since user should be signed in
logon_success = not "Sign in" in page_res.text
print "Logged on successfully: " + str(logon_success)


# # Outerloop-
# res = session.get(baseurl + "/organizations", verify=False)
# res.raise_for_status() 

# pagination_soup = BeautifulSoup(res.text, "html5lib")

# # Create list of all url's on page
# pages = pagination_soup.find_all('h5')

# # Innerloop- visit each URL
# for page in pages:
# 	print page.a['href'] + ', ' + page.a.string 

# 	page_res = requests.get(baseurl + page.a['href'], verify=False)
# 	page_res.raise_for_status()

# 	page_soup = BeautifulSoup(page_res.text, "html5lib")
	

