import subprocess
import click
import glob
import os

from pathlib import Path

env = os.environ.copy()
env['CLICOLOR_FORCE'] = '1'

GREEN = '\033[0;32m'
RED = '\033[0;31m'
NC = '\033[0m'

@click.command()
@click.option('-d', '--debug', is_flag=True)
def test(debug: bool):
    "Runs the last saved c++ file against the corresponding test cases"
    current_dir = os.getcwd()
    cpp_files = glob.glob('*.cpp', root_dir=current_dir)
    if not cpp_files:
        click.echo("Error: No .cpp files found in current directory")
        return 1

    latest_cpp = Path(sorted(cpp_files, key=os.path.getmtime, reverse=True)[0]).stem
    make_command = ['make', latest_cpp]
    if debug:
        make_command.append('CPPFLAGS="-DDEBUG"')
    make_process = subprocess.run(make_command,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  text=True,
                                  cwd=current_dir,
                                  env=env)
    
    click.echo(f"code = {make_process.returncode}")
    if make_process.returncode != 0:
        click.echo("Detected error compiling code. Stopping now!")
        click.echo(f"ERROR:\n{make_process.stdout}", color=True)
        return 2

    test_input = sorted(glob.glob(f"in/{latest_cpp}[0-9]*", root_dir=current_dir))
    test_output = sorted(glob.glob(f"out/{latest_cpp}[0-9]*", root_dir=current_dir))

    for i in range(len(test_input)):
        with open(test_input[i], 'r') as infile:
            result = subprocess.run(f'./{latest_cpp}', stdin=infile,
                                    capture_output=True,
                                    text=True,
                                    cwd=current_dir)

        actual_output = result.stdout
        actual_lines = actual_output.strip().split('\n')
        
        if i >= len(test_output):
            expected_content = 'OUTPUT NOT FOUND!'
            expected_lines = [expected_content]
        else:
            with open(test_output[i], 'r') as f:
                expected_content = f.read().strip()
                expected_lines = expected_content.split('\n')

        while expected_lines and not expected_lines[-1]:
            expected_lines.pop()
        while actual_lines and not actual_lines[-1]:
            actual_lines.pop()

        if expected_lines == actual_lines:
            click.echo(f"{GREEN}Test {i+1}: PASSED{NC}")
        else:
            click.echo(f"{RED}Test {i+1}: FAILED{NC}")
            click.echo("Expected:")
            click.echo(expected_content)
            click.echo("Got:")
            click.echo(actual_output)

    os.unlink(latest_cpp)
    return make_process.returncode