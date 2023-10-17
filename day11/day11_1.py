import os
import threading


# 执行重命名
def rename_files(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        print(f"将{old_name}重命名为{new_name}")
    except Exception as e:
        print(f"重命名{old_name}失败，错误为：{e}")


# 录入重命名操作相关信息
def rename_files_information():
    aim_times = int(input("请输入你要重命名的文件数量"))
    file_renames = []
    now_times = 0

    while now_times < aim_times:
        now_times += 1
        old_name = input("请输入原文件名")
        new_name = input("请重新命名")
        tmp_tuple = (old_name, new_name)
        file_renames.append(tmp_tuple)

    return file_renames


# 使用多线程完成操作
def operate_files():
    threads = []
    for old_name, new_name in file_renames:
        thread = threading.Thread(target=rename_files, args=(old_name, new_name))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("已完成重命名操作。")


file_renames = rename_files_information()
operate_files()
