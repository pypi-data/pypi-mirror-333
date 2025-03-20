import sewerrat
import os
import tempfile
import time


def test_list_registered_directories(basic_config):
    url, mydir = basic_config

    regged = sewerrat.list_registered_directories(url)
    assert len(regged) > 0

    found = False
    for x in regged:
        if x["path"] == mydir:
            found = True
            assert x["names"] == [ "metadata.json" ]
    assert found

    # Filter by user.
    filtered = sewerrat.list_registered_directories(url, user=True)
    assert regged == filtered

    filtered = sewerrat.list_registered_directories(url, user=regged[0]["user"] + "_asdasdasd")
    assert len(filtered) == 0

    # Filter by contains.
    filtered = sewerrat.list_registered_directories(url, contains=os.path.join(mydir, "metadata.json"))
    assert regged == filtered

    filtered = sewerrat.list_registered_directories(url, contains=os.path.join(mydir + "-asdasd"))
    assert len(filtered) == 0

    # Filter by prefix.
    filtered = sewerrat.list_registered_directories(url, prefix=os.path.dirname(mydir))
    assert regged == filtered

    filtered  = sewerrat.list_registered_directories(url, prefix=os.path.dirname(mydir) + "-asdasdad")
    assert len(filtered) == 0

    # Multiple filters work.
    filtered  = sewerrat.list_registered_directories(url, prefix=os.path.dirname(mydir), user=True, contains=os.path.join(mydir, "metadata.json"))
    assert regged == filtered
