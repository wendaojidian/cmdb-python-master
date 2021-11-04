from utils.nats import pynats


def NATS_subscribe():
    c = pynats.Connection(verbose=True)
    c.connect()

    # Simple Subscriber
    def callback(msg):
        print(msg.data)
    c.subscribe('holy', callback)

    c.wait()
    # Close connection
    c.close()


# NATS_subscribe()
