import pandas as pd


# Read the data from the file
data = pd.read_excel(io = '/Users/sevancoe/Downloads/Documents/project_form.xlsx')

map = data.head().values
revenue = map[0][1]
expenses = map[1][1]
taxes = map[2][1]
text = map[3][1]

print(revenue + expenses + taxes)
print(text)


#usecols = 'B'