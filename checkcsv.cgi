#!/usr/bin/perl --
use strict;
use CGI;
use utf8;
use JSON qw/encode_json decode_json/;
use URI::Escape;
use File::Copy qw/copy move/;
use POSIX qw(strftime);

$CGI::POST_MAX = 1024 * 1024 * 1024;

# read from webpages
my $q = new CGI;
my $json_in = uri_unescape($q->param('POSTDATA'));
#my $json_in = '[["PORTC_TOK_130,b,c","PORTC_TOK_132,bbb,ccc"],["WKCK-route-0064,aaa,SEARGN_TSS_4,0,SEARGN_TSS_4,0,1,-,SEARGN_TSS_4,SEARGN_TSS_4","WKCO-route-0065,bbb,SEARGN_TSS_4,0,SEARGN_TSS_4,0,1,-,SEARGN_TSS_4,SEARGN_TSS_4"]]';
#my $json_in = '[["QQQ,b,c","aaa,bbb,ccc"],["AAA,aaa,SEARGN_TSS_4,0,SEARGN_TSS_4,0,1,-,SEARGN_TSS_4,SEARGN_TSS_4","DDD,bbb,SEARGN_TSS_4,0,SEARGN_TSS_4,0,1,-,SEARGN_TSS_4,SEARGN_TSS_4"]]';
my $data = decode_json($json_in);
my $seapt_csv = $data->[0];
my $route_csv = $data->[1];


# master files
my $file1 = "./master_file/seapt_master.csv";
my $file2 = "./master_file/route_master.csv";

# open files
open my $out1, "<", $file1;
open my $out2, "<", $file2;

# read files
my @seapts = [];
while (my $line = <$out1>){
    chomp $line;
    push (@seapts, $line);
}
my @routes = [];
while (my $line = <$out2>){
    chomp $line;
    push (@routes, $line);
}

# close files
close $out1;
close $out2;



#check if there is an existing entries
my $ids = "";
my $flg = 0;

for my $line (@$seapt_csv){
    my @items = [];
    @items = split(/,/, $line);
    #print ($items[0]."\n");
    my @found = grep {/$items[0]/} @seapts;
    my $num = @found;
    if ($num != 0){
	$flg = 1;
	$ids = $ids.$items[0].",";
    }
}

for my $line (@$route_csv){
    my @items = [];
    @items = split(/,/, $line);
    #print ($items[0]."\n");
    my @found = grep {/$items[0]/} @routes;
    my $num = @found;
    if ($num != 0){
	$flg = 1;
	$ids = $ids.$items[0].",";
    }
}

if ($flg != 0){
    my $txt = "Duplicate entry is found:".$ids.".";
    print "Content-Type: text/html\n\n";
    print $txt;
} else {
    print "Content-Type: text/html\n\n";
    print "0";
}
