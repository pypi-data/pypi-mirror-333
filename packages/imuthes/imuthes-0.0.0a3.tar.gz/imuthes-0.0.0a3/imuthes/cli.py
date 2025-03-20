import pathlib
import click
from hakisto.click import hakisto_severity, hakisto_short_trace, hakisto_process_all, hakisto_file


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@hakisto_severity()
@hakisto_file(default=False)
@hakisto_short_trace()
@click.pass_context
def main(ctx, **kwargs):
    """Imuthes Utilities"""
    hakisto_process_all(**kwargs)
    ctx.ensure_object(dict)


@main.command()
@click.option("-t", "--target", type=click.Path(exists=True, path_type=pathlib.Path), required=True, help="Target")
@click.option("-l", "--link", type=click.Path(path_type=pathlib.Path), required=True, help="will be created")
@click.pass_context
def make_link(ctx, target, link):
    """Create symbolic link (or junction)"""

    make_link(target=target, link=link)
