#!/usr/bin/perl

my(@tonebank, @drumset);
my(@pathlist, @patch_ext_list);
my($rcf_count);
my($def_instr_name);
my($cfg, $cfgroot);
my($MAX_AMPLIFICATION);

@pathlist = ('.');
@patch_ext_list = ('', '.pat', '.shn', '.pat.shn', '.gz', '.pat.gz');
$rcf_count = 0;
$MAX_AMPLIFICATION = 800;

if(@ARGV != 1)
{
    print STDERR "Usage: $0 cfg-file\n";
    exit 1;
}

$cfgroot = $cfg = $ARGV[0];
if($cfgroot =~ s/\/[^\/]+$//)
{
    unshift(@pathlist, $cfgroot);
}

if(&read_config_file($cfg) != 0)
{
    exit 1;
}
$rcf_count++;
&lspatch('bank', @tonebank);
&lspatch('drumset', @drumset);
exit 0;

sub read_config_file
{
    my($name) = @_;
    local(*CFG);
    my(@args, $bank, $line, $orig_name);

    if($rcf_count > 50)
    {
	print STDERR "Probable source loop in configuration files";
	return -1;
    }

    $orig_name = $name;
    undef $_;
    if(!($name = &open_file(*CFG, $name)))
    {
	return -1;
    }
    undef $_;

    $line = 0;
    while(<CFG>)
    {
	$line++;

	s/^\s+|\r?\n$//;

	@args = split(/[ \t\r\n\240]+/, $_);
	next if @args == 0 || $args[0] =~ /^$|^#/;

	if($args[0] eq 'dir')
	{
	    if(@args < 2)
	    {
		print STDERR "$name: line $line: No directory given\n";
		return -2;
	    }
	    shift @args;
	    map(s/\/+$//, @args);
	    unshift(@pathlist, reverse(@args));
	}
	elsif($args[0] eq 'source')
	{
	    if(@args < 2)
	    {
		print STDERR "$name: line $line: No file name given\n";
		return -2;
	    }
	    shift @args;
	    for(@args)
	    {
		my($status);
		$rcf_count++;
		print "source $_\n";
		$status = &read_config_file($_);
		$rcf_count--;
		if($status != 0)
		{
		    return $status;
		}
	    }
	}
	elsif($args[0] eq 'default')
	{
	    if(@args < 2)
	    {
		print STDERR "$name: line $line: Must specify exactly one patch name\n";
		return -2;
	    }
	    $def_instr_name = $args[1];
	}
	elsif($args[0] eq 'drumset')
	{
	    my($i);

	    if(@args < 2)
	    {
		print STDERR "$name: line $line: No drum set number given\n";
		return -2;
	    }
	    $i = $args[1];
	    if($i < 0 || $i > 127)
	    {
		print STDERR "$name: line $line: Drum set must be between 0 and 127\n";
		return -2;
	    }
	    if(! defined $drumset[$i])
	    {
		$drumset[$i] = [];
	    }
	    $bank = $drumset[$i];
	}
	elsif($args[0] eq 'bank')
	{
	    my($i);
	    if(@args < 2)
	    {
		print STDERR "$name: line $line: No bank number given\n";
		return -2;
	    }
	    $i = $args[1];
	    if($i < 0 || $i > 127)
	    {
		print STDERR "$name: line $line: Tone bank must be between 0 and 127\n";
		return -2;
	    }
	    if(! defined $tonebank[$i])
	    {
		$tonebank[$i] = [];
	    }
	    $bank = $tonebank[$i];
	}
	else
	{
	    my($i, $patch);

	    if(@args < 2 || $args[0] !~ /^[0-9]/)
	    {
		print STDERR "$name: line $line: syntax error\n";
		return -2;
	    }

	    $i = shift @args;
	    $patch = shift @args;
	    if($i < 0 || $i > 127)
	    {
		printf STDERR "$name: line $line: Program must be between 0 and 127\n";
		return -2;
	    }

	    if(! defined $bank)
	    {
		print STDERR "$name: line $line: Must specify tone bank or drum set before assignment\n";
		return -2;
	    }

	    for(@args)
	    {
		my($x, $y) = split(/=/, $_, 2);

		if($x eq 'amp')
		{
		    if($y < 0 || $y > $MAX_AMPLIFICATION || $y !~ /^[0-9]/)
		    {
			print STDERR "$name: line $line: amplification must be between 0 and $MAX_AMPLIFICATION\n";
			return -2;
		    }
		}
		elsif($x eq 'note')
		{
		    if($y < 0 || $y > 127 || $y !~ /^[0-9]/)
		    {
			print STDERR "$name: line $line: note must be between 0 and 127\n";
			return -2;
		    }
		}
		elsif($x eq 'pan')
		{
		    my($k);
		    if($y eq 'center')
		    {
			$k = 64;
		    }
		    elsif($y eq 'left')
		    {
			$k = 0;
		    }
		    elsif($y eq 'right')
		    {
			$k = 127;
		    }
		    else
		    {
			$k = int(($y + 100) * 100 / 157);
		    }
		    if($k < 0 || $k > 127 ||
		       ($k == 0 && $y !~ /^[0-9\-]/))
		    {
			print STDERR "$name: line $line: panning must be left, right, center, or between -100 and 100\n";
			return -2;
		    }
		}
		elsif($x eq 'keep')
		{
		    if($y ne 'env' && $y ne 'loop')
		    {
			print STDERR "$name: line $line: keep must be env or loop\n";
			return -2;
		    }
		}
		elsif($x eq 'strip')
		{
		    if($y ne 'env' && $y ne 'loop' && $y ne 'tail')
		    {
			print STDERR "$name: line $line: strip must be env, loop, or tail\n";
			return -2;
		    }
		}
		elsif($x eq 'comm')
		{
		    ;
		}
		else
		{
		    print STDERR "$name: line $line: bad patch option\n";
		    return -2;
		}
	    }

	    $bank->[$i] = ["$name:$line", $patch, @args];
	}
    }

    close(CFG);
    return 0;
}

sub open_file
{
    local(*fiz) = shift;
    my($fname) = shift;

    if($fname =~ /^\//)
    {
	if(open(*fiz, $fname))
	{
	    return $fname;
	}
	return 0;
    }

    for(@pathlist)
    {
	return "$_/$fname" if open(*fiz, "$_/$fname");
    }

    print STDERR "$fname: $!\n" if $rcf_count == 0;
    return 0;
}

sub lspatch
{
    my($tag, @insts) = @_;
    my($i, $j, $bank, $p, @inst, $pos);

    for($i = 0; $i < 128; $i++)
    {
	next if !defined $insts[$i];
	$bank = $insts[$i];

	for($j = 0; $j < 128; $j++)
	{
	    next if !defined $bank->[$j];
	    $p = $bank->[$j];
	    @inst = @$p;
	    $pos = shift @inst;

#	    $p = $bank->[$j]->[1];
	    print "$tag $i $pos: $j @inst ", &find_patch($inst[0]), "\n";
	}
    }
}

sub find_patch
{
    my($f) = @_;
    local(*FIZ);
    my($realpath);

    for(@patch_ext_list)
    {
	$realpath = &open_file(*FIZ, "$f$_");
	return $realpath if $realpath;
    }

    return "-";
}
