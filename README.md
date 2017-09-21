# Netbyte

![Version 1.0](http://img.shields.io/badge/version-v1.0-orange.svg)
![Python 2.7](http://img.shields.io/badge/python-2.7-blue.svg)
![MIT License](http://img.shields.io/badge/license-MIT%20License-blue.svg)
[![sc0tfree Twitter](http://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Follow)](https://twitter.com/sc0tfree)

Netbyte is a Netcat-style tool that facilitates manual probing, fuzzing and exploitation of TCP and UDP services.
It is lightweight, fully interactive and provides formatted output in both hexadecimal and ASCII.

## Why

When testing proprietary or custom-written services on pentests, I’ve frequently been disappointed while trying to reverse engineer 
these protocols.

In the past, this has been done using netcat with wireshark and/or hexdump.
However, due to truncation issues with using hexdump (i.e.: `nc domain.com 1234 | hexdump -C`)
and wireshark’s tedious process, I decided to create Netbyte as quick and easy alternative when opening unknown ports.

## Install

Clone the git:
```
git clone https://github.com/sc0tfree/netbyte.git
```
Enter the directory:
```
cd netbyte
```
Run setup.py script with 'install':
```
python setup.py install
```

## Basic Usage

```
$ netbyte example.com 12345
Connection Established
������!��'
FF FB 01 FF FB 03 FF FD 21(!) FF FD 27(')


Enter your user id:
0D 0A(\n)
0D 0A(\n)
45(E) 6E(n) 74(t) 65(e) 72(r) 20 79(y) 6F(o) 75(u) 72(r) 20 75(u) 73(s) 65(e) 72(r) 20 69(i) 64(d) 3A(:) 20 07
admin
user password:
61(a) 64(d) 6D(m) 69(i) 6E(n) 0D 0A(\n)
75(u) 73(s) 65(e) 72(r) 20 70(p) 61(a) 73(s) 73(s) 77(w) 6F(o) 72(r) 64(d) 3A(:) 20
admin

Invalid user or password

Connection closed
```
You can also pipe input into netbyte:
```
$ echo "GET /" | netbyte test.com 80
Connection Established
<html>
<head><title>302 Found</title></head>
<body bgcolor="white">
<center><h1>302 Found</h1></center>
<hr><center>nginx/1.13.4</center>
</body>
</html>

3C(<) 68(h) 74(t) 6D(m) 6C(l) 3E(>) 0D 0A(\n)
3C(<) 68(h) 65(e) 61(a) 64(d) 3E(>) 3C(<) 74(t) 69(i) 74(t) 6C(l) 65(e) 3E(>) 33(3) 30(0) 32(2) 20 46(F) 6F(o) 75(u) 6E(n) 64(d) 3C(<) 2F(/) 74(t) 69(i) 74(t) 6C(l) 65(e) 3E(>) 3C(<) 2F(/) 68(h) 65(e) 61(a) 64(d) 3E(>) 0D 0A(\n)
3C(<) 62(b) 6F(o) 64(d) 79(y) 20 62(b) 67(g) 63(c) 6F(o) 6C(l) 6F(o) 72(r) 3D(=) 22 77(w) 68(h) 69(i) 74(t) 65(e) 22 3E(>) 0D 0A(\n)
3C(<) 63(c) 65(e) 6E(n) 74(t) 65(e) 72(r) 3E(>) 3C(<) 68(h) 31(1) 3E(>) 33(3) 30(0) 32(2) 20 46(F) 6F(o) 75(u) 6E(n) 64(d) 3C(<) 2F(/) 68(h) 31(1) 3E(>) 3C(<) 2F(/) 63(c) 65(e) 6E(n) 74(t) 65(e) 72(r) 3E(>) 0D 0A(\n)
3C(<) 68(h) 72(r) 3E(>) 3C(<) 63(c) 65(e) 6E(n) 74(t) 65(e) 72(r) 3E(>) 6E(n) 67(g) 69(i) 6E(n) 78(x) 2F(/) 31(1) 2E 31(1) 33(3) 2E 34(4) 3C(<) 2F(/) 63(c) 65(e) 6E(n) 74(t) 65(e) 72(r) 3E(>) 0D 0A(\n)
3C(<) 2F(/) 62(b) 6F(o) 64(d) 79(y) 3E(>) 0D 0A(\n)
3C(<) 2F(/) 68(h) 74(t) 6D(m) 6C(l) 3E(>) 0D 0A(\n)

Connection closed
```

## Manual Fuzzing and Exploitation

Netbyte is able to send evaluated Python expressions by using `!!` at the beginning of any input. This is useful for manual fuzzing and even exploitation.

*Note: using `!!` mode does not automatically include a newline (\n) in the string to send.*

### Newlines

To include a newline automatically at the end of an evaluated expression, use `!!!` at the beginning of any input.

### Examples:
| Expression | Result |
|:-----------|:-------|
| `!! "A" * 250` | Send 250 A's |
| `!! "\x65" * 250` | Send 250 A's |
| `!! "A" * 250 + "\n"` | Send 250 A's and a newline ('\n')|
| `!!! "A" * 250` | Send 250 A's and a newline ('\n') |
| `!!! "abc" * 2 + "def"` | Send 'abcabcdef' and a newline ('\n') |


Let's see it in action by crashing a PCMan FTP Server:
```
$ netbyte pcmanserver.com 21
Connection Established
220 PCMan's FTP Server 2.0 Ready.

32(2) 32(2) 30(0) 20 50(P) 43(C) 4D(M) 61(a) 6E(n) 27(') 73(s) 20 46(F) 54(T) 50(P) 20 53(S) 65(e) 72(r) 76(v) 65(e) 72(r) 20 32(2) 2E 30(0) 20 52(R) 65(e) 61(a) 64(d) 79(y) 2E 0D 0A(\n)

USER anonymous
331 User name okay, need password.

33(3) 33(3) 31(1) 20 55(U) 73(s) 65(e) 72(r) 20 6E(n) 61(a) 6D(m) 65(e) 20 6F(o) 6B(k) 61(a) 79(y) 2C(,) 20 6E(n) 65(e) 65(e) 64(d) 20 70(p) 61(a) 73(s) 73(s) 77(w) 6F(o) 72(r) 64(d) 2E 0D 0A(\n)

!!! "PASS " + "A" * 6400
230 User logged in

32(2) 33(3) 30(0) 20 55(U) 73(s) 65(e) 72(r) 20 6C(l) 6F(o) 67(g) 67(g) 65(e) 64(d) 20 69(i) 6E(n) 0D 0A(\n)

```

*The exploit for this buffer overflow can be found [here](https://www.exploit-db.com/exploits/27277/).*

## Test Server

Netbyte includes a built-in test server to better view its functionality.

The server has three tests:

* Echo Test - server echoes back a user-specified string
* Display Hex Test - server sends a string of random bytes with user-specified length
* Byte Count Test - server counts number of input bytes sent from client

To run the test server on default port 12345:
```
$ netbyte --testserver
```
In another terminal, connect to the test server using netbyte:
```
$ netbyte localhost 12345
```

## License and Contributions

Netbyte is under the MIT License.

Questions, comments and suggestions are always welcomed!

## Future Work

* Listen option to interact with custom-built clients
* Proper unit tests
