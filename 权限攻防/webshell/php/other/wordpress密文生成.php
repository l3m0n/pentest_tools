<?php
 $password = 'abc';
 global $wp_hasher;
 if ( empty($wp_hasher) ) {
  require_once( './wp-includes/class-phpass.php');
  $wp_hasher = new PasswordHash(8, TRUE);
 }
 echo $wp_hasher->HashPassword($password);
?>