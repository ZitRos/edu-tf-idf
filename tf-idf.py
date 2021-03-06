#!python3

import text as text_parser
import utils
import xlsxwriter
import re


workbook = xlsxwriter.Workbook('tf-idf.xlsx')
print('Reading texts...')
all_texts = text_parser.get_text_corpus(9999, 'texts/news')
print('Done! Computing TF-IDF ranks...')
all_ranks = utils.tf_idf(all_texts)
print('\nDone! Writing results...')
text_no = 0
for dictionary in all_ranks:
	text_no += 1
	print(
		'Writing worksheet ' + str(text_no) + '/' + str(len(all_ranks))
		+ ' (' + dictionary['title'][:10] + '...)'
		, end='\r'
	)
	sheet_name = str(text_no) + ' ' + re.sub('[\[\]:*?/\\\]', '', dictionary['title'][:-1])
	worksheet = workbook.add_worksheet(sheet_name[:28] + ('...' if len(sheet_name) > 28 else ''))
	worksheet.write(0, 0, dictionary['title'])
	worksheet.write(1, 0, '#')
	worksheet.write(1, 1, 'Rank')
	worksheet.write(1, 2, 'Word')
	row = 2
	sorted_dict = sorted(dictionary['stats'].items(), key=lambda x: (x[1], x[0]), reverse=True)
	for [key, value] in sorted_dict:
		worksheet.write(row, 0, row - 1)
		worksheet.write(row, 1, value)
		worksheet.write(row, 2, key)
		row += 1
workbook.close()
print('\nDone!')
