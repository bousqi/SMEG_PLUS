# SMEG+ Binaries Analysis

### vxWorks

    VxWorks (for Freescale MPC5121E ADS (Rev 0.1)) version 6.7.
This software part is stored in NAND Flash out of any filesystem.<br>
<br>

For updates, this binary is located in "TBD", with a filename **vxWorks.bin**<br>
<br>
vxWorks kernel seems to always expect for CDC_EEM devices. Thus any damage performed in file system that would brick SMEG, might be fixable if shell could be reached through CDC_EEM rather than BT Internet sharing (that requires interactions on screen).
<br>
One interesting command "**d**" allows to display memory 

	-> d 0x200000
	NOTE: memory values are displayed in hexadecimal.
	0x00200000:  9421 ffe0 7c08 02a6 9001 0024 93e1 001c  *.!..|......$....*
	0x00200010:  7c3f 0b78 907f 0008 807f 0008 4801 a445  *|?.x........H..E*

When comparing with **vxWorks.bin** file contents :

	0000h: 94 21 FF E0 7C 08 02 A6 90 01 00 24 93 E1 00 1C  
	0010h: 7C 3F 0B 78 90 7F 00 08 80 7F 00 08 48 01 A4 45 

vxWorks allows direct read to NAND Flash.

----------------

Another vxWorks **lkup** allows to find all symbols with there associated address<br>
(these dumps are totally useless as vxWorks.bin embed its own symbols)

	-> lkup "UBoot"
	UBootVersionShow          0x0024727c text     
	getUBootVersion           0x00246fe8 text     
	g_UBootVersion            0x007a14a8 data     

**vxWorks** disassembly almost complete thanks to full dump of symbols.<br>
There are three identified segments :
- [.text (all symbols)](./logs/seg_text.txt)
- [.data (all symbols)](./logs/seg_data.txt)
- [.bss (all symbols)](./logs/seg_bss.txt)

----------------
#### Binary Format
Image characteristics are :
* Base Addr : `0x00200000`
* TOC  (r2) : ~~`0x007A5F80`~~ <br>**(Problem, it points in the middle of a very large data array, an deflated bmp picture).**
* SDA (r13) : `0x0086DBB0`
<br>

Dawn ! even on the SMEG+, memory contents are the same as in the binary. My TOC at 0x007A5F80 is definitely **wrong**
```
-> d 0x007A5F80
NOTE: memory values are displayed in hexadecimal.
0x007a5f80:  d0d4 a902 1512 3355 42db 0e98 20ab 1689  *......3UB... ...*
0x007a5f90:  5a06 b40e 89a9 38fe ca04 6825 4456 dcba  *Z.....8...h%DV..*
```
Even with the help of a debug method **resShow**, the value appears incoherent: 
```
-> regsShow

r0         = 0x20004d64   sp         = 0x10306060   r2         = 0x80080148
r3         = 0x074bd320   r4         = 0x180200e0   r5         = 0x00800630
r6         = 0x51020049   r7         = 0xe1b4c940   r8         = 0x08230040
r9         = 0x84800320   r10        = 0x010671c0   r11        = 0x0294ae41
r12        = 0x8d04d604   r13        = 0x02500200   r14        = 0x810441a0
r15        = 0x00087220   r16        = 0x86031124   r17        = 0x90100086
r18        = 0x20409700   r19        = 0x82186040   r20        = 0x2d094180
r21        = 0x0812010c   r22        = 0x54641480   r23        = 0xc1c46c00
r24        = 0x12481020   r25        = 0x0084000b   r26        = 0xc0242005
r27        = 0x01190020   r28        = 0x64038841   r29        = 0x440a42b4
r30        = 0x4d000090   r31        = 0x800025c6   msr        = 0xc7248000
lr         = 0x29614514   ctr        = 0x06940921   pc         = 0xc0a04201
cr         = 0x06cc2020   xer        = 0xd00074a1   pgTblPtr   = 0xb4f80087
scSrTblPtr = 0x8d470420   srTblPtr   = 0x10200189
```

At `0x00822024` there is a Symbol Table which is made of 13853 symbols.<br>
One symbol is identified:

	struct s_Symbol
	{
	  int unk1;
	  void *name;
	  void *address;
	  int unk2;
	  int type;
	};

Type is defined as :

	enum symbolType
	{
	  unk = 0x100,
	  func = 0x400,
	  data = 0x800,
	  ext = 0x1000,
	};

With some smart scripts, the disassembly can be populated with symbol section (done).

----------------
#### Supported hardware

