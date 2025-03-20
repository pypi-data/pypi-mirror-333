import os
import subprocess
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys

root_dir_path = os.path.dirname(__file__)
src_dir_path = os.path.abspath(os.path.join(root_dir_path, 'src', 'iprm', 'util'))
sys.path.append(src_dir_path)


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

    @classmethod
    def _find_vcvarsall(cls):
        from vcvarsall import find_vcvarsall
        return find_vcvarsall()

    def vcvarsall_script(self, cmake_command):
        vcvarsall_path = self._find_vcvarsall()
        assert vcvarsall_path is not None
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.bat', delete=False, mode='w') as vcvarsall_batch:
            temp_script_path = vcvarsall_batch.name
            vcvarsall_batch.write("@echo off\n")
            vcvarsall_batch.write(f'call "{vcvarsall_path}" x64\n')
            vcvarsall_batch.write(f'{cmake_command}\n')
            return temp_script_path


class IPRMBuild(build_ext):
    def run(self):
        try:
            subprocess.check_output(['ninja', '--version'])
        except OSError:
            raise RuntimeError("Ninja must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        try:
            subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        if isinstance(ext, CMakeExtension):
            configure = [
                'cmake',
                '-G', 'Ninja',
                '-S', '.',
                '-B', 'build_pkg',
                '-DCMAKE_BUILD_TYPE=RelWithDebInfo',
                '-DIPRM_INCLUDE_STUDIO_CXX_IMPL=FALSE',
                '-DIPRM_INCLUDE_STUDIO_RUST_IMPL=FALSE',
                '-DIPRM_INCLUDE_STUDIO_WEB_IMPL=FALSE',
            ]
            build = [
                'cmake',
                '--build', 'build_pkg',
                '--config', 'RelWithDebInfo',
                '--parallel',
                '--verbose',
            ]
            src_dir = os.path.abspath(os.path.join('src', 'iprm'))
            import platform
            if platform.system() == "Windows":
                subprocess.check_call(ext.vcvarsall_script(' '.join(configure)), cwd=src_dir)
                subprocess.check_call(ext.vcvarsall_script(' '.join(build)), cwd=src_dir)
            else:
                subprocess.check_call(configure, cwd=src_dir)
                subprocess.check_call(build, cwd=src_dir)
            install = [
                'cmake',
                '--install', 'build_pkg',
                '--config', 'RelWithDebInfo',
            ]
            #subprocess.check_call(' '.join(install), cwd=src_dir)


setup(
    ext_modules=[CMakeExtension("IPRM Core and Extension Modules", "src"), ],
    cmdclass={"build_ext": IPRMBuild},
)
