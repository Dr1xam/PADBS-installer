from .rocketchat import RocketChatParser
from .ubuntu import UbuntuParser
from .zabbix import ZabbixParser
from .debian import DebianCloudParser

PARSER_REGISTRY = {
    "rocketchat": RocketChatParser,
    "ubuntu": UbuntuParser,
    "zabbix": ZabbixParser,
    "debian": DebianCloudParser,
}
