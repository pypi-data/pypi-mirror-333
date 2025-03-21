
# @this module contains tools for downloading files from
# - github release

from tqdm import tqdm

import typing
import pathlib
import requests


# @the github api for every release query.
GITHUB_API = "https://api.github.com/repos/{username}/{repository}/releases/{version}"


def download(
        filename: str,
        github_username: str,
        github_repository: str,
        release_version: str = 'latest',
        output_directory: str = None,
) -> typing.Tuple[bool, str]:
    # @customize the github_api based on given parameters
    api = GITHUB_API.replace('{username}', github_username) \
        .replace('{repository}', github_repository) \
        .replace('{version}', release_version)
    
    # @connect to the github api
    response = requests.get(api)

    # @try and check for any errors.
    try: response.raise_for_status()
    except: return False, "@network-failure"
    
    # @convert the response into json
    response_json = response.json()

    # @initialize a variable to None and
    # - try to find the filename given in the given release
    asset_url = None
    for asset in response_json['assets']:
        if asset['name'] == filename:
            asset_url = asset['browser_download_url']
            break
    
    # @if asset url is not found, return error
    if asset_url is None:
        return False, "@file-not-found"
    
    # @start the download process to the output directory.
    # - check if the output directory exists and is a directory.
    if output_directory is None:
        output_directory = pathlib.Path.cwd()
    outdir = pathlib.Path(output_directory).expanduser().resolve()

    if not outdir.exists() or not outdir.is_dir():
        return False, "@output-destination-must-be-a-directory"
    
    # - start the download
    response_d = requests.get(asset_url, stream=True)
    total_size = int(response_d.headers.get('content-length', 0))
    blocksize = 1024 # 1KB


    with open(outdir.joinpath(filename), 'wb') as f, tqdm(
        desc="Downloading " + filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=blocksize,
        bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]',
        ncols=90
    ) as tqdmbar:
        
        try:
            for data in response_d.iter_content(blocksize):
                f.write(data)
                tqdmbar.update(len(data))
        except KeyboardInterrupt:
            return False, "Interrupt"
    
    return True, ""