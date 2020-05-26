import click
import songlib.helpers.helper as helper

@click.group()
def cli():
    """ Provides easy access to study materials for songs."""
    helper.startup()
    pass

@cli.command()
@click.argument('songname', required=True)
@click.argument('mat_type', type=click.Choice(['chart', 'video']), required=True)
@click.argument('mat_title', required=True)
@click.argument('mat_source', required=True)
def add(songname, mat_type, mat_title, mat_source):
    """ Adds specified material to the specified song. 

    MAT_TITLE is the title given to the material you want to add.

    MAT_SOURCE is the file path/url of the material you want to add.
    """
    helper.add_helper(songname, mat_type, mat_title, mat_source)

@cli.command()
@click.argument('songname', required=True)
@click.option('--chart', '-c', is_flag=True, help='Opens a chart for this song.')
@click.option('--video', '-v', is_flag=True, help='Opens a video for this song.')
def mats(songname, chart, video):
    """ Opens materials for the specified song. """
    if chart:
        helper.open_spec_mat(songname, 'chart')
    elif video:
        helper.open_spec_mat(songname, 'video')
    else:
        helper.open_all_mats(songname)

@cli.command()
@click.argument('songname', required=True)
@click.option('--chart', '-c', is_flag=True, help='Removes a chart from this song.')
@click.option('--video', '-v', is_flag=True, help='Removes a video from this song.')
def rm(songname, chart, video):
    """ Removes materials for the specified song. """
    if chart:
        helper.rm_spec_helper(songname, 'chart')
    elif video:
        helper.rm_spec_helper(songname, 'video')
    else:
        helper.rm_helper(songname)

@cli.command()
def ls():
    """ Lists all the songs in your library. """
    helper.ls_helper()