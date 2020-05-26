import click
import validators
import json
import os.path

ROOT = os.path.dirname(os.path.dirname(__file__))
FILEPATH = os.path.abspath('data/songs.json')
SONGFILE = os.path.join(ROOT, FILEPATH)

def startup():
    exists = os.path.exists(SONGFILE)
    if not exists:
        init = {"songs": []}
        with click.open_file(SONGFILE, 'w') as f:
            json.dump(init, f, indent=4)

def get_song_dump():
    with click.open_file(SONGFILE, 'r') as f:
        song_dump = json.load(f)
    
    return song_dump

def get_curr_song(songname, songs):
    song = next((song for song in songs if song['name'] == songname), None)
    return song

def get_materials(song, mat_type):
    materials = song['tabs'] if mat_type == 'tab' else song['videos']
    return materials

def init(songname="", mat_type=""):
    song_dump = get_song_dump()
    songs = song_dump['songs']
    song = get_curr_song(songname, songs) if songname else None
    materials = get_materials(song, mat_type) if song and mat_type else None

    return song_dump, songs, song, materials

def validate_sources(mat_source):
    valid = os.path.isfile(mat_source) or validators.url(mat_source)
    return valid

def duplicate_sources(songname, mat_type, mat_source):
    _, _, _, materials = init(songname, mat_type)
    dupes = [mat for mat in materials if mat['source'] == mat_source]
    return dupes

def duplicate_titles(songname, mat_type, mat_title):
    _, _, _, materials = init(songname, mat_type)
    dupes = [mat for mat in materials if mat['title'] == mat_title]
    return dupes

def get_mat_choice(songname, mat_type, action):
    click.echo('Multiple {}s found for this song.'.format(mat_type))

    _, _, _, materials = init(songname, mat_type)

    for i, mat in enumerate(materials, start=1):
        click.echo('[{}] {}'.format(i, mat['title']))
    click.echo('Which would you like to {}?'.format(action))

    while True:
            try:
                choice = int(input('')) - 1
            except ValueError:
                click.echo('Error: Input must be a number from {} to {}.'.format('1', str(len(materials))))
                continue

            if not 0 <= choice < len(materials):
                click.echo('Error: Input must be a number from {} to {}.'.format('1', str(len(materials))))
                continue
            else:
                break
        
    return choice

def open_spec_mat(songname, mat_type):
    _, _, song, materials = init(songname, mat_type)

    if not song:
        raise click.ClickException('Currently \'{}\' does not exist in your library.'.format(songname.title()))

    if not materials:
        raise click.ClickException('Currently no {}s for \'{}.\''.format(mat_type, songname.title()))

    cnt = len(materials)
    choice = 0 if cnt == 1 else get_mat_choice(songname, mat_type, 'view')

    click.launch(materials[choice]['source'])

def open_all_mats(songname):
    _, _, song, _ = init(songname)

    if not song:
        raise click.ClickException('Currently \'{}\' does not exist in your library.'.format(songname.title()))

    tabs, videos = get_materials(song, 'tab'), get_materials(song, 'video')
    tab_cnt, video_cnt = len(tabs), len(videos)

    if not tabs and videos:
        click.echo('Currently no tabs for \'{}.\' Opening just the video(s).'.format(songname.title()))
        open_spec_mat(songname, 'video')
        return
    elif not videos and tabs:
        click.echo('Currently no videos for \'{}.\' Opening just the tab(s).'.format(songname.title()))
        open_spec_mat(songname, 'tab')
        return
    elif not tabs and not videos:
        raise click.ClickException('Currently no tabs or videos for \'{}.\''.format(songname.title()))

    action = 'view'
    tab_choice = 0 if tab_cnt == 1 else get_mat_choice(songname, 'tab', action)
    video_choice = 0 if video_cnt == 1 else get_mat_choice(songname, 'video', action)

    click.launch(tabs[tab_choice]['source'])
    click.launch(videos[video_choice]['source'])

def add_helper(songname, mat_type, mat_title, mat_source):
    valid = validate_sources(mat_source)
    if not valid:
        raise click.ClickException('Source provided is not a valid file/url.')

    song_dump, songs, song, materials = init(songname, mat_type)
    mat = {"title": mat_title, "source": mat_source}

    if not song:
        tabs = [mat] if mat_type == 'tab' else []
        videos = [mat] if mat_type == 'video' else []
        entry = {"name": songname, "tabs": tabs, "videos": videos}

        songs.append(entry)
    else:
        dupe_source = duplicate_sources(songname, mat_type, mat_source)
        if dupe_source:
            raise click.ClickException('Source provided already exists for \'{}.\''.format(songname.title()))

        dupe_title = duplicate_titles(songname, mat_type, mat_title)
        if dupe_title:
            raise click.ClickException('Source with the title provided already exists for \'{}.\''.format(songname.title()))

        song['tabs'].append(mat) if mat_type == 'tab' else song['videos'].append(mat)

    with click.open_file(SONGFILE, 'w') as f:
        f.seek(0)
        json.dump(song_dump, f, indent=4) 

    click.echo('Successfully added {} to \'{}.\''.format(mat_type, songname.title()))

def rm_helper(songname):
    song_dump, songs, song, _ = init(songname)

    if not song:
        raise click.ClickException('Currently \'{}\' does not exist in your library.'.format(songname.title()))

    songs.remove(song)
    with click.open_file(SONGFILE, 'w') as f:
        f.seek(0)
        json.dump(song_dump, f, indent=4) 

    click.echo('Successfully removed \'{}.\''.format(songname.title()))

def rm_spec_helper(songname, mat_type):
    song_dump, songs, song, materials = init(songname, mat_type)

    if not song:
        raise click.ClickException('Currently \'{}\' does not exist in your library.'.format(songname.title()))

    if not materials:
        raise click.ClickException('Currently no {}s for \'{}.\''.format(mat_type, songname.title()))

    cnt = len(materials)
    choice = 0 if cnt == 1 else get_mat_choice(songname, mat_type, 'remove')

    title = materials[choice]['title']
    mat = next((mat for mat in materials if mat['title'] == title), None)
    materials.remove(mat)

    if not song['tabs'] and not song['videos']:
        songs.remove(song)

    with click.open_file(SONGFILE, 'w') as f:
        f.seek(0)
        json.dump(song_dump, f, indent=4)
    
    click.echo('Successfully removed {} for \'{}.\''.format(mat_type, songname.title()))

def ls_helper():
    _, songs, _, _ = init()

    if not songs:
        raise click.ClickException('Currently no songs in your library.')

    song_names = [song.get('name') for song in songs]
    song_names.sort()

    for i, name in enumerate(song_names, start=1):
        click.echo('[{}] {}'.format(i, name.title()))