import argparse
import pandas as pd

def main(args):
    # 读取CSV文件
    df = pd.read_csv(args.path)

    # 显示原始数据
    print("Original Data:")
    print(df)

    # 删除指定列
    if args.number is not None:
        if args.number in df.columns:
            df.drop(args.number, axis=1, inplace=True)
            print(f"Data after removing '{args.number}' column:")
            print(df)
        else:
            print(f"Column '{args.number}' not found in the CSV file.")

    # 选择 "John" 和 "Alice" 行并执行相加操作
    john_alice_rows = df[df['Name'].isin(['John', 'Alice'])]
    if not john_alice_rows.empty:
        john_alice_salary_sum = john_alice_rows['Salary'].sum()
        print(f"\nTotal Salary for John and Alice: {john_alice_salary_sum}")
    else:
        print("No 'John' and 'Alice' rows found in the CSV file.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process CSV data")
    parser.add_argument("--path", required=True, help="Path to the CSV file")
    parser.add_argument("--number", help="Name of the column to be removed")

    args = parser.parse_args()
    main(args)
