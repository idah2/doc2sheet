#!/usr/bin/env python

'''
    File name: doc2sheet.py
    Author: Daniel Story
    Date created: 2/5/2019
    Date last modified: 2/8/2019
    Python Version: 2.7, 3
'''

import sys, pandas
from bs4 import BeautifulSoup

filename=str(sys.argv[1])
rows = []

def main():
	with open(filename, "r") as file:

		html = file.read()
		soup = BeautifulSoup(html, "html.parser")

		base = "cmnt_ref"
		count = 1
		needle = base + str(count)
		link = soup.find(id=needle)

		while (link):
			# get highlight text
			linkp = link.find_parent()
			highlight = linkp.find_previous_sibling("span")
			# get comment text
			anchor = "#" + needle
			commentAnchor = soup.find("a", href=anchor)
			comment = commentAnchor.find_next("span")
			# get class that indicates theme
			classes = highlight.attrs
			className = classes["class"][-1]
			# get chapter of highlight
			highlightp = highlight.find_parent()
			prev = highlightp.find_previous_siblings("p")
			for i in prev:
				child = i.findChild("span", {'class': 'c16'})
				if (child):
					chapter = child.text
					break
			
			# store information and add to array
			newdict = dict()
			newdict.update({'chapter': chapter,'category': className, 'text': highlight.text, 'comment': comment.text})
			rows.append(newdict)
			print("Row " + str(count) + " saved.")

			# augment needle and look for next highlight
			count += 1
			needle = base + str(count)
			link = soup.find(id=needle)

	# save all rows to file
	newdf = pandas.DataFrame(rows)
	with open('output.csv', 'w') as f:
		newdf.to_csv(f, columns=["chapter", "category", "text", "comment"], index=False, mode='a', header=f.tell()==0, encoding='utf-8')
		print("Done.")

if __name__ == '__main__':
  main()