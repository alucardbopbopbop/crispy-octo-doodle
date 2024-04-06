import openai

import pandas as pd
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle)
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER, inch
from reportlab.graphics.shapes import Line, LineShape, Drawing
from reportlab.lib.colors import Color
import textwrap


class Main():

openai.api_key = "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"


# AI recommendations
def chat_gpt(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides recommendations about an "
                                              "organization based on the provided information."},
                {"role": "user", "content": prompt}
            ]
        )
        print(response)  # Print the entire response
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred: {e}")


# Read the data from the file
data = pd.read_excel(io='/Users/sevancoe/Downloads/Documents/project_form.xlsx')

# Extract the data from the file
map = data.values
org_name = map[2][1]
description = map[3][1]
fp_or_np = map[4][1]
funding_type = map[5][1]
fp_funding_type = map[6][1]
rev_fy = map[9][1]
rev_lq = map[10][1]
employee_count = map[11][1]
fte_count = map[12][1]
fte_wages = map[13][1]
pte_count = map[14][1]
pte_wages = map[15][1]
contractor_count = map[16][1]
contractor_wages = map[17][1]
l_b_or_o = map[18][1]
rent_cost = map[19][1]
mortgage_yn = map[20][1]
mortgage_cost = map[21][1]
property_insurance = map[22][1]
property_insurance_cost = map[23][1]
utilities_cost = map[24][1]
expenses = map[25][1]
assets = map[26][1]
debt = map[27][1]
debt_payment = map[28][1]

# equations
wages = (fte_wages + pte_wages + contractor_wages) * 4
if l_b_or_o == "Both":
    lease_and_own = (rent_cost + mortgage_cost) * 12

housing_cost = (rent_cost + mortgage_cost + property_insurance_cost + utilities_cost) * 12
if mortgage_yn == "No":
    mortgage_cost = 0

if fp_or_np == "For-Profit":
    org_type_switch = False
else:
    org_type_switch = True

if funding_type == "Earned Income":
    funding_type_switch = 1
elif funding_type == "Donations":
    funding_type_switch = 2
elif funding_type == "Grants":
    funding_type_switch = 3
elif funding_type == "Investments":
    funding_type_switch = 4
else:
    funding_type_switch = 0

employee_count = fte_count + pte_count
emp_inc_ratio = rev_fy / employee_count

if property_insurance == "No":
    property_insurance_cost = 0

if debt == "No":
    debt_payment = 0

debt_cost = debt_payment * 12
total_expenses = wages + housing_cost + expenses + debt_cost
profit = rev_fy - total_expenses

profitability = ""

if profit < 0:
    profitability = "not profitable"
elif profit > 0:
    profitability = "profitable"

p_l = ""
if profit < 0:
    p_l = "loss"
elif profit > 0:
    p_l = "profit"

# AI prompt
data_input = (f"{org_name} is a {fp_or_np} organization who gets the majority of their funding via {funding_type}. The "
              f"following is a description of the organization provided by"
              f"the user: '{description}'. The organization has {assets} in assets, and {debt} in debt."
              f"they pay {wages} in wages, {housing_cost} in housing costs, and {total_expenses} in total expenses per year."
              f"In the last fiscal year, they had {rev_fy} in revenue, and were {profitability}; making {profit} in {p_l}."
              f"they have {employee_count} employees, {fte_count} of which full-time employees and {pte_count} of which "
              f"were part time. Describe the organization's financial health and provide 1 or 2 recommendations for improvement."
              f"Respond professionally in the third person.")
# print(rent_cost)

print(chat_gpt(f"{data_input}"))

# sample chart creation
chart = PieChart2D(700, 400)
chart.add_data([10, 10, 30, 200])
chart.set_pie_labels([
    'Budding Chemists',
    'Propane issues',
    'Meth Labs',
    'Attempts to escape morgage',
])
chart.download('chart.png')

# Create a PDF file
canvas = Canvas("Project_output.pdf", pagesize=letter)
canvas.Canvas.save()

canvas.drawString(72, 720, f"Analysis prepared for: {org_name}")
canvas.drawString(72, 705, "Date prepared: today lmao")
canvas.drawString(72, 690, "Date prepared: today lmao")

# saves the file to the directory

class Canvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
        self.width, self.height = LETTER

    def save(self):
        x = 128
        self.saveState()
        self.setStrokeColorRGB(0, 0, 0)
        self.setLineWidth(0.5)
        self.drawImage("chart.png'", self.width - inch * 8 - 5, self.height - 50, width=100, height=20,
                       preserveAspectRatio=True)
        self.line(30, 740, LETTER[0] - 50, 740)
        self.line(66, 78, LETTER[0] - 66, 78)
        self.setFont('Times-Roman', 10)
        self.restoreState()

        self.pages.append(dict(self.__dict__))
        self._startPage()

        PDFPSReporte.__init__(self)
        canvas.Canvas.save(self)

