FULL_TEST: bool = False

TEST_MASS_DATA_PULL: bool = FULL_TEST or False
TEST_PERIPHERAL_URLS: bool = FULL_TEST or True


_tries = 2
_fail_delay = 5
_success_delay = 0.5
