from qgis.server import *
from qgis.core import *


class GwSetRoleFilter(QgsAccessControlFilter):

    def __init__(self, server_iface: QgsServerInterface):
        super().__init__(server_iface)
        QgsMessageLog.logMessage(f"SUCCESS - GwSetRoleFilter initialized!", 'plugin', Qgis.Info)

    def layerFilterExpression(self, layer: QgsVectorLayer):
        request = self.serverInterface().requestHandler()
        params = request.parameterMap()
        username = params.get("USER")

        if username:
            dataSource = layer.source()
            uri = QgsDataSourceUri(dataSource)

            if (uri.hasParam("session_role")):
                uri.removeParam("session_role")
            uri.setParam("session_role", username)

            newDS = uri.uri()
            baseName = layer.name()
            providerKey = layer.providerType()

            layer.setDataSource(newDS, baseName, providerKey)

        return super().layerFilterExpression(layer)


class GwSetRolePlugin:
    def __init__(self, serverIface: QgsServerInterface):

        QgsMessageLog.logMessage("SUCCESS - GwSetRolePlugin init", 'plugin', Qgis.Info)

        try:
            serverIface.registerAccessControl(GwSetRoleFilter(serverIface))
        except Exception as e:
            QgsLogger.debug(f"GwSetRoleFilter failed loading: {e}")

