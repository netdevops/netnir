from netnir.helpers.scaffold.command import CommandScaffold
from netnir.plugins.template import template_file
from netnir.plugins.netmiko import netmiko_send_commands
from netnir.plugins.rosetta import convert_config_to_yang, convert_yang_to_config
from netnir.plugins.hier import hier_host
from netnir.helpers import output_writer
from netnir.helpers.common.args import config_to_yang, yang_to_config
from netnir.constants import OUTPUT_DIR
from nornir.plugins.functions.text import print_result


class ConfigPlan(CommandScaffold):
    """
    config plan cli plugin to render configuration plans, either by
    compiling from template or using hier_config to create a remediation
    plan
    """

    @staticmethod
    def parser(parser):
        """
        cli options parser

        :params parser: type obj
        """
        CommandScaffold.parser(parser)
        parser.add_argument(
            "--compile",
            nargs="?",
            const=True,
            help="compile configuration from template",
            required=False,
        )
        parser.add_argument(
            "--include-tags",
            action="append",
            help="hier_config include tags",
            required=False,
        )
        parser.add_argument(
            "--exclude-tags",
            action="append",
            help="hier_config exclude tags",
            required=False,
        )
        config_to_yang(parser)
        yang_to_config(parser)

    def run(self):
        """
        cli execution

        :params template_file: type str

        :returns: result string
        """
        self.nr = self._inventory()

        if self.args.config_to_yang:
            results = self.nr.run(
                task=convert_config_to_yang,
                config_file=self.args.config_to_yang,
                name="CONVERT CONFIGURATION TEXT TO YANG MODEL",
                num_workers=self.args.workers,
                dry_run=self.args.X,
                severity_level=self._verbose()["level"],
                to_console=self._verbose()["to_console"],
            )
            print_result(result=results, severity_level=self._verbose()["level"])
            return results

        if self.args.yang_to_config:
            results = self.nr.run(
                task=convert_yang_to_config,
                yang_model=self.args.yang_to_config,
                name="CONVERT YANG MODEL TO CONFIGURATION TEXT",
                num_workers=self.args.workers,
                dry_run=self.args.X,
                severity_level=self._verbose()["level"],
                to_console=self._verbose()["to_console"],
            )
            print_result(result=results, severity_level=self._verbose()["level"])
            return results

        results = self.nr.run(
            task=template_file,
            template_file="main.conf.j2",
            output_file="compiled.conf",
            name="COMPILE TEMPLATES",
            num_workers=self.args.workers,
            dry_run=self.args.X,
            severity_level=self._verbose()["level"],
            to_console=self._verbose()["to_console"],
        )
        output_writer(nornir_results=results, output_file="compiled.conf")
        print_result(result=results, severity_level=self._verbose()["level"])

        if self.args.compile:
            return results

        results = self.nr.run(
            task=netmiko_send_commands,
            commands="show running",
            name="FETCH RUNNING CONFIG",
            num_workers=self.args.workers,
            dry_run=self.args.X,
            severity_level=self._verbose()["level"],
            to_console=self._verbose()["to_console"],
        )
        output_writer(nornir_results=results, output_file="running.conf")
        print_result(result=results, severity_level=self._verbose()["level"])

        results = self.nr.run(
            task=hier_host,
            include_tags=self.args.include_tags,
            exclude_tags=self.args.exclude_tags,
            running_config="running.conf",
            compiled_config="compiled.conf",
            config_path=OUTPUT_DIR,
            load_file=True,
            name="RENDER REMEDIATION CONFIG",
            num_workers=self.args.workers,
            dry_run=self.args.X,
            severity_level=self._verbose()["level"],
            to_console=self._verbose()["to_console"],
        )
        output_writer(nornir_results=results, output_file="remediation.conf")
        print_result(result=results, severity_level=self._verbose()["level"])

        return results
