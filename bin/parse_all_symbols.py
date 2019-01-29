#!/usr/bin/python2.7

symb_file = "../logs/symbols.dump"
kernel_only = False

def format_tuples(list):
	global kernel_only

	segments = {}
	for item in list:

		# Looking for address location
		addr_pos = 0
		while (addr_pos < len(item) and not item[addr_pos].startswith("0x")):
			addr_pos += 1

		if (addr_pos >= len(item)):
			# pos not found
			continue

		# addr found, building function name, addr, segment, module
		address = item[addr_pos]
		segment = item[addr_pos+1]
		fname   = ' '.join(item[:addr_pos])
		module  = ' '.join(item[addr_pos+2:len(item)])

		# adding item to appropriate segment
		if segments.get(segment) == None:
			# creating new segment
			segments[segment] = {}

		# filtering module out of kernel
		if kernel_only and module != "":
			continue

		# adding item to appropriate segment
		if module != "":
			segments[segment][address] = module + " " + fname
		else:
			segments[segment][address] = fname

		# print (segment + " - " + address + " " + fname + " [" + module + "]")

	return segments

def filter_lines(line):
	return ((line != "Type <CR> to continue, Q<CR> to stop:") and
			(line != ""))

def read_symbols_from_dump(file):
	with open(file) as f:
		content = f.readlines()

	print ("%d entries read..." % len (content))

	# you may also want to remove whitespace characters like `\n` at the end of each line
	content = [x.strip() for x in content]
	content = [x.split() for x in content if filter_lines(x)]

	print ("%d filtered entries..." % len (content))

	symbol_table = format_tuples(content)

	return (symbol_table)

def filter_addr(symbols, min, max):

	addr_min = int(min, 16)
	addr_max = int(max, 16)

	print ("Filtering addresses out of [0x%.8X , 0x%.8X]"%(addr_min, addr_max))

	for segment in symbols:
		symbols[segment] = {k:v for k, v in symbols[segment].iteritems() if addr_min < int(k, 16) and int(k, 16) < addr_max}

	return symbols

def dump_segment(symbols, segment):
	print ""
	print "Dumping section ." + segment

	for item in symbols[segment]:
		print ("%s %s" %(item, symbols[segment][item]))

def dump_sorted_segment(symbols, segment):
	print ""
	print "Dumping section ." + segment

	for addr in sorted(symbols[segment].iterkeys()):
		print ("%s %s" %(addr, symbols[segment][addr]))

def symbols_summary(symbols):
	count = 0
	print ("%d segments :" %len(symbols))
	for segment in symbols:
		count += len(symbols[segment])
		print ("- %4s : %5d entries..." %(segment, len(symbols[segment])))
	print ("Total %d entries" %count)

def main():

	symbols = read_symbols_from_dump(symb_file)
	symbols_summary(symbols)

	symbols = filter_addr(symbols, "0x200000", "0x201000")
	symbols_summary(symbols)

	# dump_segment(symbols, "text")
	# dump_sorted_segment(symbols, "bss")

main()
