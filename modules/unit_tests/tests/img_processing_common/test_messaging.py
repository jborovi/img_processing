from img_processing_common.messaging import read_messages_failover


def test_read_msg_failover_no_host():
    res = read_messages_failover("NoHOst", 6379, "queue")
    assert res is None
