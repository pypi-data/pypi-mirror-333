import os
import json

from typing import Dict, Any
from colorama import Fore


class ManifestManager:
    def __init__(self, fp):
        """
        :param fp: File path to root directory
        """
        self.fp = fp
        self.manifest = {}

    # Read manifest.json
    def read_manifest(self) -> Dict[str, Any]:
        with open(os.path.join(self.fp, 'manifest.json'), 'r') as file:
            manifest = json.load(file)

        self.manifest = manifest

        return manifest

    # Write manifest.json
    def write_manifest(self, manifest) -> None:
        with open(os.path.join(self.fp, 'manifest.json'), 'w') as file:
            json.dump(manifest, file, indent=4)

        print(f"[{Fore.GREEN}*{Fore.RESET}] Wrote to manifest.")

    # Add a key to the manifest
    def add_key(self, key: str, value: str) -> None:
        manifest = self.read_manifest()
        manifest[key] = value
        self.write_manifest(manifest)

    # Add a key to the manifest
    def remove_key(self, key: str) -> None:
        manifest = self.read_manifest()
        del manifest[key]
        self.write_manifest(manifest)

    # Create locales directory
    def enable_locales(self, default_locale: str = 'en') -> None:
        try:
            os.makedirs(os.path.join(self.fp, '_locales'), exist_ok=True)

        except PermissionError:
            raise PermissionError("Permission denied to create _locales directory.")

        print(f"[{Fore.GREEN}*{Fore.RESET}] Locale directory created.")

        self.add_key('default_locale', default_locale)

    # Add language
    def add_language(self, lang: str) -> None:
        locales_dir = os.path.join(self.fp, '_locales')
        lang_dir = os.path.join(locales_dir, lang)

        try:
            os.makedirs(lang_dir, exist_ok=True)

        except PermissionError:
            raise PermissionError("Permission denied to create language directory.")

        print(f"[{Fore.GREEN}*{Fore.RESET}] Language directory created: {lang_dir}")

        # Create messages.json file
        with open(os.path.join(lang_dir, 'messages.json'), 'w') as file:
            json.dump({}, file, indent=4)

        print(f"[{Fore.GREEN}*{Fore.RESET}] {lang} message.json file created.")