# Netbyte

![Version 0.5](http://img.shields.io/badge/version-v0.5-orange.svg)
![Python 2.7](http://img.shields.io/badge/python-2.7-blue.svg)
![MIT License](http://img.shields.io/badge/license-MIT%20License-blue.svg)
[![sc0tfree Twitter](http://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Follow)](https://twitter.com/sc0tfree)

Netbyte is a Netcat-style tool that facilitates probing proprietary TCP and UDP services.
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

## Usage

```
$ netbyte example.com 12345
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
<html>
<head><title>302 Found</title></head>
<body bgcolor="white">
<center><h1>302 Found</h1></center>
<hr><center>nginx/1.11.13</center>
</body>
</html>

3C(<) 68(h) 74(t) 6D(m) 6C(l) 3E(>) 0D 0A(\n)
3C(<) 68(h) 65(e) 61(a) 64(d) 3E(>) 3C(<) 74(t) 69(i) 74(t) 6C(l) 65(e) 3E(>) 33(3) 30(0) 32(2) 20 46(F) 6F(o) 75(u) 6E(n) 64(d) 3C(<) 2F(/) 74(t) 69(i) 74(t) 6C(l) 65(e) 3E(>) 3C(<) 2F(/) 68(h) 65(e) 61(a) 64(d) 3E(>) 0D 0A(\n)
3C(<) 62(b) 6F(o) 64(d) 79(y) 20 62(b) 67(g) 63(c) 6F(o) 6C(l) 6F(o) 72(r) 3D(=) 22 77(w) 68(h) 69(i) 74(t) 65(e) 22 3E(>) 0D 0A(\n)
3C(<) 63(c) 65(e) 6E(n) 74(t) 65(e) 72(r) 3E(>) 3C(<) 68(h) 31(1) 3E(>) 33(3) 30(0) 32(2) 20 46(F) 6F(o) 75(u) 6E(n) 64(d) 3C(<) 2F(/) 68(h) 31(1) 3E(>) 3C(<) 2F(/) 63(c) 65(e) 6E(n) 74(t) 65(e) 72(r) 3E(>) 0D 0A(\n)
3C(<) 68(h) 72(r) 3E(>) 3C(<) 63(c) 65(e) 6E(n) 74(t) 65(e) 72(r) 3E(>) 6E(n) 67(g) 69(i) 6E(n) 78(x) 2F(/) 31(1) 2E 31(1) 31(1) 2E 31(1) 33(3) 3C(<) 2F(/) 63(c) 65(e) 6E(n) 74(t) 65(e) 72(r) 3E(>) 0D 0A(\n)
3C(<) 2F(/) 62(b) 6F(o) 64(d) 79(y) 3E(>) 0D 0A(\n)
3C(<) 2F(/) 68(h) 74(t) 6D(m) 6C(l) 3E(>) 0D 0A(\n)

Connection closed
```

## Test Server

I have included a test server to better view the functionality of netbyte. The server has two tests:
* Echo Test - echo back a user entered string
* Hex Test - send a random hexadecimal string of user-specified size

To run the test server:
```
$ python testserver.py
```
In another terminal, connect to the test server using netbyte:
```
$ netbyte localhost 12345
```

## Modifying Output Colors

To modify the color scheme, change the functions `print_ascii` and `print_hex` inside the netbyte package.
See the [colorama page](https://pypi.python.org/pypi/colorama) for color options.

## License and Contributions

Netbyte is under the MIT License.

Questions, comments and suggestions are always welcomed!

## Future Work

* Ability to enter input sent as hex
* Listen option to interact with custom-built clients
* Proper unit tests
