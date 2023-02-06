cd ../..

file='Tests/Coverage Scripts/.coverage.cumulative'

# coverage run -a --data-file="$file" -m unittest 'Tests/TestUtilities.py'
# coverage run -a --data-file="$file" -m unittest 'Tests/TestWUBRG.py'
# coverage run -a --data-file="$file" -m unittest 'Tests/TestRequesting.py'
# coverage run -a --data-file="$file" -m unittest 'Tests/TestDataFetching.py'
# coverage run -a --data-file="$file" -m unittest 'Tests/TestGameMetadata.py'
# coverage run -a --data-file="$file" -m unittest 'Tests/TestGameMetadataCard.py'
# coverage run -a --data-file="$file" -m unittest 'Tests/TestGameMetadataDeck.py'
# coverage run -a --data-file="$file" -m unittest 'Tests/TestGameMetadataDraft.py'

# coverage run -a --data-file="$file" -m unittest 'Tests/TestGameMetadataDraft.py'
coverage html
exit