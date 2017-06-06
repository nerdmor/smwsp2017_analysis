#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################################################################
#	os arquivos gerados por este script não deduplicam as palestras, devendo ser usada ferramenta externa para tal
#	felizmente, o Excel basta ;)
###########################################################################################################################

import urllib.request
import csv, time
from random import randint
from bs4 import BeautifulSoup

def parse_palestrante(div):
	try:
		link = 'http://socialmedia.8020mkt.com.br'+div.find(class_="thumb").find("a").get('href')
	except:
		link = ''

	try:
		palestrante = div.find(class_="thumb").find("span").get_text().strip()
	except:
		palestrante = ''
	
	try:
		nome = div.find(class_="subttl").get_text().strip()
	except:
		nome = ''
	
	try:
		likes = div.find(class_="quantidade").get_text().replace('likes','').strip()
	except:
		likes = ''
	
	try:
		comentarios = div.find(class_="comentarios").find("strong").get_text().strip()
	except:
		comentarios = ''
	
	extra_data = get_extra_data(link)

	exit = [nome, palestrante, link, extra_data[0], extra_data[1]]
	tags = sorted([a.lower().strip() for a in extra_data[2].split(',')])
	if len(tags) == 0:
		exit = exit + ['n/a','n/a','n/a']
	elif len(tags) == 1:
		exit = exit + [tags[0],'n/a','n/a']
	elif len(tags) == 2:
		exit = exit + [tags[0],tags[1],'n/a']
	else: 
		exit = exit + [tags[0],tags[1],tags[2]]

	exit = exit + [likes, comentarios]

	return exit

def get_extra_data(url_palestra):

	with urllib.request.urlopen(url_palestra) as response:
		soup = BeautifulSoup(response.read(), 'html.parser')
		descricao = soup.find(id='palestra').find(class_='intro').find('p').get_text().replace('\t','').replace('\n','').replace('\r','').replace(';','.').strip()
		more = soup.find(id='palestra').find(class_='palestrante-info').get_text().replace('\t','').replace('\n','').replace('\r','').replace('Biografia','').replace(';','.').strip()
		bio = more[:more.find('Linkedin')-1]
		tags = more[more.find('Tags')+4:]

	return [descricao,bio,tags]


print("Pegando lista de categorias...", end='')
with urllib.request.urlopen('http://socialmedia.8020mkt.com.br/') as response:
	soup = BeautifulSoup(response.read(), 'html.parser')
	categorias = [(obj.get_text().lower().strip(), 'http://socialmedia.8020mkt.com.br'+obj.get('href'))  for obj in soup.find(id='tagCloud').find_all('a')]
	with open('categorias.csv', 'w', newline='') as csvfile:
		categoria_writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		categoria_writer.writerow(['nome_categoria','url'])
		for cat in categorias:
			categoria_writer.writerow(cat)
print("Done!")


print("Trabalhando nas categorias...")
grabbed_talks = []

with open('palestras.csv', 'w', newline='',encoding='utf-8') as csvfile:
	palestra_writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	palestra_writer.writerow(['id','nome', 'palestrante', 'link', 'descricao', 'bio', 'tag1', 'tag2','tag3','likes','comentarios'])

	for cat in categorias:
		if str(cat[0]) != 'aaaaaaaaaaaaa':
			print("\t"+cat[0]+'...')

			with urllib.request.urlopen(cat[1]) as response:
				soup = BeautifulSoup(response.read(), 'html.parser')
				for div in soup.find_all(class_="palestrante"):
					talk_id = div.find(class_="thumb").find("a").get('href').split('/')[-1]
					print("\t\t"+talk_id+'...', end='', flush=True)
					if talk_id not in grabbed_talks:
						grabbed_talks.append(talk_id)
						palestra_writer.writerow([talk_id]+[a.encode('utf-8').decode('utf-8') for a in parse_palestrante(div)])
						print(" done!")
						sleeptime = randint(0,3)
						print('\t\t\tsleeping for '+str(sleeptime))
						time.sleep(sleeptime)
					else:
						print(" skipped!")

			print("\tdone!")
		else:
			print("\t tag inválida. Pulando...")

print("done!")


