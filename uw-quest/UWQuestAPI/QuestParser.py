from bs4 import BeautifulSoup
import re

# Return ['Address Type', 'Address', 
#	'Home', '101-137 UNIVERSITY AVE. W, WATERLOO Ontario N2L 3E6', 
#	'Mail', '101-137 UNIVERSITY AVE. W, WATERLOO Ontario N2L 3E6']
def Parse_personalInfo_address(html):
	soup = BeautifulSoup(html)

	# addressTable contains address information
	addressTable = soup.find(id="SCC_ADDR_H$scroll$0")

	# Clean tags
	tableString = str(addressTable)
	x = re.sub("\<.*?\>", "", tableString);
	# clean result list
	resultList = filter(lambda x: len(x) > 0, x.replace(" \r", ", ").split("\n"))
	del(resultList[2])
	# resultList contains
	return resultList