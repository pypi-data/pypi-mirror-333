import click


@click.group()
def plugins():
    pass


@plugins.command()
@click.argument("plugin_name")
def install(plugin_name: str):
    click.echo(f"Installing plugin: {plugin_name}")


@plugins.command()
def list():
    click.echo("Installed plugins:")
