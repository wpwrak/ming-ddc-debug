#!/usr/bin/perl
use Net::TFTPd;

sub type
{
	local ($rq) = @_;

	my $op = $rq->{'_REQUEST_'}{'OPCODE'};
	return "READ" if $op eq 1;
	return "WRITE" if $op eq 2;
	return sprintf("0x%x", $op);
}


my $tftpd = Net::TFTPd->new('RootDir' => '.', 'Writable' => 1) ||
    die "Error creating TFTPd listener: ", Net::TFTPd->error;

my $rq = $tftpd->waitRQ(3600*100) ||
    die "Error waiting for TFTP request: ", Net::TFTPd->error;

printf "%s %s\n", type($rq), $rq->getFileName();

$rq->processRQ() ||
    die "Error processing TFTP request: ", Net::TFTPd->error;

printf "%u bytes has been transferred\n", $rq->getTotalBytes() || 0;
