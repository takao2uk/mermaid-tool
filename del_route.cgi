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
my $json_in = uri_unescape($q->param('POSTDATA'));
my $data = decode_json($json_in);

# back up file
my $today = strftime "%Y%m%d_%H%M%S", localtime;
my $file1 = "./master_file/route_master.csv";
my $file2 = "./master_file/changelog.log";
my $backup1 = "./master_file/route_master_{$today}.csv";
copy ($file1, $backup1) or die "Cannot copy \"$file1\" to \"$backup1\": $!";;

# write new data
open my $out1, ">", $file1 or die qq/Cannot open file "$file1" : $!/;
open my $in1, "<", $backup1 or die qq/Cannot open file "$file1" : $!/;
open my $out2, ">>", $file2 or die qq/Cannot open file "$file1" : $!/;

my $delId = $data->[0];
my $log_msg = $data->[1];

#print $out1 join(",", @$route_master)."\n";

while(my $line = <$in1>){
    if ($line !~ /$delId/){
	print $out1 $line;
    }
}

print $out2 $log_msg."\n";

close $out1;
close $in1;
close $out2;

print "Content-Type: text/html\n\n";
print "ROUTE OK";





