#!/usr/bin/python2.7

from parse_all_symbols import *
from idautils import *
from idaapi import *
from idc import *

symb_file = "../logs/symbols.dump"

def main():

	count = 0

	symbols = read_symbols_from_dump(symb_file)
	symbols = filter_addr(symbols, "0x200000", "0x800000")
	symbols_summary(symbols)

	for addr in sorted(symbols["data"].iterkeys()):
		print ("%s -> %s" %(addr, symbols["data"][addr]))
	 	idc.MakeName(int(addr, 16), symbols["data"][addr])
		count+=1

	print ("%d vars name updated..."%count)

main()