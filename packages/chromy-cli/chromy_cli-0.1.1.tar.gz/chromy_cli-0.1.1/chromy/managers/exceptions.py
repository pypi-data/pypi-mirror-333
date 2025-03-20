class PermissionExists(Exception):
    """Exception raised when a permission already exists."""
    def __init__(self):
        super().__init__("Permission already exists.")


class PermissionNotFound(Exception):
    """Exception raised when a permission is not found."""
    def __init__(self):
        super().__init__("Permission not found.")