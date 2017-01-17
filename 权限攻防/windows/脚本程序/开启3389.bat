echo Windows Registry Editor Version 5.00>>3389.reg 
echo [HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server]>>3389.reg 
echo "fDenyTSConnections"=dword:00000000>>3389.reg 
echo [HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server\Wds\rdpwd\Tds\tcp]>>3389.reg 
echo "PortNumber"=dword:00000d3d>>3389.reg 
echo [HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp]>>3389.reg 
echo "PortNumber"=dword:00000d3d>>3389.reg 
regedit /s 3389.reg 
del 3389.reg