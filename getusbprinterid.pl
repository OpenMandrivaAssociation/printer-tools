#!/usr/bin/perl

open FILE, "$ARGV[0]" or die;

my $result;
# Calculation of IOCTL function 0x84005001 (to get device ID string):
# len = 1024
# IOCNR_GET_DEVICE_ID = 1
# LPIOC_GET_DEVICE_ID(len) = _IOC(_IOC_READ, 'P', IOCNR_GET_DEVICE_ID, len)
# _IOC(), _IOC_READ as defined in /usr/include/asm/ioctl.h

ioctl(FILE, 0x84005001, $result) or die;
close FILE;

# Cut resulting string to its real length
my $length = ord(substr($result, 1, 1)) + (ord(substr($result, 0, 1)) << 8);
$result = substr($result, 2, $length-2);

# Remove non-printable characters
$result =~ tr/[\x0-\x1f]/\./;
print "$result\n";
