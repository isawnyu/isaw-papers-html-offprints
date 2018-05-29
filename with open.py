import os
from bs4 import BeautifulSoup

for element in os.listdir("isaw-papers-awdl/7"):
	if os.path.isdir('isaw-papers-awdl/7/'+str(element)):
		for el in os.listdir('isaw-papers-awdl/7/'+ str(element)):
			if str(el) == "index.xhtml":
				with open ('isaw-papers-awdl/7/'+ str(element) + '/'+ str(el), "r") as article : 
					soup = BeautifulSoup(article,"html.parser")
					header = soup.body("div", {"id": "isaw_papers_header"})
					print(header)

				with open ("7/"+str(element)+"/head.xml", "w") as header_file:
					header_file.write(str(header))



