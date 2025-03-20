import os


def find():
    """Search for OneDrive folders across all drives"""
    onedrive_paths = set()

    # 1. Check environment variables (OneDrive, OneDriveCommercial, OneDriveConsumer)
    env_vars = [
        "OneDrive",
        "OneDriveCommercial",
        "OneDriveConsumer",
    ]
    for var in env_vars:
        path = os.getenv(var)
        if path and os.path.isdir(path):
            onedrive_paths.add(path)

    return list(onedrive_paths)
