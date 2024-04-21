import openai
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Image, Spacer, Table, TableStyle)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import inch
from reportlab.graphics.shapes import Line, Drawing
from reportlab.lib.colors import Color
from matplotlib import pyplot as plt
from datetime import datetime

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
expenses = map[25][1]*4
assets = map[26][1]
debt = map[27][1]
debt_payment = map[28][1]

todays_date = datetime.today().strftime('%m-%d-%Y')

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
              f"were part time. Describe the organization's financial health and provide recommendations for improvement."
              f"Respond professionally in the third person.")

response = (chat_gpt(f"{data_input}"))

# common things
fontSize = 8
green = Color((45.0 / 255), (166.0 / 255), (153.0 / 255), 1)
blue = Color((54.0 / 255), (122.0 / 255), (179.0 / 255), 1)
spacer = Spacer(10, 10)
headerStyle = ParagraphStyle('Hed0', fontSize = 14, alignment = TA_LEFT, borderWidth = 2, textColor = blue)
paragraphStyle = ParagraphStyle('Resume', fontSize = 11, leading = 14, justifyBreaks = 1, alignment = TA_LEFT,justifyLastLine = 1)
tableStyle = TableStyle([
    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
    ("ALIGN", (1, 0), (1, -1), 'RIGHT'),
    ('LINEABOVE', (0, 0), (-1, -1), 1, blue),
    ('BACKGROUND', (0, 0), (-1, 0), green),
    ('BACKGROUND', (0, -1), (-1, -1), blue),
    ('SPAN', (0, -1), (-2, -1))
])

# DISPLAY PREP
# Creating total expense chart
totalExpensesDataSet = ['Wages', 'Housing costs', 'Expenses', 'Debt']
wagesInt = wages
housingInt = housing_cost
expensesInt = expenses
debtInt = debt_cost
totalExpenseData = [wagesInt, housingInt, expensesInt, debtInt]
fig = plt.figure(figsize = (12, 9))
plt.pie(totalExpenseData, labels = totalExpensesDataSet, textprops = {'fontsize': 30}, autopct = '%1.1f%%', startangle = 140)
plt.savefig('totalExpense.png')

# -----------------------------------------------------------------------------------------------
# Create PDF
doc = SimpleDocTemplate("Project_output.pdf", pagesize = letter)
elements = []

# Title
elements.append(Paragraph(f"{org_name} Analysis", headerStyle))
elements.append(spacer)
elements.append(Paragraph(f"Prepared on: {todays_date}", paragraphStyle))
elements.append(spacer)

# draw line
d = Drawing(500, 1)
line = Line(-15, 0, 483, 0)
line.strokeColor = green
line.strokeWidth = 2
d.add(line)
elements.append(d)
elements.append(spacer)

# table data
elements.append(Paragraph('Annual Employment Data', headerStyle))
elements.append(spacer)
elements.append(spacer)

d = []
textData = ["Employment Type", "Full Time", "Part Time", "Contractors", "TOTAL"]

centered = ParagraphStyle(name = "centered", alignment = TA_CENTER)
for text in textData:
    d.append(Paragraph("<font size='%s'><b>%s</b></font>" % (fontSize, text), centered))

data = [d]
formattedLineData = []
alignStyle = [ParagraphStyle(name = "01", alignment = TA_CENTER), ParagraphStyle(name = "02", alignment = TA_CENTER), ParagraphStyle(name = "03", alignment = TA_CENTER),
              ParagraphStyle(name = "04", alignment = TA_CENTER), ParagraphStyle(name = "05", alignment = TA_CENTER)]

# add row 1 data
total_count = fte_count + pte_count + contractor_count
lineData = ["Employed Persons", f"{fte_count}", f"{pte_count}", f"{contractor_count}", f"{total_count}"]
columnNumber = 0
for item in lineData:
    formattedLineData.append(Paragraph("<font size='%s'>%s</font>" % (fontSize - 1, item), alignStyle[columnNumber]))
    columnNumber = columnNumber + 1
data.append(formattedLineData)
formattedLineData = []

# add row 2 data
total_salary = (fte_wages + pte_wages + contractor_wages )*4
lineData = ["Wages Paid", f"${fte_wages*4}", f"${pte_wages*4}", f"${contractor_wages*4}", f"${total_salary}"]
columnNumber = 0
for item in lineData:
    formattedLineData.append(Paragraph("<font size='%s'>%s</font>" % (fontSize - 1, item), alignStyle[columnNumber]))
    columnNumber = columnNumber + 1
data.append(formattedLineData)
formattedLineData = []

# add row 3 data
lineData = ["Average wages paid per person", "-", "-", "-", f"${total_salary/total_count}"]
columnNumber = 0
for item in lineData:
    formattedLineData.append(Paragraph("<font size='%s'>%s</font>" % (fontSize - 1, item), alignStyle[columnNumber]))
    columnNumber = columnNumber + 1
data.append(formattedLineData)
formattedLineData = []

table = Table(data, colWidths=[100, 80, 80, 80, 80])
table.setStyle(tableStyle)
elements.append(table)
elements.append(spacer)

# AI output formatted
elements.append(Paragraph('Advice ', headerStyle))
elements.append(spacer)
elements.append(Paragraph(response, paragraphStyle))
elements.append(spacer)

# add total expense image
img = Image('totalExpense.png', kind = 'proportional')
img.drawHeight = 2 * inch
img.drawWidth = 3 * inch
img.hAlign = 'LEFT'
elements.append(Paragraph('Expenses', headerStyle))
elements.append(spacer)
elements.append(img)

doc.build(elements)
