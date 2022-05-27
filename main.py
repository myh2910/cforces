"""
CForces
=======

A custom terminal simulator with python.

"""
import os
import platform
import shutil
import subprocess
import time

from pathlib import Path

__author__ = 'Yohan Min'
__version__ = '1.1.0'

CONFIG = {
	'auto': True,
	'encodings': ('utf-8', 'euc-kr', 'windows-1250', 'windows-1252'),
	'line_limit': 500,
	'char_limit': 80,
	'mode': 'codeforces',
	'usaco_id': 'minleey1',
	'cpp_compiler': 'g++' 
}

HELP = {
	'cat': {
		'usage': "cat <file>",
		'description': "Output file contents."
	},
	'cd': {
		'usage': "cd [directory]",
		'description': "Change the working directory."
	},
	'exec': {
		'usage': "exec <command>",
		'description': "Execute command on terminal."
	},
	'gcc': {
		'usage': "gcc [directory]",
		'description': "Compile the C++ file from the given project directory."
	},
	'help': {
		'usage': "help [option]",
		'description': "Print help message."
	},
	'ls': {
		'usage': "ls [file]",
		'description': "List directory contents."
	},
	'code': {
		'usage': "code <directory>",
		'description': "Create a programming project according to the current mode."
	},
	'mode': {
		'usage': "mode <mode>",
		'description': "Select compiling mode of the script. Default is 'codeforces'. Allowed values are 'codeforces' and 'usaco'."
	},
	'open': {
		'usage': "open <file>",
		'description': "Open files with the default viewer."
	},
	'rm': {
		'usage': "rm <file>",
		'description': "Remove files or directories."
	},
	'run': {
		'usage': "run [directory]",
		'description': "Execute the compiled file from the given project directory."
	}
}

TEMPLATE = {
	'codeforces': """#include <bits/stdc++.h>
using namespace std;

int main() {
#ifdef _DEBUG
	freopen("input.txt", "r", stdin);
	freopen("output.txt", "w", stdout);
#endif
	ios_base::sync_with_stdio(false); cin.tie(NULL);
\t
	return 0;
}
""",
	'usaco': """/*
ID: %s
TASK: %s
LANG: C++
*/
#include <bits/stdc++.h>
using namespace std;

int main() {
	freopen("%s.in", "r", stdin);
	freopen("%s.out", "w", stdout);
	ios_base::sync_with_stdio(false); cin.tie(NULL);
\t
	return 0;
}
"""
}

class signal:
	DONE = 0
	ERROR = 1
	WARNING = 2
	EXIT = 3

def show_help(option=None, err_msg=None):
	if not option:
		if err_msg:
			print("\033[31m× %s" % err_msg)
			print("╰─>\033[0m Usage: <option> [argument]\n\n    Options:")
			for msg in HELP.values():
				print("""      %s\n        %s""" % (msg['usage'], msg['description']))
		else:
			print("CForces %s" % __version__, end='\n\n')
			print("Usage: <option> [argument]\n\nOptions:")
			for msg in HELP.values():
				print("""  %s\n    %s""" % (msg['usage'], msg['description']))

	elif option not in HELP.keys():
		print("\033[31m× Unknown option: %s" % option)
		print("╰─>\033[0m Options:")
		for msg in HELP.values():
			print("""      %s\n        %s""" % (msg['usage'], msg['description']))

	elif err_msg:
		print("\033[31m× %s" % err_msg)
		print("╰─>\033[0m Usage: %s" % HELP[option]['usage'])
		print("      %s" % HELP[option]['description'])

	else: 
		print("Usage: %s" % HELP[option]['usage'])
		print("  %s" % HELP[option]['description'])

def output_line(i, limit, line):
	# TODO: Print single line on multiple lines of length CONFIG['char_limit']
	line = line.replace('\t', '\033[36m| \033[0m')
	print("\033[34m│ %s │ \033[0m%s" % (str(i + 1).rjust(limit), line))

