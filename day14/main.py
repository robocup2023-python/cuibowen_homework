import concurrent.futures
import os
import time
import pandas as pd


# 装饰器用于记录程序运行时间
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 运行时间: {end_time - start_time} 秒")
        return result
    return wrapper


# 统计单词数量的函数
def count_words_in_file(filename):
    word_count = {}
    with open(filename, 'r') as file:
        for line in file:
            words = line.split()
            for word in words:
                word = word.strip('.,!?()[]{}"\'')
                if word:
                    if word in word_count:
                        word_count[word] += 1
                    else:
                        word_count[word] = 1
    return word_count


# 处理单个文件的函数
def process_file(filename):
    print(f"处理文件: {filename}")
    word_count = count_words_in_file(filename)
    return word_count


# 主函数
@timing_decorator
def main():
    input_dir = 'test'  # 指定要处理的文件夹
    output_file = 'word_count.csv'

    filenames = [os.path.join(input_dir, filename) for filename in os.listdir(input_dir) if filename.endswith('.txt')]

    # 使用进程池和线程池
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as process_pool:
        results = list(process_pool.map(process_file, filenames))

    # 合并单词计数
    combined_word_count = {}
    for result in results:
        for word, count in result.items():
            if word in combined_word_count:
                combined_word_count[word] += count
            else:
                combined_word_count[word] = count

    # 将结果保存到CSV文件
    df = pd.DataFrame(list(combined_word_count.items()), columns=['Word', 'Count'])
    df.to_csv(output_file, index=False)


if __name__ == "__main__":
    main()
