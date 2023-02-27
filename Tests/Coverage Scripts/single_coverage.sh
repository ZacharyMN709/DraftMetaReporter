cd ../..

file='Tests/Coverage Scripts/.coverage.single'

# coverage run --data-file="$file" -m unittest 'Tests/TestUtilities.py'
# coverage run --data-file="$file" -m unittest 'Tests/TestWUBRG.py'
# coverage run --data-file="$file" -m unittest 'Tests/TestRequesting.py'
# coverage run --data-file="$file" -m unittest 'Tests/TestDataFetching.py'
# coverage run --data-file="$file" -m unittest 'Tests/TestGameMetadata.py'
# coverage run --data-file="$file" -m unittest 'Tests/TestGameMetadataCard.py'
# coverage run --data-file="$file" -m unittest 'Tests/TestGameMetadataDeck.py'
# coverage run --data-file="$file" -m unittest 'Tests/TestGameMetadataDraft.py'

coverage run --data-file="$file" -m unittest 'Tests/TestUtilities.py'
coverage html --data-file="$file"
exit
