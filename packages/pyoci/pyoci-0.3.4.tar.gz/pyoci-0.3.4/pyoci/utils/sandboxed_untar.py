from os import path
import tarfile


def assert_no_path_traversal(tar_file: tarfile.TarFile, sandbox_root: str):
    for member in tar_file.getmembers():
        member_path = path.join(sandbox_root, member.name)
        
        member_root = path.commonprefix((sandbox_root, member_path))

        if not member_root == sandbox_root:
            raise Exception(f"Path traversal detected in tar file {tar_file.name}.")
