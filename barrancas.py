#!/usr/bin/python

from barrancas.server import Server
from barrancas.generator import Generator
from path import path
import argparse
import yaml
import sys

CONFIG = {
	'port': 8000,		
}

def main():    

	try:
		properties_f = path('conf.yml').text()
		properties = yaml.load(properties_f)
		CONFIG.update(properties)
	except:
		pass
   
	parser = argparse.ArgumentParser()
	parser.add_argument('--server', metavar='PORT', nargs='?', default=None, type=int, required=False)
	parser.add_argument('--generate', action='store_true')
	args = parser.parse_args()
	if len(sys.argv) > 1:
		if args.server or args.server is None:
			port = CONFIG['port']
			if not args.server is None:
				port = args.server
			s = Server(port)
			s.start()
		if args.generate:
			g = Generator(CONFIG)
			g.generate()
	else:
	        g = Generator(CONFIG)
        	g.generate()


if __name__ == '__main__':
	main()
