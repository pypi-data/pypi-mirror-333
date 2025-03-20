import argparse
from iprm.load.native import NativeLoader
from iprm.gen.cmake import CMakeGenerator
from iprm.gen.meson import MesonGenerator
from iprm.core.session import Session


def main():
    parser = argparse.ArgumentParser(description='IPRM Command Line Interface')
    parser.add_argument('project_dir', help='The project root folder')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--emit-cmake', nargs='?', const='Ninja', metavar='generator',
                       help='Generate CMakeLists.txt files using the specified generator (default: Ninja)')
    group.add_argument('--emit-meson', nargs='?', const='ninja', metavar='generator',
                       help='Generate meson.build files using the specified generator (default: Ninja)')
    group.add_argument('--emit-graphviz', metavar='output_dir',
                       help='Generate a Graphviz dependency graph dot file and a SVG render file to the specified '
                            'output directory')

    # TODO: add `--consume-<system>` where for now the only plan is to have
    #  `scons` and MAYBE `msbuild` (*.vcxproj) files as a stretch goal
    # TODO: When adding SCons support, the main/vanilla scons can go into
    #  the main branch.
    #  For the FME-specific SCons addons, the work to support that should
    #  go into a separate branch (to keep the main infrastructure not
    #  fme-specific). In the supported build systems section of the
    #  README, mention "FME-SCons" as an addon in its own branch,
    #  mention the branch man and link to it

    # TODO: When adding FME-SCons support, if there are some
    #  hacks/hardcoded assumptions made to get things to work,
    #  that is fine and okay. It can be justified because the
    #  point is for us to never have to write SCons again, so
    #  the current assumptions will hold and therefore can be
    #  hardcoded. Once you have the .iprm version working on
    #  all platforms, the SConscript's can be thrown away

    # TODO: For scons loader, add a fla `--ext-modules <path/to/file>` which is
    #  a JSON file that contains absolute paths to extra python-loadable files
    #  that are needed in order to properly consume and parse the scripts
    args = parser.parse_args()
    project_dir = args.project_dir

    generator_class = None
    generator_kwargs = {}
    if args.emit_cmake:
        generator_class = CMakeGenerator
        generator_kwargs['generator'] = args.emit_cmake
    elif args.emit_meson:
        generator_class = MesonGenerator
        generator_kwargs['generator'] = args.emit_meson
    elif args.emit_graphviz:
        # TODO: support GraphVizGenerator
        generator_kwargs['output_dir'] = args.emit_graphviz
    assert generator_class is not None

    Session.create(project_dir)
    import platform
    loader = NativeLoader(project_dir, platform.system())

    generator = generator_class(loader, **generator_kwargs)
    generator.generate_project()

    Session.destroy()
