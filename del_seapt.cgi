#!/usr/bin/perl --
use strict;
use CGI;
use utf8;
use JSON qw/encode_json decode_json/;
use URI::Escape;
use File::Copy qw/copy move/;
use POSIX qw(strftime);

$CGI::POST_MAX = 1024 * 1024;

my $q = new CGI;
my $json_in = uri_unescape($q->param('POSTDATA'));
my $data = decode_json($json_in);

# back up file
my $today = strftime "%Y%m%d_%H%M%S", localtime;
my $file1 = "./master_file/accesslist.csv";
my $file2 = "./master_file/seapt_master.csv";
my $file3 = "./master_file/changelog.log";
my $backup1 = "./master_file/accesslist_{$today}.csv";
my $backup2 = "./master_file/seapt_master_{$today}.csv";
copy ($file1, $backup1) or die "Cannot copy \"$file1\" to \"$backup1\": $!";;
copy ($file2, $backup2) or die "Cannot copy \"$file2\" to \"$backup2\": $!";;


# write new data
open my $out1, ">", $file1;
open my $out2, ">", $file2;
open my $out3, ">>", $file3;

my $accesslist = $data->[0];
my $seapt_master = $data->[1];
my $log_msg = $data->[2];

for my $line (@$accesslist){
    print $out1 join(",", @$line)."\n";
}

for my $line (@$seapt_master){
    print $out2 join(",", @$line)."\n";
}

print $out3 $log_msg."\n";

print "Content-Type: text/html\n\n";
print "OK OK OK";

close $out1;
close $out2;
close $out3;




