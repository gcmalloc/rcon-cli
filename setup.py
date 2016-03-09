from setuptools import setup
setup(
      name='rcon-cli',
      version = '0.1',
      description = 'A nicer rcon interface in cli with completion',
      author = 'gcmalloc',
      url = 'http://github.com/gcmalloc/rcon',
      install_requires=['python-valve', 'prompt_toolkit', 'colorama'],
      scripts = ['rcon.py'])
