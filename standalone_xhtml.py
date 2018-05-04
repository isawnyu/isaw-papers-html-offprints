import base64
from bs4 import BeautifulSoup    
import os
import re

i64 = []


for j in range(9, 10):

	# soup
	with open("isaw-papers-awdl/"+str(j)+"/index.xhtml", "r") as article :
		soup = BeautifulSoup(article, "lxml")
	print(soup)
	images = soup.find_all("img", {"src" : re.compile("images/*")}) 

	# Replacing images by base64 images for the articles that are illustrated in the soup
	if os.path.isdir(str(j)+"/images_small/images") :
		for filename in os.listdir(str(j)+"/images_small/images"):
		    with open(str(j)+"/images_small/images/"+filename, "rb") as imageFile:
		        im64 = base64.b64encode(imageFile.read())
		        i64.append(str(im64).replace("b'", "").replace("'",""))

		for i in range(0, len(images)):
			source = images[i]["src"]
			source = source.replace("images/", "").replace(".png", "").replace(".jpg", "")
			images[i].wrap(soup.new_tag("a", href="http://dlib.nyu.edu/awdl/isaw/isaw-papers/"+str(j)+"/#"+source))
			images[i]["src"] = "data:image/png;base64,"+str(i64[i])

	# putting the css in the xhtml file
	if os.path.exists("isaw-papers-awdl/"+str(j)+"/isaw-papers.css"):
		with open("isaw-papers-awdl/"+str(j)+"/isaw-papers.css", "r") as css_file :
			css = css_file.read()
	elif os.path.exists("isaw-papers-awdl/"+str(j)+"/isaw-publications.css"):
		with open("isaw-papers-awdl/"+str(j)+"/isaw-publications.css", "r") as css_file :
			css = css_file.read()

	soup.head.append(soup.new_tag("style"))
	soup.head.style.append(css)

	# creating the standlone xhtml file
	with open(str(j)+"/standalone-"+str(j)+".xhtml", "w") as article :
		article.write(str(soup))

	# adding the link to the download file
	with open("index.md", "a") as download_page:
		download_page.write("<a href='"+str(j)+"/standalone-"+str(j)+".xhtml' download>Click to Download Paper " + str(j) + "</a>\n  <a href='"+str(j)+"/standalone-"+str(j)+".xhtml'>Click to see in browser Paper "+str(j) + "</a>\n\n")


