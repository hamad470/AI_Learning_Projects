import pandas as pd

# Example DataFrame
data = None
data = {'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'Los Angeles', 'Chicago']}

df = pd.DataFrame(data)

# Access the first row

df =df.set_index("Name")
# Access the rows for 'Alice' and 'Charlie' by label
alice_row = df.loc["Alice"]

print(alice_row)

