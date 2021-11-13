#!/usr/bin/perl --
use strict;
use CGI;
use utf8;
use JSON qw/encode_json decode_json/;
use URI::Escape;
use File::Copy qw/copy move/;
use POSIX qw(strftime);

$CGI::POST_MAX = 1024 * 1024 * 1024;

my $q = new CGI;
my $routeID = uri_unescape($q->param('POSTDATA'));

# open file
my $file = "./master_file/route_master.csv";
open my $in, "<", $file or die qq/Cannot open file "$file" : $!/;

#my $routeID = "TKSTKS";
#my $routeID = "JXTG";
#my $routeID = "DAI";
#my $routeID = "IMO";
#my $routeID = "NITB"; #21063
#my $routeID = "DAIN"; #7240
#my $routeID = "SHKY"; #4079
#my $routeID = "KYK"; #145
#my $routeID = "JFE"; #1303
#my $routeID = "ZENNO"; #192
#my $routeID = "AZUMA"; #1421
#my $routeID = "FTCO"; #205
#my $routeID = "JFECM"; #15252
#my $routeID = "YSDH"; #58
#my $routeID = "YGKK"; #6
#my $routeID = "SPILIN"; #222
#my $routeID = "TBCK"; #1106
#my $routeID = "NANI"; #39204
#my $routeID = "HANKYU"; #6
#my $routeID = "KURIRI"; #84
#my $routeID = "KOKAS"; #2249
#my $routeID = "FERSF"; #6
#my $routeID = "OCTOCT"; #10
#my $routeID = "KAGOF"; #41
#my $routeID = "TKSTKS"; #42
#my $routeID = "TFKTFN"; #72
#my $routeID = "MOK"; #735
#my $routeID = "MOLFER"; #25
#my $routeID = "SHS000SHSO"; #3192
#my $routeID = "NTG0000000"; #1456
#my $routeID = "NME"; #10
#my $routeID = "MOLDOM"; #44840
#my $routeID = "DNJF"; #7
#my $routeID = "ASKW"; #8
#my $routeID = "JAPEX"; #22
#my $routeID = "NSUNK"; #116
#my $routeID = "SRIK00SRIK"; #1027
#my $routeID = "WKCK"; #119
#my $routeID = "OGF0000OGF"; #48
#my $routeID = "ASAH"; #32096

my $seq = 0;
my $last = "";
while(my $line = <$in>){
    my @items = split(/,/, $line);
    my @routeID_arr = split(/-/, $items[0]);
    if ($routeID_arr[0] ne "" && $routeID_arr[1] ne "" && $routeID_arr[2] ne ""){
	if ($routeID_arr[0] eq $routeID && $routeID_arr[1] eq "route"){
	    if ($routeID_arr[2] > $seq){
		$seq = $routeID_arr[2];
		$last = $items[0];
	    }
	}
    }
}

#print $routeID.": ".$seq."\n";

close $in;

print "Content-Type: text/html\n\n";
print $last;
