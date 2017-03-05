To fetch directory contents using Java, you'll need to use the FTP tool to setup
a fake FTP server and send the contents of the directory as the FTP username. 

To start, host the DTD file on your server, update the xml file to point to this location, and
upload the XML file to the vulnerable server. The server will fetch the remote DTD file
and send the directory contents as an FTP username.
