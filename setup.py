from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = ['pyglet'], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.py', base=base, targetName = 'leviball')
]

setup(name='Leviball',
      version = '1.0a',
      description = 'Avoid those little things in your way',
      options = dict(build_exe = buildOptions),
      executables = executables)
