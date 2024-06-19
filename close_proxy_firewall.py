import subprocess

# 關閉 Proxy
subprocess.run(['netsh', 'winhttp', 'reset', 'proxy'])

# 關閉 Windows 防火牆
subprocess.run(['netsh', 'advfirewall', 'set', 'allprofiles', 'state', 'off'])

# 關閉 Windows Defender 病毒與威脅防護
subprocess.run(['powershell', '-command', 'Set-MpPreference -DisableRealtimeMonitoring $true'])

# 關閉第三方防火牆（需以系統管理員身份執行）
#subprocess.run(['net', 'stop', 'firewall'])