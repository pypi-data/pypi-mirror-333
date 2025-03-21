import os
import subprocess

from setuptools import Command, setup
from setuptools.command.build import build

class BuildJS(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        self.build_lib = self.get_finalized_command('build').build_lib

    def run(self):
        src_dir = 'mathjax/static/mathjax'
        dst_dir = os.path.join(self.build_lib, 'mathjax/static/mathjax')

        subprocess.check_call(
            ['npm', 'install'],
            cwd=src_dir, stdin=subprocess.DEVNULL,
        )
        subprocess.check_call(
            ['npm', 'run', '--silent', 'compile'],
            cwd=src_dir, stdin=subprocess.DEVNULL,
        )
        subprocess.check_call(
            ['npm', 'run', '--silent', 'make-components'],
            cwd=src_dir, stdin=subprocess.DEVNULL,
        )

        os.makedirs(dst_dir, exist_ok=True)
        os.rename(os.path.join(src_dir, 'js'), os.path.join(dst_dir, 'js'))
        os.rename(os.path.join(src_dir, 'es5'), os.path.join(dst_dir, 'es5'))

class CustomBuild(build):
    sub_commands = [('build_js', None)] + build.sub_commands

setup(
    cmdclass={
        'build': CustomBuild,
        'build_js': BuildJS,
    },
)
