import sys
import argparse
import subprocess
import os


def launch_studio():
    from iprm.util.env import Env
    from iprm import studio

    studio_dir_path = os.path.dirname(studio.__file__)
    studio_exe_name = f'studio{".exe" if Env.plat.windows else ""}'
    studio_exe_path = os.path.join(studio_dir_path, studio_exe_name)
    import iprm
    try:
        # Launch detached process
        if Env.plat.windows:
            # DETACHED_PROCESS ensures complete detachment on Windows
            subprocess.Popen(
                [studio_exe_path, *sys.argv[1:]],  # Forward any CLI arguments
                creationflags=subprocess.DETACHED_PROCESS,
                start_new_session=True
            )
        else:
            # On Unix-like systems, we use start_new_session
            subprocess.Popen(
                [studio_exe_path, *sys.argv[1:]],
                start_new_session=True
            )
        return 0

    except Exception as e:
        print(f"Unable to launch IPRM Studio: {e}", file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(description="IPRM Studio")
    parser.add_argument(
        "project_dir",
        type=str,
        nargs='?',
        help="Path to the project directory"
    )

    args = parser.parse_args()
    sys.exit(launch_studio())
