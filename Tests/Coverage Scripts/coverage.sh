cd ../..
coverage run --data-file='Tests/Coverage Scripts/.coverage' -m unittest discover
coverage html --data-file='Tests/Coverage Scripts/.coverage'
exit