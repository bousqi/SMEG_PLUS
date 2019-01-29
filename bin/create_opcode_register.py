
start = ScreenEA()
ea = ScreenEA()
while ea < start+24:
	MakeUnknown(ea, 12, DOUNK_SIMPLE)
	MakeStruct(ea, "opcode")
	ea+=12

00000000 opcode          struc # (sizeof=0xC, mappedto_1) # XREF: ROM:opcode_list/r
00000000                                         # ROM:007A2C04/r ...
00000000 name:           .long ?                 # offset (00000000)
00000004 bytecode:       .long ?                 # base 16
00000008 unk:            .long ?                 # base 16
0000000C opcode          ends
0000000C
00000000 # ---------------------------------------------------------------------------
00000000
00000000 register        struc # (sizeof=0x8, mappedto_2) # XREF: ROM:stru_7A3540/r
00000000                                         # ROM:007A3548/r ...
00000000 unk:            .long ?                 # base 16
00000004 name:           .long ?                 # offset (00000000)
00000008 register        ends
00000008

limit = 0x007A3540
ea = ScreenEA()
MakeName(ea, "opcodes")
while ea < limit:
	MakeUnknown(ea, 12, DOUNK_SIMPLE)
	MakeStruct(ea, "opcode")
	ea+=12


limit = 0x007A36A8
ea = ScreenEA()
MakeName(ea, "peripherals")
while ea < limit:
	MakeUnknown(ea, 8, DOUNK_SIMPLE)
	MakeStruct(ea, "peripheral")
	ea+=8


limit = 0x007A2784
ea = ScreenEA()
while ea < limit:
	MakeUnknown(ea, 8, DOUNK_SIMPLE)
	MakeStruct(ea, "register")
	ea+=8




ea = 0x00744F74
limit = 0x100
MakeUnknown(ea, limit-ea, DOUNK_SIMPLE)
while ea < limit:
	MakeStr(ea, BADADDR)
	ea+=1
