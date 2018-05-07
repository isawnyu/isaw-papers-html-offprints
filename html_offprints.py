import base64
from bs4 import BeautifulSoup    
import os
import re

with open("index.md", "w") as download_page:
	download_page.write("""# ISAW Papers Articles standalone XHTML file



The journal is accessible online here : <a href="http://isaw.nyu.edu/publications/isaw-papers">http://isaw.nyu.edu/publications/isaw-papers</a>.

Unless otherwise noted all content is distributed under a Creative Commons Atribution license. See <a href="http://creativecommons.org/licenses/by/4.0/">http://creativecommons.org/licenses/by/4.0/</a>.

Feedback can be left by open an issue on the <a href="https://github.com/fmezard/isaw-papers-xhtml-standalone/">GitHub repository</a> that hosts this content.
""")


for j in range(1, 14):
	i64 = []
	# soup
	with open("isaw-papers-awdl/"+str(j)+"/index.xhtml", "r") as article :
		soup = BeautifulSoup(article, "lxml")
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
	with open(str(j)+"/isaw-papers-"+str(j)+"-offprint.xhtml", "w") as article :
		article.write(str(soup))

	# adding the link to the download file
	with open("index.md", "a") as download_page:

		download_page.write("ISAW Papers "+str(j)+"  \n---\n<a href='"+str(j)+"/isaw-papers-"+str(j)+"-offprint.xhtml' download>Click to download</a>  \n<a href='"+str(j)+"/isaw-papers-"+str(j)+"-offprint.xhtml'>Click to see in browser</a>\n\n")


