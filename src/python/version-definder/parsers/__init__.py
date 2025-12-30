from .rocketchat import RocketChatParser
from .ubuntu import UbuntuParser
from .zabbix import ZabbixParser
from .debian import DebianCloudParser
from .pexip_management_nodes import PexipManagementNodesParser 
from .pexip_conferencing_nodes import PexipConferencingNodesParser
from .snapd import SnapdParser
from .core_snaps import CoreSnapsParser

PARSER_REGISTRY = {
    "rocketchat": RocketChatParser,
    "ubuntu": UbuntuParser,
    "zabbix": ZabbixParser,
    "debian": DebianCloudParser,
    "pexip_manage": PexipManagementNodesParser,       
    "pexip_conf": PexipConferencingNodesParser,
    "snapd": SnapdParser,
    "cores": CoreSnapsParser,     
}
