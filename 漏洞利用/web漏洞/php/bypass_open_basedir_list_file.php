<?php
printf('<b>open_basedir : %s </b><br />', ini_get('open_basedir'));
$file_list = array();
// normal files
$it = new DirectoryIterator("glob:///home/*");
foreach ($it as $f) {
	$file_list[] = $f->__toString();
}
// special files (starting with a dot(.))
$it = new DirectoryIterator("glob:///.*");
foreach ($it as $f) {
	$file_list[] = $f->__toString();
}
sort($file_list);
foreach ($file_list as $f) {
	echo "{$f}<br/>";
}
?>