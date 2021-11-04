from utils.nats import pynats


def NATS_publish(msg):
    c = pynats.Connection(verbose=True)
    c.connect()
    # Simple Publisher
    c.publish('holy', msg=msg)
    c.close()
