# ======================================================================
#  Project : FTPRobot for Automatic replication of Builds to Remote Servers using FTP 
#
# NAME: <FTPWizard.pl>
#
#c
# DATE  : 3/25/2003
#
# PURPOSE: <The only sure shot way to get that important FTP done>
#
# ======================================================================
use strict;
use Net::FTP;                                         # allows FTP control
use File::Path;                                       # provides the mkpath function
use Win32::NetResource;                               # allows connection to a network share
use Net::SMTP;                                        # allows smtp protocol 
use Net::Ping;
#use Acme::Comment;
use File::Find;
use File::Path;
use Fcntl;
use FileHandle;


my ($ProductName,$LocalPath,$RemotePath,$RemoteServerName,$RemoteServerIP,$LoginName,$PassWord,$BuildType,$Folder2Upload,$StartMailTo,$StartMailCc,$FinishMailTo,$FinishMailCc,$DistressMailTo,$DistressMailCc,$MisereturFile,$BuildNumber,@Order)= ReadParameters();
my $file;
my @tmp = @Order;
my $retrycount =0;

my ($x,$y);
for ($x=0; $x <= $#tmp; $x++)
{
 $file = $LocalPath."\\".$Folder2Upload."\\".$tmp[$x];
 my $size= stat($file) ?(stat(_))[7]:(0);
 $size = ($size / 1024)/1024;
 $size =~ /(.*\.\d\d\d)/;
 $size = $1;
 $y = $x + 1; 
 
 $tmp[$x] = "$y \. $tmp[$x]	Size : $size MB";
 
 print "$tmp[$x]\n";
}

my $Priority =  join "\n",@tmp;
$Priority = "\n\n".$Priority;

my $ftp;

my $Start_Time =scalar(localtime);
sendmail("Initiated",$ProductName,$StartMailTo,$StartMailCc,$BuildType,$Folder2Upload,$LocalPath,$RemotePath,$RemoteServerName,$RemoteServerIP,$Priority,$BuildNumber,$Start_Time);

Connect();

my $End_time =scalar(localtime);
sendendmail("Completed",$ProductName,$FinishMailTo,$FinishMailCc,$BuildType,$Folder2Upload,$LocalPath,$RemotePath,$RemoteServerName,$RemoteServerIP,$Priority,$BuildNumber,$Start_Time,$End_time );


sub Connect
{
		if ($ftp = Net::FTP->new($RemoteServerIP ,Debug => 1, Timeout =>99999))
		{
			print "FTP Session with $RemoteServerName ($RemoteServerIP) opened...\n";
		
		}
		else
		{
			print "Could not open session with $RemoteServerName ($RemoteServerIP) ! Retrying...\n";
			sleep(20);
			$retrycount++;
			if ($retrycount > 300)
			{
			 $retrycount =0;
			 sendmail("In Trouble - Link Failure",$ProductName,$DistressMailTo,$DistressMailCc,$BuildType,$Folder2Upload,$LocalPath,$RemotePath,$RemoteServerName,$RemoteServerIP,$Priority);
			} 
			Connect();
		}
				
		if($ftp->login($LoginName,$PassWord))
		{
			print "User $LoginName Logged into $RemoteServerName...\n";
		}
		else
		{
			print "Could not Log on to $RemoteServerName ($RemoteServerIP) !!!\n";
			print "Please recheck Login info => User : $LoginName, Pswd : $PassWord\n";
			exit();
		}		

		$ftp->binary;
				
		$ftp->hash("1","4096");
		
		MakeHierarchy(@Order);
		
		$ftp->cwd($RemotePath);
		
		FTPFiles(@Order);
		
		$MisereturFile =~ /.*\\(.*)/;
		
		$ftp->ascii;
		
		$ftp->put($MisereturFile,"/SCMDropBox/FTPRobot/$1");
		
		$ftp->quit;
		
}		
		

sub ReadParameters
{
	 my $var;
	 my @dirList;
	 my $count = 0;
	 my ($ProductName,$LocalPath,$RemotePath,$RemoteServerName,$RemoteServerIP,$LoginName,$PassWord,$BuildType,$Folder2Upload,$StartMailTo,$StartMailCc,$FinishMailTo,$FinishMailCc,$DistressMailTo,$DistressMailCc,$BuildNumber,$Priority);
	 
	 
	 open (InFile,$ARGV[0])||die "\nfile not found :( !!!\n";
	 print "\nfile found :)...proceeding...\n\n";
	
	  while (<InFile>)
	  {
		    $count++;
		    /.*?:(.*)/;                      
		    $var = $1;                    	#put the value after the colon in the variable
		    $var =~ s/^\s+//;
		    $var =~ s/\s+$//;				#remove leading and trailing spaces
		    chomp $var;
		    SWITCH : 
		    {
		    	if ($count==1){$ProductName			= $var ; print "Product	: $var\n" ;last SWITCH ; }
		    	if ($count==2){$LocalPath			= $var ; print "Local Path	: $var\n" ;last SWITCH ; }
		    	if ($count==3){$RemotePath			= $var ; print "Remote Path	: $var\n" ;last SWITCH ; }
				if ($count==4){$RemoteServerName	= $var ; print "Remote Server	: $var\n" ;last SWITCH ; }
				if ($count==5){$RemoteServerIP		= $var ; print "Remote IP	: $var\n" ;last SWITCH ; }
				if ($count==6){$LoginName			= $var ; print "Login Name	: $var\n" ;last SWITCH ; }
				if ($count==7){$PassWord			= $var ; print "Login Password	: $var\n" ;last SWITCH ; }
				if ($count==8){$BuildType			= $var ; print "Build Type	: $var\n" ;last SWITCH ; }
			
				if ($count==9)
				{
					$Folder2Upload	= $var ; 
					print "Build Number	: $var\n";
		
					if ($Folder2Upload eq "LatestBuild")
					{
						opendir(SOURCE,$LocalPath);
						my $name;	
						while($name = readdir(SOURCE))
						{                                  #read each item in directory
							next if $name=~/^(\.|\.\.)$/;  #skip the . and .. in the directory listing
							next if $name=~/archive/i;
							next if $name=~/TruCoverage/i;
							push(@dirList,$name);
						}
					
						close SOURCE;
						
						$Folder2Upload=$dirList[$#dirList];
						print "Latest Build	: $Folder2Upload\n";
			
					}
				}
				
				if ($count==10){$StartMailTo	= $var ; print "Init Mail To	: $var\n";last SWITCH; }
				if ($count==11){$StartMailCc = $var ; print "Init Mail Cc	: $var\n";last SWITCH; }
				if ($count==12){$FinishMailTo	= $var ; print "Finish Mail To	: $var\n";last SWITCH; }
				if ($count==13){$FinishMailCc = $var ; print "Finish Mail Cc	: $var\n";last SWITCH; }
			 	if ($count==14){$DistressMailTo = $var ; print "Distress Mail To	: $var\n";last SWITCH; }
			 	if ($count==15){$DistressMailCc = $var ; print "Distress Mail Cc	: $var\n";last SWITCH; }
			 	if ($count==16){$Priority = $var ; last SWITCH; }
			 	if ($count==17){$BuildNumber = $var ; print "Build Number	:$var\n";last SWITCH; }
			 	if ($count==18){$MisereturFile = $var ; print "Miseretur File	:$var\n";last SWITCH; }
			 	
			 	
			 }
		}	
		
	my ($x,$temp);
	my ($otherfiles, $priorityfiles, $alreadyThere);

	my @Order = split /;/,$Priority;
	for ($x=0; $x <= $#Order; $x++) #remove trailing\leading white spaces
	{
	 $Order[$x] =~ s/^\s+//;
	 $Order[$x] =~ s/\s+$//;
	}

	my @NormalOrder;
	find (sub {push @NormalOrder,$File::Find::name unless ((-d $File::Find::name)||($_ eq '.DS_Store'));},"$LocalPath\\$Folder2Upload");
	
	for ($x=0; $x <= $#NormalOrder; $x++)
	{
	 $NormalOrder[$x] =~ s/\//\\/g;
	 $temp = "$LocalPath\\$Folder2Upload";
	 $temp = quotemeta $temp;
	 $NormalOrder[$x] =~ s/$temp\\//g;
	}
	
	my @CopyOfOrder = @Order;

	foreach $otherfiles (@NormalOrder)
	{
	 	$alreadyThere = 0;
	 	
	 	foreach $priorityfiles (@CopyOfOrder)
	 	{
	  		if ($otherfiles eq $priorityfiles)
	  		{
	   			$alreadyThere = 1;
	  		}
	 	}
	 	
	 	if (!($alreadyThere))
	 	{
	 	 push @Order, $otherfiles;
	    }
	}     

 	 
   return ($ProductName,$LocalPath,$RemotePath,$RemoteServerName,$RemoteServerIP,$LoginName,$PassWord,$BuildType,$Folder2Upload,$StartMailTo,$StartMailCc,$FinishMailTo,$FinishMailCc,$DistressMailTo,$DistressMailCc,$MisereturFile,$BuildNumber,@Order);
}

sub MakeHierarchy()
{
 my @Order = @_;
 my $dir;
 foreach $dir(@Order)
 {
	 $dir =~ /(.*)\\/;
	
	 $dir = "/".$RemotePath."/".$Folder2Upload."/".$1;
	 
	 $dir =~ s/\\/\//g;
	
	 my $t =  $ftp->mkdir($dir,1)||Connect();
	 print "Creating Folder : $t\n";
 } 
}

sub FTPFiles()
{
 my @Order = @_;
 my ($file,$localfile,$remotefile);

 foreach $file(@Order)
 {
	  $localfile = $LocalPath."\\".$Folder2Upload."\\".$file;
	  $file =~ s/\\/\//g;
	  $remotefile = "/".$RemotePath."/".$Folder2Upload."/".$file; 
	   
	 my $ftpsize = $ftp->size("$remotefile");
	 
	 my $localsize= stat($localfile) ?(stat(_))[7]:(0);
	 
	 if(($ftpsize != $localsize)||($localsize == 0))
	  {

		 print "\n\nUploading $localfile...\nAs $remotefile\n\n";

		 sysopen(FH, $localfile, O_RDONLY);
	     binmode(FH);
	     sysseek(FH, $ftpsize, 0);
		 
		 $ftp->append(\*FH,$remotefile)||Connect();
		 print $ftp->message, "\n";

	}
	 else
	  {
	   print "File $file already exists...\n";
	  }   
 }	  
}


sub sendmail()
{

 my ($status,$ProductName,$MailTo,$MailCc,$BuildType,$Folder2Upload,$LocalPath,$RemotePath,$RemoteServerName,$RemoteServerIP,$Priority,$BuildNumber,$Start_Time,$End_time ) = @_;
 print "\nSending $status Mail...\n";
 my @To = split /;/, $MailTo;
 my @Cc = split /;/, $MailCc;
 push @To,@Cc;
 print "\nTo : @To\n";

 my $source = $LocalPath."\\".$Folder2Upload;

 my $destination = "ftp://$RemoteServerName/$RemotePath/$Folder2Upload";
 
 my $subject = "FTP $status Alert for $ProductName (Build : $BuildNumber) to $RemoteServerName ($RemoteServerIP)";
 
 my $time =scalar(localtime);
 
 my $body = "
			<html>
			
			<head>
			</head>
			
			<body>
			
			<p><font face=\"Transl Eur Bold\"><b><font SIZE=\"3\" COLOR=\"#ff0000\">IMPORTANT</font></b><font SIZE=\"3\" color=\"#FF0000\">:
			</font><font SIZE=\"3\" COLOR=\"\#0000ff\">
			</font><font SIZE=\"3\">This information is for internal authorized use only. The
			information provided below is restricted to those who received this e-mail. Do
			not re-distribute this e-mail in any form or show the items mentioned below to
			any other **** employee unless authorization has been given to do so. Help
			maintain security and do not treat this request casually.</font></font></p>
			<pre><font face=\"Arial Black\">Product			: $ProductName (Build : $BuildNumber)</font></pre>
			<pre><font face=\"Arial Black\">Transfer Source		: <a href=\"$source\">$source</a></font></pre>
			<pre><font face=\"Arial Black\">Transfer Destination	: <a href=\"$destination\">$destination</a></font></pre>
			<pre><font face=\"Arial Black\">Remote Server		: $RemoteServerName($RemoteServerIP)</font></pre>
			<pre><font face=\"Arial Black\">Transfer Order		: <span style=\"background-color: \#99CCFF\">$Priority</span></font></pre>
			<pre><font face=\"Arial Black\">Transfer Status		: <font color=\"#800080\">$status</font></font></pre>
			<pre><font face=\"Arial Black\">Initiation Time		: <font color=\"#800080\">$Start_Time IST</font></font></pre>
			<pre><b>Regards,</b></pre>
			<pre><font face=\"Monotype Corsiva\" color=\"#000080\"><b>**** FTPRobot</b></font></pre>
			<p>&nbsp;</p>
			<p>&nbsp;</p>
			<p>&nbsp;</p>
			
			</body>
			
			</html>";
 my $smtp;
 while(!($smtp=Net::SMTP->new('10.91.0.200')))
 {
  sleep 10;
  print "\ncould not establish connection with saraswati to send mail...retrying...\n";
 } 
 $smtp->mail('ftprobot@****.com')||print "$!";

 $smtp->to(@To)||print "$!";
 $smtp->data();
 $smtp->datasend("Content-type: text/html\n");
 $smtp->datasend("From: FTPRobot\@****\.com\n");
 $smtp->datasend("To: $MailTo\n");
 $smtp->datasend("Cc: $MailCc\n");
 $smtp->datasend("Subject: $subject\n");
 $smtp->datasend("Date: ".scalar(gmtime));
 $smtp->datasend("\n$body\n");
 $smtp->dataend();
 $smtp->quit;
 print "\nmail sent...\n";
}


sub sendendmail()
{

 my ($status,$ProductName,$MailTo,$MailCc,$BuildType,$Folder2Upload,$LocalPath,$RemotePath,$RemoteServerName,$RemoteServerIP,$Priority,$BuildNumber,$Start_Time,$End_time ) = @_;
 print "\nSending $status Mail...\n";
 my @To = split /;/, $MailTo;
 my @Cc = split /;/, $MailCc;
 push @To,@Cc;
 print "\nTo : @To\n";

 my $source = $LocalPath."\\".$Folder2Upload;

 my $destination = "ftp://$RemoteServerName/$RemotePath/$Folder2Upload";
 
 my $subject = "FTP $status Alert for $ProductName (Build : $BuildNumber) to $RemoteServerName ($RemoteServerIP)";
 
 my $time =scalar(localtime);
 
 my $body = "
 			<html>
 			
 			<head>
 			</head>
 			
 			<body>
 			
 			<p><font face=\"Transl Eur Bold\"><b><font SIZE=\"3\" COLOR=\"#ff0000\">IMPORTANT</font></b><font SIZE=\"3\" color=\"#FF0000\">:
 			</font><font SIZE=\"3\" COLOR=\"\#0000ff\">
 			</font><font SIZE=\"3\">This information is for internal authorized use only. The
 			information provided below is restricted to those who received this e-mail. Do
 			not re-distribute this e-mail in any form or show the items mentioned below to
 			any other **** employee unless authorization has been given to do so. Help
 			maintain security and do not treat this request casually.</font></font></p>
 			<pre><font face=\"Arial Black\">Product			: $ProductName (Build : $BuildNumber)</font></pre>
 			<pre><font face=\"Arial Black\">Transfer Source		: <a href=\"$source\">$source</a></font></pre>
 			<pre><font face=\"Arial Black\">Transfer Destination	: <a href=\"$destination\">$destination</a></font></pre>
 			<pre><font face=\"Arial Black\">Remote Server		: $RemoteServerName($RemoteServerIP)</font></pre>
 			<pre><font face=\"Arial Black\">Transfer Order		: <span style=\"background-color: \#99CCFF\">$Priority</span></font></pre>
 			<pre><font face=\"Arial Black\">Transfer Status		: <font color=\"#800080\">$status</font></font></pre>
 			<pre><font face=\"Arial Black\">Initiation Time		: <font color=\"#800080\">$Start_Time IST</font></font></pre>
 			<pre><font face=\"Arial Black\">Completion Time		: <font color=\"#800080\">$time IST</font></font></pre>
 			<pre><b>Regards,</b></pre>
 			<pre><font face=\"Monotype Corsiva\" color=\"#000080\"><b>**** FTPRobot</b></font></pre>
 			<p>&nbsp;</p>
 			<p>&nbsp;</p>
 			<p>&nbsp;</p>
 			
 			</body>
 			
 			</html>";
 
 my $smtp;
 while(!($smtp=Net::SMTP->new('*************')))
 {
  sleep 10;
  print "\ncould not establish connection with saraswati to send mail...retrying...\n";
 } 
 $smtp->mail('ftprobot@****.co.in')||print "$!";

 $smtp->to(@To)||print "$!";
 $smtp->data();
 $smtp->datasend("Content-type: text/html\n");
 $smtp->datasend("From: FTPRobot\@****\.com\n");
 $smtp->datasend("To: $MailTo\n");
 $smtp->datasend("Cc: $MailCc\n");
 $smtp->datasend("Subject: $subject\n");
 $smtp->datasend("Date: ".scalar(gmtime));
 $smtp->datasend("\n$body\n");
 $smtp->dataend();
 $smtp->quit;
 print "\nmail sent...\n";
}