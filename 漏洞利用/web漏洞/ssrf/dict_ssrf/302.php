<?php

$ip = $_GET['ip'];

$port = $_GET['port'];

$scheme = $_GET['s'];

$data = $_GET['data'];

header("Location: $scheme://$ip:$port/$data");

?>