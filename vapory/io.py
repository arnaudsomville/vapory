"""
All the advanced Input/Output operations for Vapory
"""

import re
import os
import shutil
import subprocess
from pathlib import Path
import tempfile
from .config import POVRAY_BINARY

try:
    import numpy
    numpy_found=True
except:
    numpy_found=False

try:
    from IPython.display import Image
    ipython_found=True
except:
    ipython_found=False

def ppm_to_numpy(filename=None, buffer=None, byteorder='>'):
    """Return image data from a raw PGM/PPM file as numpy array.

    Format specification: http://netpbm.sourceforge.net/doc/pgm.html

    """

    if not numpy_found:
        raise IOError("Function ppm_to_numpy requires numpy installed.")

    if buffer is None:
        with open(filename, 'rb') as f:
            buffer = f.read()
    try:
        header, width, height, maxval = re.search(
            b"(^P\d\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
    except AttributeError:
        raise ValueError("Not a raw PPM/PGM file: '%s'" % filename)

    cols_per_pixels = 1 if header.startswith(b"P5") else 3

    dtype = 'uint8' if int(maxval) < 256 else byteorder+'uint16'
    arr = numpy.frombuffer(buffer, dtype=dtype,
                           count=int(width)*int(height)*3,
                           offset=len(header))

    return arr.reshape((int(height), int(width), 3))

def render_povstring(string, outfile=None, height=None, width=None,
                     quality=None, antialiasing=None, remove_temp=True,
                     show_window=False, temporarypovfile=None, includedirs=None,
                     output_alpha=False):

    """ Renders the provided scene description with POV-Ray.

    Parameters
    ------------

    string
      A string representing valid POVRay code. Typically, it will be the result
      of scene(*objects)

    outfile
      Name of the PNG file for the output.
      If outfile is None, a numpy array is returned (if numpy is installed).
      If outfile is 'ipython' and this function is called last in an IPython
      notebook cell, this will print the result in the notebook.

    height
      height in pixels

    width
      width in pixels

    output_alpha
      If true, the background will be transparent,
    rather than the default black background.  Note
    that this option is ignored if rendering to a
    numpy array, due to limitations of the intermediate
    ppm format.

    """

    pov_file = temporarypovfile or '__temp__.pov'
    with open(pov_file, 'w+') as f:
        f.write(string)

    return_np_array = (outfile is None)
    display_in_ipython = (outfile=='ipython')

    format_type = "P" if return_np_array else "N"

    if return_np_array:
        outfile='-'

    if display_in_ipython:
        outfile = '__temp_ipython__.png'

    cmd = [POVRAY_BINARY, pov_file]
    if height is not None: cmd.append('+H%d'%height)
    if width is not None: cmd.append('+W%d'%width)
    if quality is not None: cmd.append('+Q%d'%quality)
    if antialiasing is not None: cmd.append('+A%f'%antialiasing)
    if output_alpha: cmd.append('Output_Alpha=on')
    if not show_window:
        cmd.append('-D')
    else:
        cmd.append('+D')
    if includedirs is not None:
        for dir in includedirs:
            cmd.append('+L%s'%dir)
    cmd.append("Output_File_Type=%s"%format_type)
    cmd.append("+O%s"%outfile)
    process = subprocess.Popen(cmd, stderr=subprocess.PIPE,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE)

    out, err = process.communicate(string.encode('ascii'))

    if remove_temp:
        os.remove(pov_file)

    if process.returncode:
        print(type(err), err)
        raise IOError("POVRay rendering failed with the following error: "+err.decode('ascii'))

    if return_np_array:
        return ppm_to_numpy(buffer=out)

    if display_in_ipython:
        if not ipython_found:
            raise("The 'ipython' option only works in the IPython Notebook.")
        return Image(outfile)

def render_docker(string, outfile=None, height=None, width=None,
                  quality=None, antialiasing=None,
                  temporarypovfile=None, includedirs=None,
                  output_alpha=False, resources_folder=None):

    pov_file = str(Path(temporarypovfile or '__temp__.pov').resolve())
    with open(pov_file, 'w+') as f:
        f.write(string)

    return_np_array = (outfile is None)
    display_in_ipython = (outfile == 'ipython')

    format_type = "P" if return_np_array else "N"

    if return_np_array:
        outfile = '-'

    if display_in_ipython:
        outfile = '__temp_ipython__.png'

    if resources_folder is None:
        tmp_path = tempfile.gettempdir()
        resources_folder = Path(tmp_path).joinpath("empty_resources_folder")
        resources_folder.mkdir(parents=True, exist_ok=True)

    docker_output_directory = Path.home().joinpath('vapory_images') #Hardcoded in docker-compose.yml
    docker_output_directory.mkdir(parents=True, exist_ok=True)

    cmd = [
        "bash",
        f"{Path(__file__).parent.joinpath('docker_container/run_povray_container.sh')}",
        f"{pov_file}"
    ]
    cmd.append(str(resources_folder))

    if width is not None:
        cmd.append(str(width))  # Convert to str
    if height is not None:
        cmd.append(str(height))  # Convert to str

    extra_args = []
    if quality is not None:
        extra_args.append(f'+Q{quality}')
    if antialiasing is not None:
        extra_args.append(f'+A{antialiasing}')
    if output_alpha:
        extra_args.append('Output_Alpha=on')

    if includedirs is not None:
        for dir in includedirs:
            extra_args.append(f'+L{dir}')
    extra_args.append(f"Output_File_Type={format_type}")
    extra_args.append(f"+O{outfile}")

    # Correctly extend extra_args into cmd
    cmd.extend(extra_args)
    print("Commande exécutée :", cmd)

    process = subprocess.run(cmd, capture_output=True, text=True)

    # Stocke et affiche les logs
    logs = []
    if process.stdout:
        # print(process.stdout, end='')  # Affiche stdout
        logs.extend(process.stdout.splitlines())  # Ajoute les lignes à la liste

    if process.stderr:
        # print(process.stderr, end='')  # Affiche stderr
        logs.extend(process.stderr.splitlines())  # Ajoute les lignes à la liste

    # Vérifie si "Render failed" est présent dans les logs
    if any("Render failed" in log for log in logs):
        print("\n[Erreur détectée] Voici les logs complets :\n")
        print("".join(logs))  # Affiche tous les logs
        raise IOError("POVRay rendering failed due to 'Render failed' in logs.")

    # Vérifie le code de retour du processus
    if process.returncode:
        print("\n[Erreur détectée] Voici les logs complets :\n")
        print("".join(logs))  # Affiche tous les logs
        raise IOError(f"POVRay rendering failed with exit code {process.returncode}")

    if return_np_array:
        return ppm_to_numpy(buffer=process.stdout)

    if display_in_ipython:
        if not ipython_found:
            raise("The 'ipython' option only works in the IPython Notebook.")
        return Image(outfile)

    file_path = Path(outfile)
    if file_path.is_file():
        file_path.parent.mkdir(parents=True, exist_ok=True)
    else:    
        file_path.mkdir(parents=True, exist_ok=True)

    shutil.move(str(docker_output_directory.joinpath('output.png')), str(Path(outfile).resolve()))
