import click
import shutil
import os
import glob

@click.group()
def cli():
    pass

# add_to_package build/production/*.bin build/production/*.elf -O package/ -P production
@cli.command()
@click.argument('files', nargs=-1)
@click.option('-O', '--output', type=click.Path(), required=True)
@click.option('-P', '--package',required=False, default='')
def add_to_package(files, output, package):
    if not os.path.exists(output):
        os.makedirs(output)
    for file in files:
        for f in glob.glob(file):
            target = os.path.join(output, os.path.basename(f))
            # Add package name to the file as suffix
            if package != '':
                target = os.path.join(output, os.path.basename(f).replace('.bin', f'.{package}.bin').replace('.elf', f'.{package}.elf'))
            print(f'Copying {f} to {target}')
            shutil.copy(f, target)
            

@cli.command()
@click.argument('files', nargs=-1)
@click.option('-O', '--output', type=click.Path(), required=True)
def add_to_root(files, output):
    if not os.path.exists(output):
        os.makedirs(output)
    for file in files:
        for f in glob.glob(file):
            target = os.path.join(output, os.path.basename(f))
            shutil.copy(f, target)

@cli.command()
@click.argument('folders', nargs=-1)
@click.option('-O', '--output', type=click.Path(), required=True)
@click.option('-N', '--name', required=False, default='')
def add_folders(folders, output, name):
    if not os.path.exists(output):
        os.makedirs(output)

    for folder in folders:

        if len(glob.glob(folder)) == 0:
            raise Exception(f'No folders found for {folder}')
        
        for f in glob.glob(folder):
            target = os.path.join(output, os.path.basename(f), name)
            print(f'Copying {f} to {target}')
            # If exists remove the folder
            if os.path.exists(target):
                shutil.rmtree(target)

            # If souce does not exist, skip
            if not os.path.exists(f):
                raise Exception(f'{f} does not exist')
            
            shutil.copytree(f, target)
            
@cli.command()
@click.argument('from_path', nargs=1)
@click.argument('to_path', nargs=1)
def copy(from_path, to_path):
    if not os.path.exists(os.path.dirname(to_path)):
        os.makedirs(os.path.dirname(to_path))
    shutil.copy(from_path, to_path)

@cli.command()
@click.argument('path', nargs=1)
def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)   
    
@cli.command()
@click.argument('directory', nargs=1)
def remove(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    else:
        print(f'{directory} does not exist')

@cli.command()
@click.option('-O', '--output', type=click.Path(), required=True)
def add_version(output):
    version = os.popen('git describe --dirty --always --tags').read().strip()
    with open(os.path.join(output, f"version_{version}"), 'w') as f:
        f.write(version)


if __name__ == '__main__':
    cli()