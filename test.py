import pdfkit
from xhtml2pdf import pisa             # import python module
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from xhtml2pdf.default import DEFAULT_FONT

message = """
<html>
<head></head>
<body>
<p>中文</p>
</body>
</html>"""


# pdfmetrics.registerFont(TTFont('yh', 'msyh.ttf'))
# DEFAULT_FONT['helvetica'] = 'yh'

# Utility function
def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html.encode('UTF-8'),                # the HTML to convert
            dest=result_file,encoding='UTF-8')           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return False on success and True on errors
    return pisa_status.err

convert_html_to_pdf(message, 'out.pdf')