class PDFPSReporte:

    def __init__(self, path):
        self.path = path
        self.styleSheet = getSampleStyleSheet()
        self.elements = []

        self.green = Color((45.0 / 255), (166.0 / 255), (153.0 / 255), 1)
        self.blue = Color((54.0 / 255), (122.0 / 255), (179.0 / 255), 1)

        self.firstPage()
        # Build
        self.doc = SimpleDocTemplate(path, pagesize=LETTER)

    def firstPage(self):
        spacer = Spacer(30, 100)
        self.elements.append(spacer)

        psHeaderText = ParagraphStyle('Hed0', fontSize=12, alignment=TA_LEFT, borderWidth=3,
                                      textColor=self.blue)
        text = 'Title of report'
        paragraphReportHeader = Paragraph(text, psHeaderText)
        self.elements.append(paragraphReportHeader)

        spacer = Spacer(10, 250)
        self.elements.append(spacer)

        img = Image('static/chart.png', kind='proportional')
        img.drawHeight = 0.5 * inch
        img.drawWidth = 2.4 * inch
        img.hAlign = 'LEFT'
        self.elements.append(img)

        d = Drawing(500, 1)
        line = Line(-15, 0, 483, 0)
        line.strokeColor = self.green
        line.strokeWidth = 2
        d.add(line)
        self.elements.append(d)

        psDetalle = ParagraphStyle('Resume', fontSize=9, leading=14, justifyBreaks=1, alignment=TA_LEFT,
                           justifyLastLine=1)
        bigText = f"""{chat_gpt(f"{data_input}")}"""
        self.elements.append(Paragraph(bigText,psDetalle))

        self.remoteSessionTableMaker()


        text = f"""Report Generated via ....<br/>
        Client: {org_name}<br/>
        Date Generated: 23-Oct-2019<br/>
        Contact info: sevancoe@uw.edu<br/>
        """
        paragraphReportSummary = Paragraph(text, psDetalle)
        self.elements.append(paragraphReportSummary)
        self.elements.append(PageBreak())

    def remoteSessionTableMaker(self):
        psHeaderText = ParagraphStyle('Hed0', fontSize=12, alignment=TA_LEFT, borderWidth=3, textColor=self.blue)
        text = 'Table '
        paragraphReportHeader = Paragraph(text, psHeaderText)
        self.elements.append(paragraphReportHeader)

        spacer = Spacer(10, 22)
        self.elements.append(spacer)
        """
        Create the line items
        """
        d = []
        textData = ["col 1", "col 2", "col 3", "col 4", "col 5"]

        fontSize = 8
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER)
        for text in textData:
            ptext = "<font size='%s'><b>%s</b></font>" % (fontSize, text)
            titlesTable = Paragraph(ptext, centered)
            d.append(titlesTable)

        data = [d]
        lineNum = 1
        formattedLineData = []

        alignStyle = [ParagraphStyle(name="01", alignment=TA_CENTER),
                      ParagraphStyle(name="02", alignment=TA_LEFT),
                      ParagraphStyle(name="03", alignment=TA_CENTER),
                      ParagraphStyle(name="04", alignment=TA_CENTER),
                      ParagraphStyle(name="05", alignment=TA_CENTER)]

        for row in range(10):
            lineData = [str(lineNum), "Miércoles, 11 de diciembre de 2019",
                        "17:30", "19:24", "1:54"]
            # data.append(lineData)
            columnNumber = 0
            for item in lineData:
                ptext = "<font size='%s'>%s</font>" % (fontSize - 1, item)
                p = Paragraph(ptext, alignStyle[columnNumber])
                formattedLineData.append(p)
                columnNumber = columnNumber + 1
            data.append(formattedLineData)
            formattedLineData = []

        # Row for total
        totalRow = ["Total de Horas", "", "", "", "30:15"]
        for item in totalRow:
            ptext = "<font size='%s'>%s</font>" % (fontSize - 1, item)
            p = Paragraph(ptext, alignStyle[1])
            formattedLineData.append(p)
        data.append(formattedLineData)

        # print(data)
        table = Table(data, colWidths=[50, 200, 80, 80, 80])
        tStyle = TableStyle([  # ('GRID',(0, 0), (-1, -1), 0.5, grey),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ("ALIGN", (1, 0), (1, -1), 'RIGHT'),
            ('LINEABOVE', (0, 0), (-1, -1), 1, self.blue),
            ('BACKGROUND', (0, 0), (-1, 0), self.green),
            ('BACKGROUND', (0, -1), (-1, -1), self.blue),
            ('SPAN', (0, -1), (-2, -1))
        ])
        table.setStyle(tStyle)
        self.elements.append(table)

    def draw_wrapped_line(canvas, text, length, x_pos, y_pos, y_offset):
        """
        :param canvas: reportlab canvas
        :param text: the raw text to wrap
        :param length: the max number of characters per line
        :param x_pos: starting x position
        :param y_pos: starting y position
        :param y_offset: the amount of space to leave between wrapped lines
        """
        if len(text) > length:
            wraps = textwrap.wrap(text, length)
            for x in range(len(wraps)):
                canvas.drawCenteredString(x_pos, y_pos, wraps[x])
                y_pos -= y_offset
            y_pos += y_offset  # add back offset after last wrapped line
        else:
            canvas.drawCenteredString(x_pos, y_pos, text)
        return y_pos
