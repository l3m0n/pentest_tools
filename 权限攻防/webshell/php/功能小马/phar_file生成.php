<?php
$p = new PharData(dirname(__FILE__).'/phar.zip', 0,'phar',Phar::ZIP) ; 
$p->addFromString('testfile.txt', '<?php phpinfo();?>'); 
?>