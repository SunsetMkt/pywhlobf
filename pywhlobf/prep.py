import zipfile
import iolite as io


def extract_tags(input_whl):
    input_whl = io.file(input_whl, exists=True)

    if input_whl.suffix != '.whl':
        raise RuntimeError(f'{input_whl} does not ends with ".whl".')

    # https://www.python.org/dev/peps/pep-0427/
    name = input_whl.stem
    components = name.split('-')
    build_tag = None
    if len(components) == 5:
        distribution, version, _, _, _ = components
    elif len(components) == 6:
        distribution, version, build_tag, _, _, _ = components

    return distribution, version, build_tag


def unzip_wheel(input_whl, output_folder):
    out_fd = io.folder(output_folder, reset=True)
    with zipfile.ZipFile(input_whl) as zip_file:
        zip_file.extractall(out_fd)


def locate_py_files(input_folder):
    in_fd = io.folder(input_folder, exists=True)
    return list(in_fd.glob('**/*.py'))


def debug():
    import os
    pywhlobf_data = os.getenv('PYWHLOBF_DATA')
    assert pywhlobf_data

    print(extract_tags(f'{pywhlobf_data}/prep/textwolf-0.9.0-py3-none-any.whl'))

    unzip_wheel(
        f'{pywhlobf_data}/prep/textwolf-0.9.0-py3-none-any.whl',
        f'{pywhlobf_data}/prep/textwolf-0.9.0',
    )

    py_files = locate_py_files(f'{pywhlobf_data}/prep/textwolf-0.9.0')
    print(py_files)
