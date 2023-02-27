cd ../..
file='Tests/Coverage Scripts/.coverage'
coverage run --data-file="$file" -m unittest discover
coverage html --data-file="$file"
exit
