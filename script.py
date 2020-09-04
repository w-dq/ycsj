import json
import re
from xhtml2pdf import pisa 
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from xhtml2pdf.default import DEFAULT_FONT

ROOT = "/mnt/sda1/spider/"
DATA_ROOT = ROOT +"data/"

# Utility function
def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")
# pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result, encoding='UTF-8')
    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file, encoding='UTF-8')           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return False on success and True on errors
    return pisa_status.err


def Pre_text(question,path):
	try:
		stem = re.sub(r'src=\"', "src=\"/mnt/sda1/spider/data/"+path+"img/", question['stem'])
	except Exception as e:
		stem = "IS EMPTY"

	try:
		options = list()
		for op in question['options']:
			opt = re.sub(r'src=\"', "src=\"/mnt/sda1/spider/data/"+path+"img/", op)
			options.append(opt)
	except Exception as e:
		options = "IS EMPTY"
	
	try:
		answer = re.sub(r'src=\"', "src=\"/mnt/sda1/spider/data/"+path+"img/", question['answer'])
	except Exception as e:
		answer = "IS EMPTY"

	try:
		knowledge = re.sub(r'src=\"', "src=\"/mnt/sda1/spider/data/"+path+"img/", question['knowledge'])
	except Exception as e:
		knowledge = "IS EMPTY"

	try:
		analysis = re.sub(r'src=\"', "src=\"/mnt/sda1/spider/data/"+path+"img/", question['analysis'])
	except Exception as e:
		analysis = "IS EMPTY"
	
	
	
	return stem,options,answer,knowledge,analysis


def Present(question,path):
	stem,options,answer,knowledge,analysis = Pre_text(question,path)
	message = """
	<html>
	<head></head>
	<body>
	<p>STEM</p>
	<p>%s</p>
	<p>OPTIONS</p>
	<p>%s</p>
	<p>ANSWER</p>
	<p>%s</p>
	<p>KNOWLEDGE</p>
	<p>%s</p>
	<p>ANALYSIS</p>
	<p>%s</p>
	</body>
	</html>"""%(stem,options,answer,knowledge,analysis)
	print(message)
	convert_html_to_pdf(message.encode('utf-8'), 'out.pdf')
	return 0


ROOT = "/mnt/sda1/spider/"
DATA_ROOT = ROOT +"data/"

publisher = input("which publisher:")
semester = input("which semester:")
chapter = input("which chapter:")
section = input("which section:")

INFO_FILE = DATA_ROOT +"info_" + publisher + "_" + semester + ".json"
Q_LIST_DIR = DATA_ROOT + publisher + "/" + semester + "/" + chapter + "/" + section + "/"

with open(INFO_FILE) as in_f:
	info = json.load(in_f)

children = info[int(chapter)]["children"][int(section)]["children"]

count = 0
# tag = 0

for c in children:
	c_total = c["total"]
	c_no = c["no"]
	if not(c_total):
		continue
	c_curr = c["curr"]
	for i in range(c_curr):
		PROB_FILE = Q_LIST_DIR + str(c_no) + "/" + str(i+1) + "/question.json"
		path = publisher + "/" + semester + "/" + chapter + "/" + section +"/" + str(c_no) + "/" + str(i+1) + "/"
		with open(PROB_FILE) as ques_file:
			questions = json.load(ques_file)
		for idx,question in enumerate(questions):
			item = dict()
			print("============ start! ============")
			item["path"] = path
			item["index"] = idx
			print("------ path: %s ------"%path)
			print("----------- index: %d -----------"%idx)
			Present(question,path)
			label = input("get label: ")
			item["label"] = label
			print(item)
			print("============= end! =============")
			count += 1
			file_tag = publisher + "-" + semester + "-" + chapter + "-" + section + "-" + str(c_no) + "-" + str(i+1) + ":" + str(idx)
			OUT_FILE = "label/%s.json"%file_tag
			with open(OUT_FILE, "w", encoding="utf-8") as fh:
				json.dump(item, fh, ensure_ascii=False)


print("############ end of list #############")
print(count)



# with open(OUT_FILE, "w", encoding="utf-8") as fh:
#     json.dump(re_list, fh, ensure_ascii=False)