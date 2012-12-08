#!/usr/bin/perl -w

sub treatfile
{

  my $deletethis;
  my $readval;
  my $manufacturer;
  my $manuflinefound = 0;
  my $manufvalid;
  my $havemanuf;
  my $model;
  my $modellinefound;
  my $modelvalid;
  my $kap;

  $kap = "";
  $manufacturer = "";
  $deletethis = 0;

  print "$_[0] ... ";


  #
  # Read file for the first time to get manufacturer info and to check
  # whether it should be deleted
  #

  # open file
  if (!(open(PPDFILE,"< $_[0]"))) {
    print STDERR "Can't open PPD file: $_[0]\n";
    return(0);
  }
  # read data
  $manufvalid = 0;
  $manuflinefound = 0;
  while (defined($readval = <PPDFILE>)) {
    # Remove "Birmy PowerRIP" PPD files (they are for the commercial 
    # Birmy Power RIP software PostScript interpreter (Windows/Mac)
    if (($readval =~ /birmy/) ||
        ($readval =~ /Birmy/) ||
        ($readval =~ /BIRMY/)) {$deletethis = 1;}
    # Search for manufacturer tag
    if ($readval =~ /^\*Manufacturer:\s*"(.*)"\s*$/)
    {
      $manufacturer = $1;
      $manuflinefound = 1;
      $manufvalid = 1;
      if (($readval =~ /"Manufacturer"/) || ($readval =~ /"ESP"/)) 
        {$manufvalid = 0};
    }
  }
  # close file
  close(PPDFILE);    

  # delete file and stop if a deletion criteria is fulfilled
  if ($deletethis == 1) {
    print ("Deleted\n");
    system("rm -f $_[0]");
    return(0);
  }

  $havemanuf = $manufvalid;
  
  #
  # Read file for the second time to get model info
  #

  if (($havemanuf == 0) && ($manufvalid == 0)) {
    # open file
    if (!(open(PPDFILE,"< $_[0]"))) {
      print STDERR "Can't open PPD file: $_[0]\n";
      return(0);
    }
    # read data
    $modelvalid = 0;
    while (defined($readval = <PPDFILE>)) {
      if ($readval =~ /^\*ModelName:\s*"(.*)"\s*$/)
      {
        $model=$1;
        $modelvalid = 1;
        if (($model eq "Model") || ($readval eq "model")) {$modelvalid = 0};
      }
    }
    # close file
    close(PPDFILE);    

    # Extract manufacturers name
    if ($modelvalid == 0) { $manufacturer="UNKNOWN MANUFACTURER"
    } else {
      @sep = split(/ /,$model);
      $manufacturer = $sep[0];
    }
  }

  #
  # Rewrite file to insert manufacturer info
  #

  # open file to read
  if (!(open(PPDFILE,"< $_[0]"))) {
    print STDERR "Can't open PPD file: $_[0]\n";
    return(0);
  }
  # open file to write
  if (!(open(NPPDFILE,"> $_[0].new"))) {
    print STDERR "Can't open new PPD file: $_[0].new\n";
    return(0);
  }
  # read data
  while (defined($readval = <PPDFILE>)) {
    if (substr($readval, 0, 14) eq "*Manufacturer:") {
      $manuflinefound = 1;
      print NPPDFILE "*Manufacturer: \"$manufacturer\"\n"
    } else {
      print NPPDFILE $readval;
    }
    if ((substr($readval, 0, 4) ne "*PPD") && 
	(substr($readval, 0, 2) ne "*%")){
      if ($manuflinefound == 0) {
	 $manuflinefound = 1;
         print NPPDFILE "*Manufacturer: \"$manufacturer\"\n"
      }
    }
  }
  # close files
  close(PPDFILE);    
  close(NPPDFILE);
  # move new file onto place of old file
  system("mv -f $_[0].new $_[0]");
  # Compress the file
  system("gzip $_[0]");
  print("Processed\n");
  return(0);
}

# main program

{
   treatfile($ARGV[0]);  
}
