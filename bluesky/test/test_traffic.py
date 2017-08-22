from bluesky.traf import Traffic


def test_create_random_planes():
    count = 3
    traffic = Traffic()
    traffic.mcreate(count)

    assert len(traffic.id) == count
