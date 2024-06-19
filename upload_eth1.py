import os
import sys
import paramiko

# 取得參數
source_file = sys.argv[1]
dest_folder = "/run/media/mmcblk0p4/ftp_root/shared/"
remote_host = "10.0.0.1"

remote_port = 8822
remote_username = "root"
remote_password = "Askey+1937"

# 建立SSH連線
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(remote_host, port=remote_port, username=remote_username, password=remote_password)
# 建立SFTP連線
sftp = ssh.open_sftp()

# 上傳檔案
sftp.put(source_file, dest_folder + os.path.basename(source_file))

# 關閉SFTP連線與SSH連線
sftp.close()
ssh.close()