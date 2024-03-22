import pandas as pd


# Read the data from the file
data = pd.read_excel(io = '/Users/sevancoe/Downloads/Documents/project_form.xlsx',
                     dtype = {'revenue': int, 'expenses':int})
print(data)

map = data.head().values
print(map)

print(map[0])
revenue = map[0][1]
expenses = map[1][1]
print(revenue)
print(expenses)


#usecols = 'B'