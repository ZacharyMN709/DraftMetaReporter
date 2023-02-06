cd ../..
file='Tests/Coverage Scripts/.coverage.single'
coverage run --data-file="$file" -m unittest discover
coverage html --data-file="$file"
exit