import sys
import pathlib
import argparse

def main():
    parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る


    # 3. parser.add_argumentで受け取る引数を追加していく
    parser.add_argument('path_input', help='Path to the Test case File.')    # 必須の引数を追加
    parser.add_argument('path_python', help='Path to the python file.')

    args = parser.parse_args()    # 4. 引数を解析

    print('arg1='+args.path_input)
    print('arg2='+args.path_python)

if __name__ == '__main__':
    main()
