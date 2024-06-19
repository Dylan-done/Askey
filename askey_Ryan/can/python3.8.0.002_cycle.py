import time
import subprocess

while True:
    subprocess.Popen(["python3.8.0.002.py"])  # 執行檔案
    time.sleep(10)  # 等待10秒
    subprocess.Popen(["pkill", "-f", "python3.8.0.002.py"])  # 關閉檔案

    time.sleep(120)  # 等待120秒後再次執行迴圈