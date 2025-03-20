import os


def find(env_vars: list[str] = None) -> list[str]:
    """
    Search for OneDrive folders across all drives (Windows only).

    Args:
        env_vars (list[str], optional): Provided Parameters for OneDrive, e.g., "OneDrive", "OneDriveCommercial", "OneDriveConsumer" Defaults to None.

    Returns:
        list[str]: List of OneDrive paths.
    """
    onedrive_paths = set()

    if env_vars is None:
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
