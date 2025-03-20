import click
from docketanalyzer_core import env, notabs


config_groups = list(set([key.group for key in env.keys.values() if key.group]))
config_groups_str = ", ".join(config_groups)


class ConfigGroup(click.ParamType):
    name = "group"

    def convert(self, value, param, ctx):
        if value not in config_groups and value is not None:
            self.fail(
                f"'{value}' is not a valid group. Choose from: {config_groups_str}",
                param,
                ctx,
            )
        return value


@click.command(
    help=notabs(f"""
        Configure your environment

        GROUP: Optional filter for a group of config keys (one of: {config_groups_str}).

        --reset: Reset your configuration to default values.

        Examples:

        \b
        da configure
        da configure pacer
        da configure --reset
    """)
)
@click.argument("group", type=ConfigGroup(), default=None, required=False)
@click.option(
    "--reset", is_flag=True, help="Reset the configuration to default values."
)
def configure(group, reset):
    env.configure(reset=reset, group=group)
