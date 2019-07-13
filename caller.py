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
					callid = genid(args.prefix) if args.prefix else genid('')
	
				if args.folder:
					files = os.listdir(args.folder)
					sound = args.folder + random.choice(files).split('.')[0]
				elif args.file:
					sound = args.file.split('.')[0]
				else:
					sound = 'hello-world'

				call(target, callid, sound)

				numcalls += 1

				print('[*] Call Sent to {}'.format(target))

				time.sleep(args.frequency)
			
			elif numcalls == args.numcalls:

				print('[-] Desired number of calls reached, quitting...')

		except (KeyboardInterrupt, SystemExit):

			print('\n[-] KeyboardInterrupt caught, quitting...')




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


genid = lambda pre : str(pre) + str(random.randint(1000000000, 9999999999))


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
		help = 'country code for random callerids',
		type = str,
		const = 1
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
		required = False, 
		type = int,
		const = 60
	)

	parser.add_argument(
		'--numcalls', 
		help = 'total number of calls to send', 
		required = False, 
		type = int,
		const = math.inf
	)

	args = parser.parse_args()

	return args



if __name__ == '__main__':
	main()