def view_content(path):
	if not path:
		show_help('cat', "Enter the file path to view")
		return signal.WARNING

	if not os.path.exists(path):
		show_help('cat', "File path '%s' doesn't exist" % path)
		return signal.WARNING

	if os.path.isdir(path):
		print("File path '%s' is not a file" % path)
		return signal.WARNING

	for e in CONFIG['encodings']:
		try:
			with open(path, 'r', encoding=e) as f:
				content = f.read().splitlines()
				total = sum(1 for _ in content)
				limit = len(str(total))
				print("\033[34m◉  %s \033[33m[%s]\033[0m" % (os.path.abspath(path), e))

				for i, line in enumerate(content):
					if i >= CONFIG['line_limit']:
						k = limit + 3
						print('\033[34m%s⋮%s\033[0m' % (' ' * ((k + 1) // 2), ' ' * (k // 2)))
						output_line(total, limit, content[-1])
						break
					output_line(i, limit, line)
			return signal.DONE

		except:
			continue

	print("Failed to output file '%s'" % path)
	return signal.ERROR

def select_mode(mode):
	if not mode:
		show_help('mode', "Enter the name of the mode")
		return signal.WARNING

	if mode in ('codeforces', 'usaco'):
		CONFIG['mode'] = mode
		print("Mode %s selected" % mode)
		return signal.DONE

	show_help('mode', "Unknown mode: %s" % mode)
	return signal.WARNING

def change_dir(path):
	if not path:
		return change_dir(Path.home())

	if not os.path.exists(path):
		show_help('cd', "Directory '%s' doesn't exist" % path)
		return signal.WARNING

	if os.path.isfile(path):
		print("File path '%s' is not a directory" % path)
		return signal.WARNING

	os.chdir(path)
	return signal.DONE

def scan_files(path):
	print("\033[34m◉  %s\033[0m" % os.path.abspath(path))

	total = sum(1 for _ in os.scandir(path))
	if total:
		print("\033[34m│")

	cnt = 0
	for file in os.scandir(path):
		cnt += 1
		if file.is_dir():
			color = '\033[96m'
			filename = file.name + ('\\' if platform.system() == 'Windows' else '/')
		else:
			color = '\033[35m'
			filename = file.name
		print("\033[34m%s─ %s%s\033[0m"
			% ('╰' if cnt == total else '├', color, filename))

def list_files(path):
	if not path:
		return list_files(".")

	if not os.path.exists(path):
		show_help('ls', "File path '%s' doesn't exist" % path)
		return signal.WARNING

	if os.path.isfile(path):
		show_help('ls', "File '%s' is not a directory" % path)
		return signal.WARNING

	if not os.listdir(path):
		show_help('ls', "Directory '%s' is empty" % path)
		return signal.WARNING

	scan_files(path)
	return signal.DONE

def open_file(path):
	if not path:
		show_help('open', "Enter the file path to open")
		return signal.WARNING

	if os.path.isfile(path):
		print("Opening file '%s'..." % path)
	elif os.path.isdir(path):
		print("Opening directory '%s'..." % path)
	else:
		print("Opening new file '%s'..." % path)

	if platform.system() == 'Windows':
		os.system('code "%s"' % path)
	else:
		os.system('xfce4-terminal -x vim "%s"' % path)
	return signal.DONE

def coding_project(path):
	if not path:
		show_help('code', "Enter the project directory to open")
		return signal.WARNING

	project = os.path.split(path)[1]
	cpp_file = os.path.join(path, "%s.cpp" % project)
	if CONFIG['mode'] == 'codeforces':
		input_file = os.path.join(path, "input.txt")
		output_file = os.path.join(path, "output.txt")
	elif CONFIG['mode'] == 'usaco':
		input_file = os.path.join(path, "%s.in" % project)
		output_file = os.path.join(path, "%s.out" % project)

	if os.path.exists(path):
		print("Opening project '%s'..." % path)
	else:
		print("Creating new project '%s'..." % path)
		os.mkdir(path)

		with open(cpp_file, 'w', newline='\n') as f:
			if CONFIG['mode'] == 'codeforces':
				f.write(TEMPLATE['codeforces'])
			elif CONFIG['mode'] == 'usaco':
				f.write(TEMPLATE['usaco'] % (CONFIG['usaco_id'], project, project, project))

		for file in (input_file, output_file):
			with open(file, 'w', newline='\n') as f:
				f.write("")

	if platform.system() == 'Windows':
		os.system('code "%s" "%s" "%s"' % (cpp_file, input_file, output_file))
	elif platform.system() == 'Linux':
		os.system('vim "%s" "%s" "%s"' % (cpp_file, input_file, output_file))
	
	os.chdir(path)
	return signal.DONE

def compile_project(path):
	if not path:
		path = "."
	os.chdir(path)

	if CONFIG['mode'] == 'codeforces':
		os.system('%s -D _DEBUG *.cpp' % CONFIG['cpp_compiler'])
	elif CONFIG['mode'] == 'usaco':
		os.system('%s *.cpp' % CONFIG['cpp_compiler'])

def run_project(path):
	if not path:
		path = "."
	os.chdir(path)

	if platform.system() == 'Windows':
		path = os.path.join(path, "a.exe")
	elif platform.system() == 'Linux':
		path = os.path.join(path, "a.out")

	try:
		if not os.path.exists(path):
			if CONFIG['mode'] == 'codeforces':
				os.system('%s -D _DEBUG *.cpp' % CONFIG['cpp_compiler'])
			elif CONFIG['mode'] == 'usaco':
				os.system('%s *.cpp' % CONFIG['cpp_compiler'])
		subprocess.Popen('"%s"' % path)

	except Exception as e:
		print("\n\033[1m\033[31mError:\033[0m %s" % e)
		return signal.ERROR

	return signal.DONE

def remove_file(path):
	if not path:
		show_help('rm', "Enter the file path to remove")
		return signal.WARNING

	if not os.path.exists(path):
		show_help('rm', "File path '%s' doesn't exist" % path)
		return signal.WARNING

	if os.path.isfile(path):
		os.remove(path)
		print("File '%s' deleted successfully" % path)
		return signal.DONE

	if not os.listdir(path):
		os.rmdir(path)
		print("Directory '%s' deleted successfully" % path)
		return signal.DONE

	try:
		proceed = input("Directory '%s' is not empty; confirm to continue [y/N] \033[97m" % path).strip()
		print('\033[0m', end='')
		if proceed in ('y', 'Y'):
			shutil.rmtree(path)
			print("Directory '%s' deleted successfully" % path)
			return signal.DONE
		print("Operation has been cancelled")
		return signal.WARNING
	except Exception as e:
		print("\n\033[1m\033[31mError:\033[0m %s" % e)
		return signal.ERROR

def execute_cmd(command):
	if not command:
		show_help('exec', "Enter the command to execute")
		return signal.WARNING

	try:
		p = subprocess.Popen(command)
	except Exception as e:
		print("\n\033[1m\033[31mError:\033[0m %s" % e)
		return signal.ERROR

	try:
		while p.poll() is None:
			time.sleep(0.1)
	except KeyboardInterrupt:
		p.kill()
		print("\n\033[0mProcess terminated by KeyboardInterrupt")
		return signal.ERROR
	except Exception as e:
		p.kill()
		print("\n\033[1m\033[31mError:\033[0m %s" % e)
		return signal.ERROR

	return signal.DONE

def translate_cmd(command):
	if not command:
		show_help(err_msg="Enter the command")
		return signal.WARNING
	if command in ('exit', 'quit', 'q'):
		return signal.EXIT
	if command in ('clear', 'cls'):
		os.system('cls' if platform.system() == 'Windows' else 'clear')
		return signal.DONE

	command += ' '
	if command.startswith('cat '):
		return view_content(command[3:].strip())
	if command.startswith('cd '):
		return change_dir(command[2:].strip())
	if command.startswith('code '):
		return coding_project(command[4:].strip())
	if command.startswith('exec '):
		return execute_cmd(command[4:].strip())
	if command.startswith('gcc '):
		return compile_project(command[3:].strip())
	if command.startswith('help '):
		return show_help(command[4:].strip())
	if command.startswith('ls '):
		return list_files(command[2:].strip())
	if command.startswith('mode '):
		return select_mode(command[4:].strip())
	if command.startswith('open '):
		return open_file(command[4:].strip())
	if command.startswith('rm '):
		return remove_file(command[2:].strip())
	if command.startswith('run '):
		return run_project(command[3:].strip())

	show_help(err_msg="Unknown command: %s" % command.strip())
	return signal.WARNING

def start_cforces():
	title = " CForces %s " % __version__
	k = 46 - len(title)
	print(
		"""\033[36m┌%s\033[97m%s\033[36m%s┐
│%s      ____________                            %s│
│%s     / ____/ ____/___  _____________  _____   %s│
│%s    / /   / /_  / __ \/ ___/ ___/ _ \/ ___/   %s│
│%s   / /___/ __/ / /_/ / /  / /__/  __(__  )    %s│
│%s   \____/_/    \____/_/   \___/\___/____/     %s│
│%s                                              %s│
└──────────────────────────────────────────────┘\033[0m"""
		% ('─' * ((k + 1) // 2), title, '─' * (k // 2), *('\033[93m', '\033[36m') * 6))

	if platform.system() == 'Linux':
		import readline

	while True:
		command = input("\033[92m%s \033[1m>>\033[0m\033[97m " % os.getcwd()).strip()
		print('\033[0m', end='')
		output = translate_cmd(command)
		if output == 3:
			print("Exiting CForces...")
			break

if __name__ == '__main__':
	try:
		start_cforces()
	except KeyboardInterrupt:
		print("\n\033[0mTerminating CForces...")