- Linksys WUSB54, one of the Wireless device in this list : (https://www.linksys.com/fr/search?text=WUSB54)
- CDC-EEM USB tokens (VID/PID to be listed)<br>
  RNDIS/ECM/NCM classes are not supported
- CDC-ACM
- Mass Storage (multiple volumes on same token seems to be supported)
<br>
USB to Ethernet devices supported (TBC)

		.string "ADMtek ADM8515 USB Ethernet"
		.string "ADMtek ADM8513 USB Ethernet"
		.string "ADMtek ADM8511 USB Ethernet"
		.string "D-Link DSB-650TX USB Ethernet Adapter"
		.string "Belkin F5D5050 USB Ethernet"
		.string "NETGEAR FA101 USB Ethernet Adapter"
		.string "IO DATA USB Ethernet Adapter ET/TX-S"
		.string "3Com USB Ethernet 3C460B"
		.string "SpeedStream USB Ethernet"
		.string "SMC 2206 USB Ethernet"
		.string "SmartNIC USB Ethernet Adapter"
		.string "Microsoft MN-110 USB Ethernet Adapter"
		.string "Linksys USB10T Ethernet Adapter"
		.string "Linksys USB Ethernet Adapter USB100TX"
		.string "Linksys USB10TXX USB Ethernet Adapter"

<br>
DM9601 Devices: (TBC)

		.string "DM9601 USB Ethernet Adapter"
		.string "Hirose DM9601 USB Ethernet Adapter"
		.string "Davicom DM9601 USB Ethernet Adapter"
		.string "Corega DM9601 USB Ethernet Adapter"

<br>
USB Modem devices : (TBC)

		.string "Huawei USB 3G Modem"
		.string "Huawei SFR USB 3G Modem"


----------------
#### Internal commands

My vXworks analysis has been wrong. I found many shellCmd structures that defines commands by categories, like mem, obj, task and so on. However, it appears that **the shell does not rely at all on those commands.** Instead, the vxWorks shell seems to directly rely on symbols available. Consequently we are supposed to be able to call every single function in vxWorks.
The following command list is relevant for a different shell or a different mode (To be checked) <br>
However, each of those commands are calling a function which can be directly call :


##### Basic

 command       | alias | function
---------------|-------|-----------
set history    |       | ?
show history   | h     | h
show lasterror |       | ?
alias          |       | shellCmdAliasShow
unalias        |       | shellCmdAliasDelete
unset config   |       | ?
expr           |       | ?
repeat         |       | ?
echo           |       | ?
set prompt     |       | ?
set config     |       | ?
set env        |       | ?
reboot         |       | reboot
set bootline   | bootChange | ?
show bootline  |       | ?
show devices   | devs  | devs / iosDevShow
show drivers   |       | iosDrvShow
show fds       |       | iosFdShow
string free    | strFree | ?
version        |       | version
sleep          |       | sleep
exit           | quit  | exit
logout         |       | logout
set deploy     |       | ?
print errno    | printErrno, errno | ?
func call      |       | ?
vi             | vi    | ?
emacs          | emacs | ?

##### Mem

 command       | alias   | function
---------------|---------|------
mem dump       | d       | d /  memoryDump
mem modify     | m       | m
mem info       | memShow | 0x4F2670 / memShow

##### Interpreter, Object, Module, Various

 command       | alias  | function
---------------|--------|------
C              |       | ?
object info    | obj    | ?
object handle  | handle | ?
module unload  | unld  | ?
syslog         |       | ipcom_cmd_syslog
sysvar         |       | ipcom_cmd_sysvar
help           |       | help

##### File System

 command       | alias | function
---------------|-------|---------
file create -d | mkdir 
file copy      | cp
file move      | mv
file remove    | rm
file concat    | cat   | ipcom_cmd_cat
file list      | ls
pwd            | pwd

##### Tasks

 command       | alias | function
---------------|-------|------
task           | i
task info      | ti
task suspend   | ts
task delete    | td
task default   |
task regs      |
task hooks     |
task stop      |
task resume    | tr
task wait      |      
task wait -a   | w
task wait -d   | tw
task stack     | checkStack
task spawn     | tsp

##### Symbols

 command       | alias
---------------|-------
set symbol     | set
demangle       |
lookup         | lkup
lookup -a      | lkAddr
printf         | ?

##### Net

 command       | alias | function
---------------|-------|------
 ifconfig      |       | ifconfig
 ping          |       | ping
 traceroute    |       | ipcom_cmd_tracert
 netstat       |       | ipnet_cmd_netstat
 wifi          |       | ipwlan_cmd_wlan
 ipf           |       | ipfirewall_cmd_ipfirewall
 pppconfig     |       | ipppp_cmd_pppconfig
 route         |       | ipnet_cmd_route
 radiusc       |       | ipradius_cmd_radiusc

