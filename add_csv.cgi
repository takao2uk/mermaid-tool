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

# back up files
my $today = strftime "%Y%m%d_%H%M%S", localtime;
my $file0 = "./master_file/changelog.log";
my $file1 = "./master_file/seapt_master.csv";
my $file2 = "./master_file/route_master.csv";
my $file3 = "./master_file/accesslist.csv";
my $backup1 = "./master_file/seapt_master_{$today}.csv";
my $backup2 = "./master_file/route_master_{$today}.csv";
my $backup3 = "./master_file/accesslist_{$today}.csv";
copy ($file1, $backup1) or die "Cannot copy \"$file1\" to \"$backup1\": $!";;
copy ($file2, $backup2) or die "Cannot copy \"$file2\" to \"$backup2\": $!";;
copy ($file3, $backup3) or die "Cannot copy \"$file3\" to \"$backup3\": $!";;

# write new data
open my $out0, ">>", $file0;
open my $out1, ">>", $file1;
open my $out2, ">>", $file2;
open my $out3, ">", $file3;

#my $seapt_csv = encode_json($data->[0]);
my $seapt_csv = $data->[0];
#my $route_csv = encode_json($data->[1]);
my $route_csv = $data->[1];
my $accesslist = $data->[2];
my $log_msg = $data->[3];

print $out0 $log_msg."\n";
#print $out1 substr($seapt_csv,1,-1)."\n";
print $out1 $seapt_csv."\n";
#print $out2 substr($route_csv,1,-1)."\n";
print $out2 $route_csv."\n";
for my $line (@$accesslist){
    print $out3 join(",", @$line)."\n";
}

close $out0;
close $out1;
close $out2;
close $out3;

print "Content-Type: text/html\n\n";
print "ROUTE OK";
