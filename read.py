import requests
import re
from bs4 import BeautifulSoup

content = []


def clean(text):
    text= text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


'''
PERIODICO <--> junto con el respectivo find-all de esa página
	--> FEED-SECCION 
		--> articulo(s) del feed pulidos
	

'''
link="http://www.finanzas.com/rss/noticiasportada.xml"
#link="http://www.portafolio.co/economia/feed"
#link="http://www.banrep.gov.co/rss.xml"
#link="http://feeds.bbci.co.uk/news/politics/rss.xml"

feed = requests.get(link, timeout=20) #Link = RSS
parser='html.parser'

#Hay que cambiar el guid, en portafolio es link, pero no funciona. Tuve que usar "#comments"
for url in BeautifulSoup(feed.content,parser).find_all('link'):
	try:
		print (url.text)
		article = requests.get(url.text, timeout=20)
	except Exception:
		print ("virgula")
	soup = BeautifulSoup(article.content, parser)
	#body = soup.find_all('div', class_='articulo-articulo') Para portafolio
	body = soup.find_all('div', class_='contenido_noticia')
	if (body):
		body2= clean(' '.join([t.get_text() for t in body[0].find_all(['p','h2'])]))
		content.append(body2)
		print("contenido va: "+str(len(content)))
	else:
		print ("empty body")

#print(content)
print(len(content))
f = open('resultado.txt', 'a')
for line in content:
	f.write(line+"\n")
	#print ("wrote :"+str(line))
f.close()

if( 1 == 0 ):
#Test Unique
	link="http://www.portafolio.co/economia/feed"
	feed = requests.get(link, timeout=20) #Link = RSS
	parser='html.parser'
	find_in_rss='link'
	urls = BeautifulSoup(feed.content,parser).find_all(find_in_rss)
	article = requests.get(urls[1].text, timeout=20)
	soup = BeautifulSoup(article.content, parser)
	body = soup.find_all('div', class_='articulo-articulo')#contenido_noticia
	body2= clean(' '.join([t.get_text() for t in body[0].find_all(['p','h2'])]))



