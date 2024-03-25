import pandas as pd


# Read the data from the file
data = pd.read_excel(io = '/Users/sevancoe/Downloads/Documents/project_form.xlsx')

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
    org_type_switch = 1
else:
    org_type_switch = 0

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

print(rent_cost)

