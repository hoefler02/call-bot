#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Title  : Python Call Bot
# @Author : Michael Hoefler
# @Date.  : 2019-07-12 19:37:47

from pycall import Application, CallFile, Call
import argparse
import random
import math
import time
import os


def main():

	args = setup()

	print('[+] Starting Caller Tool...\n')

	numcalls = 0

	while True:

		try:
			if (numcalls < args.numcalls):

				target = args.target

				if not args.callid:
					callid = genid(args.prefix) if args.prefix else genid('1')
				if args.folder:
					files = os.listdir(args.folder)
					sound = args.folder + random.choice(files)
				elif args.file:
					sound = args.file
				else:
					sound = 'hello-world'

				call(target, callid, sound.split('.')[0])

				numcalls += 1

				print('[*] Call Sent to {} using callerid {} and soundfile {}, sleeping for {} seconds...'.format(formatnum(target), formatnum(callid), sound, args.frequency))


				if numcalls == int(args.numcalls):

					print('\n[-] Desired number of calls reached, quitting...\n')

					exit()
				else:
					time.sleep(int(args.frequency))

		except (KeyboardInterrupt):

			print('\n[-] KeyboardInterrupt caught, quitting...')

			exit()




def call(target, callid, sound):

	CallFile(

		Call(
			'SIP/flowroute/{}'.format(target), 
			callerid = callid
		), 

		Application(
			'Playback',
			sound
		), 

		user = 'asterisk' # assuming asterisk is running as its own user (recommended)

	).spool()


def genid(pre):

	components = pre.split('.')

	to_gen = abs(10 - (len(components[1]))) if len(components) == 2 else 10

	components.append('')

	suffix = ''.join([str(i) for i in random.sample(range(0, 10), to_gen)])

	return components[0] + components[1] + suffix

def formatnum(numstr):
	return '{}({})-{}-{}'.format(numstr[:-10], numstr[-10:-7], numstr[-7:-4], numstr[-4:])	


def setup():

	parser = argparse.ArgumentParser('Automatic Caller Script')

	parser.add_argument(
		'target', 
		help = 'target number',
		type = str
	)

	parser.add_argument(
		'--callid', 
		help = 'callerid for spoofing, if not specified a random id is used with each new call',
		type = str,
		required = False, 
	)

	parser.add_argument(
		'--prefix', 
		help = 'callerid prefix, specified as COUNTRYCODE.PREFIX',
		nargs = '?',
		default = '1',
		const = '1'
	)

	parser.add_argument(
		'--file', 
		help = 'path to a sound file to play on pickup', 
		required = False, 
		type = str
	)

	parser.add_argument(
		'--folder', 
		help = 'path to a folder with soundfiles, a random file in the folder will be picked with each new call', 
		required = False, 
		type = str
	)

	parser.add_argument(
		'--frequency', 
		help = 'send a call every X seconds', 
		nargs = '?',
		default = 60,
		const = 60
	)

	parser.add_argument(
		'--numcalls', 
		help = 'total number of calls to send', 
		nargs = '?',
		type = int,
		default = math.inf,
		const = math.inf,
	)

	args = parser.parse_args()

	return args



if __name__ == '__main__':
	main()
