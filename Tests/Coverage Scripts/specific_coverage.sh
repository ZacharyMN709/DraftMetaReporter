cd ../..

# TODO: Parameterize the datafile name.
# --data-file='Tests/Coverage Scripts/.coverage'

# coverage run -a -m unittest 'Tests/TestDataFetching.py'
# coverage run -a -m unittest 'Tests/TestGameMetadata.py'
# coverage run -a -m unittest 'Tests/TestGameMetadataCard.py'
# coverage run -a -m unittest 'Tests/TestGameMetadataDeck.py'
# coverage run -a -m unittest 'Tests/TestGameMetadataDraft.py'
# coverage run -a -m unittest 'Tests/TestRequesting.py'
# coverage run -a -m unittest 'Tests/TestUtilities.py'
# coverage run -a -m unittest 'Tests/TestWUBRG.py'
coverage html
exit