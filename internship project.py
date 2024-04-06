import openai

import pandas as pd
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

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


# Create a PDF file
# canvas = Canvas("Project_output.pdf", pagesize = letter)
# canvas.setFont("Times-Roman", 12)
# canvas.drawString(72, 720, f"Analysis prepared for: {org_name}")
# canvas.drawString(72, 705, "Date prepared: today lmao")
# canvas.drawString(72, 690, "Date prepared: today lmao")


# saves the file to the directory
# canvas.save()
