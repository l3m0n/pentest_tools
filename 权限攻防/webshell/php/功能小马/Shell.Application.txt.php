<?php 
$wsh = new COM('Shell.Application') or die("Shell.Application"); 
$exec = $wsh->open("c:\\windows\\system32\\notepad.exe"); 
//没有回显，多了个notepad进程，可以写一个批处理来运行dos命令。open换用ShellExecute 也可。 
?> 