
def serverClassFactory(serverIface):
    from .GwSetRolePlugin import GwSetRolePlugin
    return GwSetRolePlugin(serverIface)
