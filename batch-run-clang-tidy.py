import subprocess
import os
import sys

def run_clang_tidy(build_dir, source_dir, clang_tidy=None, clang_apply=None, check='modernize-use-nullptr', fix_errors=False, working_dir=None, logfile=None):
	# directory containing run-clang-tidy.py script
	current_dir = os.path.dirname(os.path.realpath(__file__))
	script = os.path.join(current_dir, 'run-clang-tidy.py')

	# directory where checks are performed/applied 
	if working_dir is None:
		working_dir = source_dir
	
	args = ['python', script, '-p', build_dir, '-header-filter=%s*' % (source_dir)]
	if clang_tidy:
		args.extend(['-clang-tidy-binary', clang_tidy])
	if clang_apply:
		args.extend(['-clang-apply-replacements-binary', clang_apply])
	args.extend(['-quiet'])
	args.extend(["-checks=-*,%s" % (check)])
	args.extend([working_dir])
	if fix_errors:
		args.extend(['-fix-errors'])
	else:
		args.extend(['-fix'])

	if logfile:
		logfile.write(" ".join(args) + '\n')
	prog = subprocess.Popen(args, stdout=logfile, stderr=logfile, cwd=working_dir)
	prog.communicate()
	return True # if prog.returncode == 0 else False -> cannot trust run-clang-tidy.py return code


def build_patch(build_dir, logfile=None, target=None):
	args = ['cmake', '--build', build_dir]
	if target:
		args.append(target)
	if logfile:
		logfile.write(" ".join(args) + '\n')
	prog = subprocess.Popen(args, stdout=logfile, stderr=logfile, cwd=build_dir)
	prog.communicate()
	return True if prog.returncode == 0 else False


def commit_patch(message, source_dir, logfile=None):
	args = ['git', 'commit', '-am', '%s' % (message)]
	if logfile:
		logfile.write(" ".join(args) + '\n')
	prog = subprocess.Popen(args, stdout=logfile, stderr=logfile, cwd=source_dir)
	prog.communicate()
	return True if prog.returncode == 0 else False


def revert_patch(source_dir, logfile=None):
	args = ['git', 'reset', '--hard', 'HEAD']
	if logfile:
		logfile.write(" ".join(args) + '\n')
	prog = subprocess.Popen(args, stdout=logfile, stderr=logfile, cwd=source_dir)
	prog.communicate()
	return True if prog.returncode == 0 else False


def batch_run_clang_tidy(build_dir, source_dir, checks, clang_tidy=None, clang_apply=None, target=None, working_dir=None, log_dir=None, no_commit=False, fix_errors=False, stop_if_compile_error=False):

	if log_dir is None:
		log_dir = build_dir
	
	with open(os.path.join(log_dir, '_check_initial_build.log'), 'w') as logfile:
		if not build_patch(build_dir, logfile=logfile):
			print("FAILED: ninja [initial build]")

	for check in checks:
		with open(os.path.join(log_dir, '_check__%s.log' % check), 'w') as logfile:
			print("Checking for '%s'" % check)
			if run_clang_tidy(build_dir=build_dir, source_dir=source_dir, clang_tidy=clang_tidy, clang_apply=clang_apply, working_dir=working_dir, check=check, fix_errors=fix_errors, logfile=logfile):
				print("  Applied fixes for '%s'" % check)
				if build_patch(build_dir=build_dir, target=target, logfile=logfile):
					print("  Built fixes for '%s'" % check)
					if no_commit:
						pass
					elif commit_patch(message=check, source_dir=source_dir, logfile=logfile):
						print("  Commited fixes for '%s'" % check)
					else:
						print("->FAILED: git commit -am '%s'" % check)
				elif stop_if_compile_error:
					print("->FAILED: ninja ['%s'] -> Stopping" % check)
					return
				else:
					revert_patch(source_dir=source_dir, logfile=logfile)
					print("->FAILED: ninja ['%s']" % check)
			else:
				print("->FAILED: clang-tidy/apply '%s'" % check)


if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser('')
	parser.add_argument('-b', '-build', dest='build',
		help='path to build dir containing compile_commands.json')
	parser.add_argument('-s', '-source', dest='source',
		help='path to source directory')
	parser.add_argument('-log_dir', dest='log_dir',
		default=None,
		help='path log files')
	parser.add_argument('-c', '-checks', dest='checks', action='append',
		help='checks to be performed')
	parser.add_argument('-clang-tidy', dest='clang_tidy',
		default=None,
		help='path to clang-tidy binary')
	parser.add_argument('-clang-apply', dest='clang_apply',
		default=None,
		help='path to clang-apply-replacements binary')
	parser.add_argument('-fix-errors', dest='fix_errors', action='store_true', 
		help='apply fix-its even if there are errors')
	parser.add_argument('-no', '-no-commit', dest='no_commit', action='store_true', 
		help='skip commit')
	parser.add_argument('-stop-on-error', dest='stop_if_compile_error', action='store_true', 
		help='cancel if there is an error')
	args = parser.parse_args()


	checks = [
		'modernize-use-override',
		'modernize-use-bool-literals',
		'modernize-use-using',
		'modernize-deprecated-headers',
		'modernize-use-nullptr',
		'modernize-redundant-void-arg',
		'readability-implicit-bool-conversion',
		'google-explicit-constructor',
		'performance-trivially-destructible'
		]
	if args.checks is not None:
		checks = args.checks

	batch_run_clang_tidy(build_dir=args.build, source_dir=args.source, clang_tidy=args.clang_tidy, clang_apply=args.clang_apply, checks=checks, log_dir=args.log_dir, no_commit=args.no_commit, fix_errors=args.fix_errors, stop_if_compile_error=args.stop_if_compile_error)
