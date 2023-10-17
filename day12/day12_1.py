import pandas as pd

df = pd.read_csv('data.csv')

print("Original Data:")
print(df)

df.drop('Salary', axis=1, inplace=True)

print("\nData after removing 'Salary' column:")
print(df)

john_alice_salary_sum = df[df['Name'].isin(['John', 'Alice'])]['Salary'].sum()

print(f"\nTotal Salary for John and Alice: {john_alice_salary_sum}")
