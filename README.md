
# Modernizing legacy C++ code

## Overview
`clang-tidy` offers a wide range of checks to lint C++ code. In some cases it can generate automatic fixes, e.g. to replace expressions with `typedef` to `using`.
`run-clang-tidy.py` is a tool which runs `clang-tidy` with a set of checks for an entire source code directory. To do this it needs to know how the source is compiled.
CMake can generate this information for `ninja` and `Makefile` generators by specifying the option `CMAKE_EXPORT_COMPILE_COMMANDS:BOOL=ON`.


## Tools
### clang-tidy provides a range of checks with fixits.
For a list of these checks see https://clang.llvm.org/extra/clang-tidy/. Some warn about bugprone code, improve readability or allow to enforce coding styles. The `modernize-*` checks mostly help to transform pre-c++11 code to c++11 (or c++14) code.
On Ubuntu you can install it via:
- `apt-get update`
- `apt install clang-tools-10`
- `apt install clang-tidy-10`

### The run-clang-tidy.py script
This script is available at [llvm](https://clang.llvm.org/extra/doxygen/run-clang-tidy_8py_source.html). Run it with `-h` to get help.
*Note: I patched the script*, because it did not merge patches correctly (because warnings did not have normalized paths). Due to this bug it would sometimes add keywords multiple times, e.g. `std::string Name() override override`.


### The batch-run-clang-tidy.py script
This script runs `run-clang-tidy.py` for a range of checks. After each check it tries to compile the code. If compilation succeeds, it commits tha patch using `git commit -am "<check_name>"`.
The script includes code compiled withing a folder (recursively), so if you want to focus on refactoring e.g. subfolder XYZ then you could run:

`python ./Modernize/batch-run-clang-tidy.py -b /work/build/debug -s /work/src/YourProject/XYZ -c modernize-use-using -c modernize-use-override`

In the call above, the folder `/work/build/debug` is where the build folder in this example. Also note that multiple checks can be queued. If you want the script to cancel if something fails, then add `-stop-on-error`.


## Other scripts to replace legacy code
Since large parts of our code is only built with msvc14 (VS 20215), and we use precompiled headers, clang-tidy was not always successful at providing fixits. Therefore, I created collection of python scripts to modernize our code, and e.g. reduce depedencies on boost where c++11 provides an alternative. The basic logic is implemented in [replace_expression.py](replace_scripts/replace_expression.py)

- replace_boost_foreach.py
  - replaces BOOST_FOREACH if on a single line
  - removes header
- replace_lexical_cast.py:
  - replaces `boost::lexical_cast<std::string>` by `std::to_string`
  - removes unused header
  - skips files with `BOOST_REVERSE_FOREACH`
- replace_typedef_with_using.py
  - transforms `typedef x::y::z<T> xyz_t` to `using xyz_t = x::y::z<T>`
  - skips multiline typedefs and function pointer-like typedefs
- replace_incorrect_include_capitalization.py
  - tries to fix incorrect spelling of headers (relative paths only)
- replace_assign_list_of.py
  - replaces `boost::assign::list_of(X)(Y)` by `{ X, Y }`
- replace_null.py
  - finds typical context where `NULL` is used and replaces it by `nullptr`
- etc.