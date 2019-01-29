#!/usr/bin/python2.7

from parse_all_symbols import *
from idautils import *
from idaapi import *
from idc import *

symb_file = "../logs/symbols.dump"

def main():

	count = 0

	symbols = read_symbols_from_dump(symb_file)
	symbols_summary(symbols)

	for segea in Segments():
	    for funcea in Functions(segea, SegEnd(segea)):
	        functionName = GetFunctionName(funcea)
	        if not (functionName.startswith('sub_') or
	        	    functionName.startswith('nullsub')):
	        	continue
	        for (startea, endea) in Chunks(funcea):
	        	fname = symbols["text"].get("0x%08x"%(startea))
	        	if (fname != None):
	           		print (functionName + ":" + "0x%08x -> %s") %(startea, fname)
	           		idc.MakeName(startea, fname)
	           		count+=1
	            # for head in Heads(startea, endea):
	            #     print functionName, ":", "0x%08x"%(head), ":", GetDisasm(head)

	print ("%d function name updated..."%count)

main()