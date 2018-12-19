
import subprocess
import sys

def main():
    filenames = ['create_io_files_for_ngweight.py', 'create_vectors_of_ngram.py', 'exec_clustering.py', 'index_src.py']
    # filenames = ['create_vectors_of_ngram.py', 'exec_clustering.py', 'index_src.py']
    for filename in filenames:
        # pythonスクリプトからngweightを直接実行し、出力ファイルを得る
        cmd = "python %s" % filename
        res = subprocess.run([cmd], stdout=subprocess.PIPE, shell=True)
        sys.stdout.buffer.write(res.stdout)

if __name__ == '__main__':
    main()