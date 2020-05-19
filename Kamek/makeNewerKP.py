# Imports
import os
from shutil import copyfile
import sys
import platform


# Get the path of this script's folder
cwd = os.path.dirname(os.path.realpath(sys.argv[0])).replace("\\", "/")

# Change the current working directory to it
os.chdir(cwd)

# Insert 'tools' to sys.path so we can import modules from there
sys.path.insert(0, os.path.join(cwd, 'tools'))

if not os.path.isdir('processed'):
    os.mkdir('processed')

# Import and execute 'mapfile_tool'
import mapfile_tool
mapfile_tool.main()

import kamek

# Set the needed parameters for kamek
if platform.system() == 'Windows':
    kamek.gcc_path = 'D:/devkitPPC_r19/devkitPPC/bin/'

else:
    kamek.gcc_path = '/opt/devkitpro/devkitPPC/bin/'
    kamek.use_wine = True

kamek.use_rels = False
kamek.use_mw = True
kamek.gcc_type = 'powerpc-eabi'
kamek.mw_path = 'tools/'
kamek.fast_hack = True

print(kamek.version_str)
print('')

project = kamek.KamekProject(os.path.normpath('NewerProjectKP.yaml'))
project.configs = kamek.read_configs('kamek_configs.yaml')
project.build()

print('compile successful')

copy_files = [
    ('NewerASM/n_%s_loader.bin', 'Build/System%s.bin'),
    ('NewerASM/n_%s_dlcode.bin', 'Build/DLCode%s.bin'),
    ('NewerASM/n_%s_dlrelocs.bin', 'Build/DLRelocs%s.bin'),
]

if not os.path.isdir('Build'):
    os.mkdir('Build')

for src, dest in copy_files:
    copyfile(src % 'pal', dest % 'EU_1')
    copyfile(src % 'pal2', dest % 'EU_2')
    copyfile(src % 'ntsc', dest % 'US_1')
    copyfile(src % 'ntsc2', dest % 'US_2')
    copyfile(src % 'jpn', dest % 'JP_1')
    copyfile(src % 'jpn2', dest % 'JP_2')

print('Built all!')
