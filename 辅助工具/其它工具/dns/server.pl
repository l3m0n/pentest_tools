#!/usr/bin/perl

use strict;
use warnings;
use Net::DNS::Nameserver;
use Fcntl qw/ :flock /;

my $ttl      = 3600;
my $respIp   = '10.1.2.3';   # this is the ip address that all dns requests will point to
my $logFile  = 'dns.log';    # all requests will get logged to this file
my $verbose  = 0;
my $user     = 1000;         # the user to run as, script must start by root
my $bindIp   = '127.0.0.1';
my $bindPort = 53;

sub reply_handler {
    my ($qname, $qclass, $qtype, $peerhost, $query, $conn) = @_;
    my ($rcode, @ans, @auth, @add);

    if ($qtype eq "A") {
        my ($ttl, $rdata) = ($ttl, $respIp);
	my $rr = new Net::DNS::RR("$qname $ttl $qclass $qtype $rdata");
	push @ans, $rr;
	$rcode = "NOERROR";
    } elsif ($qname eq "foo.example.com") {
	$rcode = "NOERROR";
    } else {
	$rcode = "NXDOMAIN";
    }

    # log the request
    log_request($peerhost, $qname);

    # mark the answer as authoritive by setting 'aa' flag
    return ($rcode, \@ans, \@auth, \@add, { aa => 1 });
}

sub log_request {
    my ($ip, $name) = @_;
    open my $fh, '>>', $logFile or die "Can't open log file: $logFile";
    flock $fh, LOCK_EX;
    print $fh time() . ",$ip,$name\n";
    close $fh;
}


my $ns = new Net::DNS::Nameserver(
    LocalAddr    => $bindIp,
    LocalPort    => $bindPort,
    ReplyHandler => \&reply_handler,
    Verbose      => $verbose
);

$<= $> = $user;
	
$ns->main_loop;
exit(0);
