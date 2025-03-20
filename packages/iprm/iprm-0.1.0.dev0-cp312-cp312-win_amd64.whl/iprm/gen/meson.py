from itertools import zip_longest
from pathlib import Path
from iprm.util.env import Env
from iprm.util.dir import CurrentSourceDir
from iprm.gen.gen import Generator
from iprm.load.native import NativeLoader
from iprm.api.obj.project import Project
from iprm.api.obj.subdirectories import SubDirectories
from iprm.api.obj.cxx import CXXTarget
from iprm.api.obj.rust import RustTarget


class MesonGenerator(Generator):
    _native_file_path: Path = None

    def __init__(self, native_loader: NativeLoader, **kwargs):
        kwargs['build_dir'] = 'builddir'
        super().__init__(native_loader, **kwargs)

    def generator_name(self):
        return 'meson'

    def generated_file_name(self):
        return 'meson.build'

    def release_build_type(self):
        return 'release'

    @classmethod
    def _generate_project(cls, project: Project):
        # https://github.com/mesonbuild/meson/issues/1752#issuecomment-1216718818
        # Unfortunately, Meson has quite a cumbersome way to specify the compiler,
        # it essentially forces you to use CMakes toolchain file concept, as it has no
        # inline build script method to set your compiler. It would be really nice if
        # it was done in the default_options section of the project() function.
        # Maybe one day!
        cls._native_file_path = project.root_dir / f'{project.name}-meson-native.txt'
        native_file_content = [
            '[binaries]',
        ]
        cxx_compiler = project.cxx_compiler
        if cxx_compiler:
            native_file_content.append(f"cpp = '{cxx_compiler}'")
        rust_compiler = project.rust_compiler
        if rust_compiler:
            native_file_content.append(f"rust = '{rust_compiler}'")
        native_file_content.append('')
        with open(cls._native_file_path, 'w') as file:
            file.write('\n'.join(native_file_content))

        meson_content = [
            f"project('{project.name}', ",
        ]
        langs_dict = project.properties.get('languages', {})
        meson_content_def_options = ["\tdefault_options : [\n"]
        cxx_std_conformance = False
        if langs_dict:
            meson_content[-1] += '['
            langs_list = list(langs_dict.items())
            for (lang_type, lang_props), next_lang in zip_longest(langs_list, langs_list[1:], fillvalue=None):
                if lang_type == CXXTarget.__name__:
                    standard = lang_props.get(CXXTarget.STANDARD, None)
                    if standard:
                        meson_content_def_options[-1] += f"\t\t'cpp_std=c++{standard}',\n"
                    cxx_std_conformance = lang_props.get('conformance')
                elif lang_type == RustTarget.__name__:
                    pass
            meson_content[-1] += '],'

        meson_content_def_options[-1] += '\t]'

        meson_content.append(f"\tversion : '{project.properties.get('version', '0.1.0')}',")
        meson_content.extend(meson_content_def_options)
        meson_content.append(f')')
        meson_content.append('')

        # TODO: is this the best equivalent to what CMake can have? Or is there something better
        description = project.properties.get('description', None)
        if description:
            meson_content.append(f"summary('description', '{description}')")

        url = project.properties.get('url', None)
        if url:
            meson_content.append(f"summary('homepage_url', '{url}')")

        if Env.platform.windows and cxx_std_conformance:
            meson_content.append("if meson.get_compiler('cpp').get_id() == 'msvc'")
            meson_content.append("\tadd_project_arguments('/Zc:__cplusplus', '/permissive-', language : 'cpp')")
            meson_content.append('endif')
            meson_content.append('')
        return meson_content

    @classmethod
    def _generate_subdirectories(cls, subdirs: SubDirectories):
        meson_content = []
        dir_paths = subdirs.properties.get('directory_paths', [])
        if dir_paths:
            for dir_path in dir_paths:
                meson_content.append(f"subdir('{dir_path}')")
        meson_content.append('')
        return meson_content

    @classmethod
    def _generate_cxx(cls, cxx: CXXTarget):
        def add_sources(key):
            meson_content_sources = []
            sources_dict = cxx.properties.get(key, {})
            if sources_dict:
                for src_dir, src_files in sources_dict.items():
                    dir_path = src_dir.path
                    for src_file in src_files:
                        meson_content_sources.append(f"\t'{dir_path}/{src_file}',")
            return meson_content_sources

        target = cxx.name
        meson_content = []
        if cxx.is_app:
            meson_content.append(f"executable('{target}',")
        meson_content.extend(add_sources('headers'))
        meson_content.extend(add_sources('sources'))
        meson_content.append(')')
        meson_content.append('')
        return meson_content

    @classmethod
    def _generate_rust(cls, rust: RustTarget):
        target = rust.name
        manifest_dir, cargo_file = rust.properties.get('manifest')
        manifest_file = f"{cls.current_src_dir()} / '{cargo_file}'" \
            if manifest_dir == CurrentSourceDir() else f"'{manifest_dir.path.as_posix()}/{cargo_file}'"
        meson_content = [
            "cargo_profile = 'dev'",
            "if get_option('buildtype') == 'release' or get_option('buildtype') == 'minsize'",
            "\tcargo_profile = 'release'",
            "endif",
            "",
            f"custom_target('{target}',",
            f"\toutput : '{target}',",
            "\tconsole : true,",
            "\tcommand : [",
            "\t\tfind_program('cargo'),",
            "\t\t'build',",
            f"\t\t'--manifest-path', {manifest_file},",
            "\t\t'--target-dir', meson.current_build_dir(),",
            "\t\t'--profile', cargo_profile,",
        ]
        cargo_locked = rust.properties.get('cargo_locked', False)
        if cargo_locked:
            meson_content.append("\t\t'--locked'")
        meson_content.append("\t],")
        meson_content.append("\tbuild_by_default : true,")
        meson_content.append(")")
        meson_content.append('')
        return meson_content

    @classmethod
    def current_src_dir(cls):
        return 'meson.current_source_dir()'

    @classmethod
    def current_bin_dir(cls):
        return 'meson.current_build_dir()'

    @classmethod
    def _write_configure(cls, build_dir, build_system, build_type):
        return f'meson setup {build_dir} --backend={build_system} --buildtype={build_type} --native-file="{str(cls._native_file_path)}"'

    @classmethod
    def _write_build(cls, build_dir, _):
        return f'meson compile -C {build_dir} -j{'$(nproc)' if not Env.platform.windows else '%NUMBER_OF_PROCESSORS%'}'

    @classmethod
    def _write_test(cls, build_dir):
        return f'meson test -C {build_dir}'
