# Fixed `run-clang-tidy.py` script

The original `run-clang-tidy.py` script is available from llvm, with many copies floating around (e.g. [here](https://clang.llvm.org/extra/doxygen/run-clang-tidy_8py_source.html)).

After using it for a while I patched it, because some fixits are applied multiple times because `clang-tidy` produces warnings at the same file location with seemingly different paths.
The patched script first loads the yaml files and normalizes the file paths before calling `clang-apply-replacements`.

I also added a simple script [batch-run-clang-tidy.py](batch-run-clang-tidy.py) to run a sequence of clang-tidy checks (with fixits), apply them, try to build the entire code, and if sucessful commit the patch. If the build is not successful, the script will either reset the changes or stop (`-stop-on-error` option).

Example use:

`python batch-run-clang-tidy.py -b /path/to/build -s /path/to/src -c modernize-use-using -c modernize-use-override`

Dependencies:
- clang-tidy
- clang-apply-replacements
- project with cmake build system + ninja (or Makefiles), configure with `CMAKE_EXPORT_COMPILE_COMMANDS:BOOL=ON`
