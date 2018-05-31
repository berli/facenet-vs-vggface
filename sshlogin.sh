#!/usr/bin/expect                                                               
set username [lindex $argv 0]  
set password [lindex $argv 1]
set ip [lindex $argv 2]

spawn ssh $username@$ip
expect "*password:"
send "$password\r"
expect "*#"
interact
