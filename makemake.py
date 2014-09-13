#!/usr/bin/env python

import argparse

def LinkerAction(in_flag):
	class LinkerAction(argparse.Action):
		flag = in_flag
		def __call__(self, parser, namespace, value, option_string=None, **kargs):
			args = getattr(namespace, 'linker_flags', [])
			needs_space = len(self.flag) > 2
			args.append(self.flag + ' ' * needs_space + value)
			setattr(namespace, 'linker_flags', args)
	return LinkerAction

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--library', metavar='name', action=LinkerAction('-l'), help='name of a library to link against')
parser.add_argument('-f', '-framework', '--framework', metavar='name', action=LinkerAction('-framework'), help='name of a framework to link against')
parser.add_argument('-a', '--architecture', '--arch', '-arch', metavar='arch', action='store', default=None, dest='architecture', help='name of the architecture to build for')
parser.add_argument('--strict-cflags', action='store_true', help='include a CFLAGS variable that enables some strict checking')
parser.add_argument('targets', metavar='name', nargs='+', help='names of programs to build (requires name.c or name.m to exist)')

args = parser.parse_args()

arch = args.architecture
cflags=[]
ldflags = getattr(args, 'linker_flags', [])
targets = args.targets

import sys
if sys.stdout.isatty():
	import os
	fd = os.open('Makefile', os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0644)
	if fd > -1:
		os.dup2(fd, 1)

printed_any_variables = False
def print_variable(before_eq, after_eq):
	global printed_any_variables
	print '%s=%s' % (before_eq, after_eq)
	printed_any_variables = True

if arch is not None:
	print_variable('ARCH?', arch)
	cflags.insert(0, '-arch')
	cflags.insert(1, arch)
	ldflags.insert(0, '-arch')
	ldflags.insert(1, arch)
if args.strict_cflags:
	cflags.insert(0, '-std=c99')
	cflags.insert(1, '-Wall')

if cflags:
	print_variable('CFLAGS+', ' '.join(cflags))
if ldflags:
	print_variable('LDFLAGS+', ' '.join(ldflags))

if printed_any_variables:
	print

printed_all_target = False
if len(targets) > 1:
	print 'all:', ' '.join(targets)
	printed_all_target = True
	print

for target in targets:
	print '%s: %s.o' % (target, target)
print
print 'clean:'
print '\trm *.o'
print '.PHONY: clean' + ' all' * printed_all_target
