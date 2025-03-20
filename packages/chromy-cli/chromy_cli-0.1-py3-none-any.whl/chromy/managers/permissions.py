from typing import List

from .exceptions import PermissionExists, PermissionNotFound
from .manifest import ManifestManager


class PermissionManager:
    fp: str
    _manifest: ManifestManager

    def __init__(self):
        self.permissions: List[str] = []

    def initialize(self, fp: str):
        self.fp = fp
        self._manifest = ManifestManager(fp)
        self.permissions = []

    # function wrapper
    def enable_locales(self, default_locale: str = 'en'):
        self._manifest.enable_locales(default_locale)

    # function wrapper
    def add_language(self, lang: str):
        self._manifest.add_language(lang)

    # Read permissions
    def read_permissions(self) -> List[str]:
        manifest = self._manifest.read_manifest()
        permissions = manifest['permissions'] if 'permissions' in manifest else []

        self.permissions = permissions

        return permissions

    # Write permissions
    def write_permissions(self) -> None:
        manifest = self._manifest.read_manifest()
        manifest['permissions'] = self.permissions
        self._manifest.write_manifest(manifest)

    # Add a permission to the list
    def add_permission(self, permission: str) -> None:
        if permission not in self.permissions:
            self.permissions.append(permission)
            self.permissions.sort()
            self.write_permissions()
        else:
            raise PermissionExists()

    # Remove a permission from the list
    def remove_permission(self, permission: str) -> None:
        if permission in self.permissions:
            self.permissions.remove(permission)
            self.write_permissions()
        else:
            raise PermissionNotFound
