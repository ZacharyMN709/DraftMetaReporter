cd ../..

module_name=$1
coverage_file='Tests/Coverage/.single'
test_module="Tests/${module_name}_Test/__init__.py"


if [ -n "$module_name" ]; then
  coverage run -a --data-file="${coverage_file}" -m unittest "${test_module}"
fi
coverage html --data-file="${coverage_file}"

exit
