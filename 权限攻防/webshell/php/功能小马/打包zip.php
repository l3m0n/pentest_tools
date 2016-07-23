<?php
function addFileToZip($path,$zip){
    $handler=opendir($path); //打开当前文件夹由$path指定。
    while(($filename=readdir($handler))!==false){
        if($filename != "." && $filename != ".."){//文件夹文件名字为'.'和‘..’，不要对他们进行操作
            if(is_dir($path."/".$filename)){// 如果读取的某个对象是文件夹，则递归
                addFileToZip($path."/".$filename, $zip);
            }else{ //将文件加入zip对象
                $zip->addFile($path."/".$filename);
            }
        }
    }
    @closedir($path);
}


$zip=new ZipArchive();
if($zip->open('images.zip', ZipArchive::OVERWRITE)=== TRUE){
    addFileToZip('/home/neirongo/lanboke.info/wp-content/themes/wp-Qzero/', $zip); //调用方法，对要打包的根目录进行操作，并将ZipArchive的对象传递给方法
    $zip->close(); //关闭处理的zip文件
}
?>