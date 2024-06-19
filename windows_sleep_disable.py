import subprocess

# 設定電源模式為「高效能」
subprocess.run(['powercfg', '-setactive', '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'])

# 設定電腦不進入睡眠
subprocess.run(['powercfg', '-change', 'monitor-timeout-ac', '0'])
subprocess.run(['powercfg', '-change', 'monitor-timeout-dc', '0'])
subprocess.run(['powercfg', '-change', 'standby-timeout-ac', '0'])
subprocess.run(['powercfg', '-change', 'standby-timeout-dc', '0'])
subprocess.run(['powercfg', '-change', 'hibernate-timeout-ac', '0'])
subprocess.run(['powercfg', '-change', 'hibernate-timeout-dc', '0'])
