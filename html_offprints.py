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


for j in range(11, 12) :
	if j != 7 :
		i64 = []

		# soup
		with open("isaw-papers-awdl/"+str(j)+"/head.xml", "r") as head:
			head = BeautifulSoup(head, "xml")
			div_head = head.div

		with open("isaw-papers/isaw-papers-"+str(j)+"/isaw-papers-"+str(j)+".xhtml", "r") as article :
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

		# putting the css in the xhtml file et virer le lien vers le CSS 
		css_link = soup.find("link", {"rel" : re.compile("stylesheet*")})
		css_link.decompose()
		with open("isaw-papers/isaw-publications.css", "r") as css_file :
				css = css_file.read()
		css = css.replace("<http://isaw.nyu.edu/publications/isaw-papers>", "&lt;http://isaw.nyu.edu/publications/isaw-papers&gt;")
		soup.head.append(soup.new_tag("style"))
		soup.head.style.append(css)

		# adding javascript elements for the paragraphs		
		paragraphs = soup.find_all("p", {"id": True})
		for p in paragraphs :
			ids = p["id"]
			p["onmouseleave"] = "document.getElementById('"+ids+"anchor').style.display='none';document.getElementById('"+ids+"anchor_label').style.display='none';"
		
			p["onmouseover"] = "document.getElementById('"+ids+"anchor').style.display='';document.getElementById('"+ids+"anchor_label').style.display='';" 
			link = soup.new_tag("a", id=ids+"anchor", style="color:#aaa;display:none", href="#"+ids )
			link.append("⬈")
			p.append(link)
			span = soup.new_tag("span", id=ids+'anchor_label', style="color:#aaa;display:none;position:fixed;right:0;bottom:50%" )
			span.append(ids)
			p.append(span)


		# absolute links for the video
		if soup.video :
			mp4s = soup.find_all("source", {"type" : "video/mp4"})
			for mp4 in mp4s :
				relative = mp4["src"]
				absolute = "http://dlib.nyu.edu/awdl/isaw/isaw-papers/"+str(j)+"/"+relative
				mp4["src"] = absolute 
			webms = soup.find_all("source", {"type" : "video/webm"})
			for webm in webms :
				relative = webm["src"]
				absolute = "http://dlib.nyu.edu/awdl/isaw/isaw-papers/"+str(j)+"/"+relative
				webm["src"] = absolute 



		

		# Adding the head.xml
		soup.header.insert_before(div_head )

		# creating the standalone xhtml file
		with open(str(j)+"/isaw-papers-"+str(j)+"-offprint.xhtml", "w") as article :
			article.write(str(soup))

		# adding the link to the index file
		with open("index.md", "a") as download_page:

			download_page.write("ISAW Papers "+str(j)+"  \n---\n<a href='"+str(j)+"/isaw-papers-"+str(j)+"-offprint.xhtml' download>Click to download</a>  \n<a href='"+str(j)+"/isaw-papers-"+str(j)+"-offprint.xhtml'>Click to see in browser</a>\n\n")


