from requests import get as requests_get
from re import search as re_search
from bs4 import BeautifulSoup as besoup

import filehandle

hostname = 'http://manganel.com'

def get_data_from_manganel(link):
	HTML = requests_get(link).text
	source = besoup(HTML, 'lxml')
	title = source.find('title').text.split('Manga')[0].split('Read')[1].strip()
	chapters = source.find(class_='chapter-list').find_all('a')
	num = len(chapters)
	print('\n-> Detect\nWeb:', hostname, '\nManga: ', title, '\nChaps:', num)
	data = []
	for chap in chapters:
		tempData = {}
		tempData['href'] = chap['href']
		tempData['title'] = chap.contents[0]
		data.append(tempData)
	return data

def save_img_from_manganel(data):
	print('Title:', data['title'], '\nLink:', data['href'])
	filename = '-'.join(data['title'].split())
	HTML = requests_get(data['href']).text
	source = besoup(HTML, 'lxml')
	links = map(lambda x: x['src'], source.find(id='vungdoc').find_all('img'))
	files = []
	print('{}\nDownloading...'.format('-' * 50))
	for no, link in enumerate(links, 1):
		fileExtension = link.split('.')[-1]
		try:
			name = filename + '-' + str(no) + '.' + fileExtension
			files.append(filehandle.download_file(link, name))
			print('Loaded', name, 'Successfully!')
		except KeyboardInterrupt:
			exit()
		except:
			print('Missed %r' %(filename + '-' + str(no) + '.' + fileExtension))
	print('Zipping...')
	filehandle.zip_file(files, filename + '-' + "manganel.com" + '.zip')
	print('Done!')