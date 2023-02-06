cd ../..

# TODO: Parameterize the datafile name.
# --data-file='Tests/Coverage Scripts/single.coverage'

# coverage run --data-file='Tests/Coverage Scripts/single.coverage' -m unittest 'Tests/TestUtilities.py'
coverage run --data-file='Tests/Coverage Scripts/single.coverage' -m unittest 'Tests/TestWUBRG.py'
# coverage run --data-file='Tests/Coverage Scripts/single.coverage' -m unittest 'Tests/TestRequesting.py'
# coverage run --data-file='Tests/Coverage Scripts/single.coverage' -m unittest 'Tests/TestDataFetching.py'
# coverage run --data-file='Tests/Coverage Scripts/single.coverage' -m unittest 'Tests/TestGameMetadata.py'
# coverage run --data-file='Tests/Coverage Scripts/single.coverage' -m unittest 'Tests/TestGameMetadataCard.py'
# coverage run --data-file='Tests/Coverage Scripts/single.coverage' -m unittest 'Tests/TestGameMetadataDeck.py'
# coverage run --data-file='Tests/Coverage Scripts/single.coverage' -m unittest 'Tests/TestGameMetadataDraft.py'
coverage html --data-file='Tests/Coverage Scripts/single.coverage'
exit