import click
import os
import songlib.helpers.helper as helper

@click.group()
def cli():
    """ Provides easy access to study materials for songs."""
    helper.startup()
    pass

@cli.command()
@click.argument('songname', required=True)
@click.argument('mat_type', type=click.Choice(['tab', 'video']), required=True)
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
@click.option('--tab', '-t', is_flag=True, help='Opens a tab for this song.')
@click.option('--video', '-v', is_flag=True, help='Opens a video for this song.')
def mats(songname, tab, video):
    """ Opens materials for the specified song. """
    if tab:
        helper.open_spec_mat(songname, 'tab')
    elif video:
        helper.open_spec_mat(songname, 'video')
    else:
        helper.open_all_mats(songname)

@cli.command()
@click.argument('songname', required=True)
@click.option('--tab', '-t', is_flag=True, help='Removes a tab from this song.')
@click.option('--video', '-v', is_flag=True, help='Removes a video from this song.')
def rm(songname, tab, video):
    """ Removes materials for the specified song. """
    if tab:
        helper.rm_spec_helper(songname, 'tab')
    elif video:
        helper.rm_spec_helper(songname, 'video')
    else:
        helper.rm_helper(songname)

@cli.command()
def ls():
    """ Lists all the songs in your library. """
    helper.ls_helper()