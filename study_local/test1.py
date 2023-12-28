import os

path = r'/home/study'
count = 0

for root, dir, file in os.walk(path):
    count += 1

    print(f'------------------------------第'
          f'{count}次循环--------------------------\n')
    print('根目录', root)
    print('文件夹列表', dir)
    print('文件列表', file)
