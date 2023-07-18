import pandas as pd

data = {'name': ['John', 'Mary', 'Peter', 'Jane'],
        'age': [25, 30, 35, 40],
        'gender': ['M', 'F', 'M', 'F']}

df = pd.DataFrame(data)

new_row = {'name': 'Bob', 'age': 28, 'gender': 'M'}
# df = df.append(new_row, ignore_index=True)

print(df)