# Move to the root of the project, to simplify path logic.
cd ../..

# Get the module names to run coverage for.
module_names=( "$@" )

# Set the variable for which coverage file to output to.
coverage_file='Tests/Coverage/.cumulative'

# For each module provided, set the correct test file and run coverage.
#  If no modules are provided, this step is inherently skipped.
for module in "${module_names[@]}"
do
  test_module="Tests/${module}_Test/__init__.py"
  coverage run -a --data-file="${coverage_file}" -m unittest "${test_module}"
done

# Output the coverage information to html.
coverage html --data-file="${coverage_file}"

exit

# List of current testable modules.
# "utilities" "wubrg" "data_requesting" "game_metadata"
