#!/usr/bin/env python3

import subprocess
import os
import time

def exect(command):
    res = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    return res.stdout.read()

art = '                           *     .--.\n' \
      '                                / /  `\n' \
      '               +               | |\n' \
      '                      \'         \ \__,\n' \
      '                  *          +   \'--\'  *\n' \
      '                      +   /\\\n' \
      '         +              .\'  \'.   *\n' \
      '                *      /======\      +\n' \
      '                      ;:.  _   ;\n' \
      '                      |:. (_)  |\n' \
      '                      |:.  _   |\n' \
      '            +         |:. (_)  |          *\n' \
      '                      ;:.      ;\n' \
      '                    .\' \:.    / `.\n' \
      '                   / .-\'\':._.\'`-. \\\n' \
      '                   |/    /||\    \|\n' \
      '             jgs _..--\"\"\"````\"\"\"--.._\n' \
      '           _.-\'``                    ``\'-._\n' \
      '         -\'                                \'-\n' \
      '        Ndless 4.5 SDK Automated Installer v1.1\n' \
      '                 by trueToastedCode\n' \
      '    ' \
      'Thanks also to lights0123 & Vogtinator (GitHub)\n'

# print art and start
print(art)
if input('Start installation (n/y): ') != 'y':
    exit(0)

startTime = time.time()

# check current path (can maybe be deleted, but it did cause errors for me)
print('\n# check path')
path = os.path.abspath(os.getcwd())
print('path=' + path)
if ' ' in path:
    if (input(
            '\nWarning: Your path contains blank characters, this did cause errors for me. Do you really wan\'t to continue? (n/y):') != 'y'):
        exit(0)
else:
    print('ok.')

# check dependencies
dependencies = ['g++', 'git', 'libbinutils', 'libgmp-dev', 'libmpfr-dev', 'libmpc-dev', 'zlib1g-dev',
                'libboost-program-options-dev', 'wget', 'python3-dev', 'python2.7', 'texinfo', 'gcc-arm-none-eabi',
                'php-dev']
print('\n# installing dependencies')

# check if apt exists
aptExist = None
if 'install ok' in str(exect('dpkg -s apt')):
    aptExist = True

    # install dependencies
    i = 1
    for pkg in dependencies:
        if 'install ok' in str(exect('dpkg -s ' + pkg)):
            print('[{}/{}] {} already installed!'.format(i, len(dependencies), pkg))
        else:
            print('[{}/{}] Installing {}'.format(i, len(dependencies), pkg))
            os.system('sudo apt -y install ' + pkg)
        i += 1
else:
    aptExist = False

    # install dependencies manuel
    print('Automated package installation works only with apt. Please install the following packages manuel:')
    for pkg in dependencies:
        print(pkg)
    if (input('Continue (n/y)') != 'y'):
        exit(0)

# get login user
print('\n# get login user')
usr = os.getlogin()
print('user=' + usr)

# download ndless
print('\n# download ndless')
os.system('cd ' + path + ' && git clone --recursive https://github.com/ndless-nspire/Ndless.git')

# build toolchain
print('\n# build toolchain\nInfo: This process can take minutes to hours depending on your connection and power\n')
os.system('cd ' + path + '/Ndless/ndless-sdk/toolchain && ./build_toolchain.sh')

"""
# was necessary for me ?
if aptExist:
    os.system('sudo apt update')
"""

# verify build
print('\n# verify  build')

cm = 'echo $?'
res = str(exect(cm))

if res == 'b\'0\\n\'':
    print(cm + '=0\nok.')
else:
    print(cm + '!=0')
    if (input(
            'Error, output of \'' + cm + '\' should be \'0\'! However you can still test it yourself while keeping this running. If this is a bug, enter y!\nContinue (n/y): ') != 'y'):
        exit(1)

# add path environment variable
print('\n# add path environment variable')
pathVar = 'export PATH="' + path + '/Ndless/ndless-sdk/toolchain/install/bin:' + path + '/Ndless/ndless-sdk/bin:${PATH}"'
print('path_environment_variable=' + pathVar)
with open('/home/' + usr + '/.profile', 'a') as file:
    file.write('\n# ndless sdk\n' + pathVar)
    file.close()

# build ndless and sdk
pathCommand = pathVar[7:] + ' && '
print('\n# build ndless and sdk\nInfo: This process should take 5 minutes top\n')
os.system(pathCommand + 'cd Ndless && make')

print(
    '\n#####################################\nThe automated installer has finished!\nTo verify the installation the code runs "nspire-gcc". If everything has been setup correctly the output should look similiar to:'
    '\n\narm-none-eabi-gcc: fatal error: no input files\ncompilation terminated.\n#####################################\n\nnspire-gcc')
os.system(pathCommand + ' nspire-gcc')
print('\nScript completed in ' + str(int((time.time() - startTime) / 1000)) + 's')
 
