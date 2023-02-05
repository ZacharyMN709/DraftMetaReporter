coverage run -s . -p 'TestRequesting.py' -m unittest discover
coverage report -m
coverage html
exit