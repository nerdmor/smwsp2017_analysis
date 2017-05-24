#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from bs4 import BeautifulSoup

def find_match(palestra, tag1, tag2):
	tag_list = [palestra[0], palestra[1], palestra[2]]
	if tag1 in tag_list and tag2 in tag_list:
		return 1
	else:
		return 0

def has_tag(palestra, tag):
	tag_list = [palestra[0], palestra[1], palestra[2]]
	if tag in tag_list:
		return 1
	else:
		return 0



#pegando categorias
with open('categorias.csv', newline='') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
	tag_list = [row[0].lower() for row in csvreader]
	tag_list_2 = tag_list


# pegando palestras
with open('palestras_withoutBOM.csv', newline='') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
	palestras = [row for row in csvreader]


# fazendo saida
with open('cruzamentos.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	writer.writerow(['cat/cat'] + tag_list + ['total linha'])



	exit = []
	i1 = 0
	for tag1 in tag_list:
		print("tag: " + tag1)
		row = [tag1]
		total_row = 0
		for tag2 in tag_list_2:
			sumlist = 0
			for p in palestras:
				sumlist += find_match(p, tag1, tag2)
				total_row += has_tag(p, tag1)
			row += [sumlist]

		writer.writerow(row+[total_row])

