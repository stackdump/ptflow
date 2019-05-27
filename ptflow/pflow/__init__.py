from ptflow.pflow.xml import StateMachine, PFlowNet

def set_provider(storage):
    """ set storage provider class """

    assert storage.SOURCE_HEADER
    assert storage.reconnect
    assert storage.migrate

    StateMachine.storage_provider = storage

def load_file(path):
    try:
        p = StateMachine(PFlowNet(path))
    except Exception as x:
        return p, x

    return p, None
