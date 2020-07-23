from netnir.core import Credentials
from netnir.constants import SERVICE_NAME, NETNIR_USER
from nornir.plugins.tasks.networking import netmiko_send_command, netmiko_send_config
import os


class Networking:
    """
    a networking class that utilizes nornir's netmiko plugin to interact with devices
    via SSH.

    :param nr: type obj (required)
    :param creds: type obj (optional)
    :param port: type int (optional)
    :param num_workers: type int (optional)
    :param service_name: type str (optional)

    .. code:: python
       from netnir.core import Networking
       from nornir import InitNornir

       nr = InitNornir()
       networking = Networking(nr=nr)
       networking.fetch(commands=['show version'])
       networking.config(commands=['ip route 10.0.0.0 255.0.0.0 null0'])
    """

    def __init__(self, nr, port=22, num_workers=None, service_name=SERVICE_NAME):
        self.nr = nr
        self.creds = Credentials(service_name=service_name, username=NETNIR_USER)
        self.creds.fetch()
        self.nr.inventory.defaults.username = self.creds.username
        self.nr.inventory.defaults.password = self.creds.password
        self.nr.inventory.defaults.port = port
        self.nr.config.core.num_workers = (
            num_workers if num_workers else self.nr.config.core.num_workers
        )

    def fetch(self, commands):
        """
        execute show commands on the remote device and return the results

        :param commands: type list
        :return: nornir results object
        """
        if isinstance(commands, list):
            output = list()

            for command in commands:
                result = self.nr.run(task=netmiko_send_command, command_string=command)
                output.append(result)
        else:
            output = self.nr.run(task=netmiko_send_command, command_string=commands)

        return output

    def config(self, commands):
        """
        execute configuration commands on a remote device and return the results

        :param commands: type list
        :return: nornir results object
        """
        output = self.nr.run(task=netmiko_send_config, config_commands=commands)

        return output
