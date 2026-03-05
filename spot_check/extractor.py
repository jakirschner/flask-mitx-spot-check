import tarfile
import os
import shutil

def extract_tarball(tarball_path, extract_dir):
    """Extract tarball to directory"""
    os.makedirs(extract_dir, exist_ok=True)
    with tarfile.open(tarball_path, 'r:gz') as tar:
        tar.extractall(path=extract_dir)

def delete_static_folder(extract_dir):
    """Delete the static folder to save space"""
    static_path = os.path.join(extract_dir, 'course', 'static')
    if os.path.exists(static_path):
        shutil.rmtree(static_path)
        print(f"Deleted static folder: {static_path}")