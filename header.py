from bs4 import BeautifulSoup

for i in range(1, 14):
	with open("isaw-papers-awdl/"+str(i)+"/head.xml", "r") as header : 
		soup = BeautifulSoup(header)

	with open(str(i)+"/head.xml", "w") as new_header :
		new_header.write(str(soup))
