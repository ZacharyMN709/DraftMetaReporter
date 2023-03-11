cd ../..

module_name=$1
coverage_file='Tests/Coverage/.single'
test_module="Tests/${module_name}_Test/__init__.py"
target_module="core/${module_name}/*"

if [ -n "$module_name" ]; then
  coverage run --data-file="${coverage_file}" -m unittest "${test_module}"
  coverage html --data-file="${coverage_file}" --include="${target_module}"
fi

exit
