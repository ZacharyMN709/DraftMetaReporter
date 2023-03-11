# Move to the root of the project, to simplify path logic.
cd ../..

# Get the module and file name from the arguments provided.
module_name=$1
file_name=$2

# Set the variables for which coverage file to output to,
#  and which module to display code for.
coverage_file='Tests/Coverage/.single'
target_module="core/${module_name}/*"

# Choose the file or module to test based on if a filename exists.
if [ -n "${file_name}" ]; then
  to_test="Tests/${module_name}_Test/${file_name}_Test.py"
  test_log="Tests/${module_name}_Test/${file_name}_Test.py"
else
  to_test="Tests/${module_name}_Test/__init__.py"
  test_log="Tests/${module_name}_Test/*"
fi

# Run the coverage program, only if a module was defined.
if [ -n "${module_name}" ]; then
  coverage run --data-file="${coverage_file}" -m unittest "${to_test}"
  # TODO: Try and isolate only the file, and not the whole module, when file is provided.
  coverage html --data-file="${coverage_file}" --include="${target_module}","${test_log}"
fi

exit
