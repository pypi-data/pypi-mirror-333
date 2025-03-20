#!/usr/bin/env python3

import cmd
import json
import os
import sys

import colorama
from colorama import Fore

import inquirer

from .managers.permissions import PermissionManager
from .blueprint_files import *
from .theme import CoolTheme

colorama.init()
version = "0.0.1"

init_questions = [
    inquirer.Confirm(
        'popup',
        message="Would you like to add a popup?",
        default=True
    ),
    inquirer.Confirm(
        'options',
        message="Would you like to add an options page?",
        default=True
    ),
    inquirer.Confirm(
        'assets',
        message='Would you like an additional directory for other assets (images, etc)?',
        default=True
    ),
    inquirer.Checkbox(
        'scripts',
        message='Which scripts would you like to add? (Press space to select)',
        choices=[
            'background.js',
            'content.js',
            'popup.js',
            'options.js',
        ],
        default=['background.js', 'content.js']  # default scripts included
    )
]
content_questions = [
    inquirer.Text(
        'content_url',
        message="Enter the URL which the content script will run on (wildcards allowed, separate with commas)",
    )
]


class ChromeExtensionCli(cmd.Cmd):
    prompt = "chromy >> "
    intro = f"""

        {Fore.CYAN}[Chromy v{version}] {Fore.RESET}
        {Fore.WHITE}Creating chrome extensions has never been easier.{Fore.RESET}
        {Fore.WHITE}Type 'init' to get started.{Fore.RESET}
        
        {Fore.WHITE}Type 'help' to see the list of available commands.{Fore.RESET}
    
    """
    _manager: PermissionManager

    def __init__(self) -> None:
        super().__init__()
        self.current_dir = os.getcwd()
        self._manager = PermissionManager()
        self._current_project = self.current_dir
        self._manager.initialize(self._current_project)

    # custom help command
    def do_help(self, line: str) -> None:
        """\n help - Show the list of available commands. \n"""
        print(f"\n[{Fore.CYAN}*{Fore.RESET}] Available commands:\n")
        print(f"[{Fore.CYAN}*{Fore.RESET}] init - Initialize a new Chrome extension project.")
        print(f"[{Fore.CYAN}*{Fore.RESET}] add <feature> - Add permission or locale to the manifest.json file.")
        print(f"[{Fore.CYAN}*{Fore.RESET}] current - Get the current project directory.")
        print(f"[{Fore.CYAN}*{Fore.RESET}] set <project> - Set the current project directory.")
        print(f"[{Fore.CYAN}*{Fore.RESET}] clear / cls - Clear the console.")
        print(f"[{Fore.CYAN}*{Fore.RESET}] quit / q - Exit the CLI.\n")
        return

    def do_init(self, line: str) -> None:
        """\n init - Initialize a new Chrome extension project. This includes creating all necessary files \n"""
        try:
            name = input("\nExtension name: ")
            description = input("Enter a description for your extension: ")
            author = input("Extension author (Optional): ") or ""

            self._current_project = name

            print()  # empty line

            answers = inquirer.prompt(init_questions, theme=CoolTheme(), raise_keyboard_interrupt=True)

            if 'content.js' in answers['scripts']:
                content_url = inquirer.prompt(content_questions, theme=CoolTheme(), raise_keyboard_interrupt=True)
                if content_url['content_url'] != '':
                    answers['content_url'] = content_url['content_url']

        except KeyboardInterrupt:
            print(f"\n\n[{Fore.CYAN}*{Fore.RESET}] Cancelling project creation...\n")
            return

        print(f"\nCreating extension {name}...")
        print(f'[{Fore.CYAN}*{Fore.RESET}] Initializing project...')

        # create directories
        try:
            os.makedirs(os.path.join(self.current_dir, name), exist_ok=True)
            os.makedirs(os.path.join(self.current_dir, f"{name}/icons"), exist_ok=True)
            os.makedirs(os.path.join(self.current_dir, f"{name}/assets"), exist_ok=True) if answers['assets'] else None
            os.makedirs(os.path.join(self.current_dir, f"{name}/popup"), exist_ok=True) if answers['popup'] else None
            os.makedirs(os.path.join(self.current_dir, f"{name}/options"), exist_ok=True) if answers[
                'options'] else None

            self._manager.initialize(os.path.join(self.current_dir, name))

        except PermissionError:
            print(f"[{Fore.RED}*{Fore.RESET}] No permission to create directory.")
            return

        print(f'[{Fore.CYAN}*{Fore.RESET}] Created directories.')

        try:
            # add default files
            if answers['popup']:
                with open(os.path.join(self.current_dir, f"{name}/popup/popup.html"), "w") as f:
                    f.write(POPUP_HTML.format(name, name, description))

                with open(os.path.join(self.current_dir, f"{name}/popup/popup.css"), "w") as f:
                    f.write(POPUP_CSS)

                if 'popup.js' in answers['scripts']:
                    with open(os.path.join(self.current_dir, f"{name}/popup/popup.js"), "w") as f:
                        f.write(POPUP_JS)

                print(f'[{Fore.CYAN}*{Fore.RESET}] Created popup files.')

        except Exception as e:
            print(f"[{Fore.RED}*{Fore.RESET}] Error creating popup files: {e}")
            return

        try:
            # add options files
            if answers['options']:
                with open(os.path.join(self.current_dir, f"{name}/options/options.html"), "w") as f:
                    f.write(OPTIONS_HTML.format(name, name))

                with open(os.path.join(self.current_dir, f"{name}/options/options.css"), "w") as f:
                    f.write(OPTIONS_CSS)

                if 'options.js' in answers['scripts']:
                    with open(os.path.join(self.current_dir, f"{name}/options/options.js"), "w") as f:
                        f.write(OPTIONS_JS)

                print(f'[{Fore.CYAN}*{Fore.RESET}] Created options files.')

        except Exception as e:
            print(f"[{Fore.RED}*{Fore.RESET}] Error creating options files: {e}")
            return

        try:
            # add js files
            if 'background.js' in answers['scripts']:
                with open(os.path.join(self.current_dir, f"{name}/background.js"), "w") as f:
                    f.write(BACKGROUND_JS)

            if 'content.js' in answers['scripts']:
                with open(os.path.join(self.current_dir, f"{name}/content.js"), "w") as f:
                    f.write(CONTENT_JS)

            print(f'[{Fore.CYAN}*{Fore.RESET}] Created javascript files.')

        except Exception as e:
            print(f"[{Fore.RED}*{Fore.RESET}] Error creating javascript files: {e}")
            return

        # create manifest.json
        manifest = {
            "manifest_version": 3,
            "name": name,
            "description": description,
            "author": author if author else "",
            "version": "0.1",
            "permissions": [],
            "background": {

            },
            "action": {
                "default_icon": "icons/icon.png",
                "default_title": name
            },
            "icons": {
                "16": "icons/icon.png",
                "32": "icons/icon.png",
                "64": "icons/icon.png"
            },
            "web_accessible_resources": [{
                "resources": ["icons/*", "assets/*", "_locales/*"],
                "matches": ["<all_urls>"]
            }]
        }

        # add necessary manifest fields
        if answers['options']:
            manifest["options_page"] = "options/options.html"

        if 'background.js' in answers['scripts']:
            manifest["background"] = {
                "service_worker": "background.js"
            }

        if 'content.js' in answers['scripts']:
            manifest["content_scripts"] = [{
                "matches": [answers['content_url'].split(",")] if 'content_url' in answers else ["<all_urls>"],
                "js": ["content.js"]
            }]

        if answers['popup']:
            manifest["action"]["default_popup"] = "popup/popup.html"

        try:
            with open(os.path.join(self.current_dir, f"{name}/manifest.json"), "w") as f:
                json.dump(manifest, f, indent=4)

            print(f'[{Fore.CYAN}*{Fore.RESET}] Created manifest.json.')

        except Exception as e:
            print(f"[{Fore.RED}*{Fore.RESET}] Error creating manifest.json: {e}")
            return

        try:
            self.do_set(name)
            self._manager.initialize(os.path.join(self.current_dir, name))
        except Exception as e:
            pass

        print(f'\nSuccessfully created {name} extension.')
        print(f'Run `cd {name}` to enter the extension directory.')
        print(f'Run `chromy add` to add permissions to the manifest.json file.\n')

        return


    # add permission or feature
    def do_add(self, line: str):
        """\n add - Add permission to the manifest.json file. \n"""

        if self._current_project == "":
            print(f"[{Fore.RED}*{Fore.RESET}] No project directory set. Use `set <project>` to set the project.")
            return

        feature = line.split(" ")[0]

        # Add permission, icons, action, background script, content script, options page, theme color, display, orientation etc.
        action = [
            'activetab',
            'alarms',
            'background',
            'bookmarks',
            'browsersettings',
            'browsingdata',
            'captiveportal',
            'clipboardread',
            'clipboardwrite',
            'contentsettings',
            'contextmenus',
            'contextualidentities',
            'cookies',
            'debugger',
            'declarativenetrequest',
            'declarativenetrequestfeedback',
            'declarativenetrequestwithhostaccess',
            'devtools',
            'dns',
            'downloads',
            'downloads.open',
            'find',
            'geolocation',
            'history',
            'identity',
            'idle',
            'management',
            'menus',
            'menus.overridecontext',
            'nativemessaging',
            'notifications',
            'pagecapture',
            'pkcs11',
            'privacy',
            'proxy',
            'scripting',
            'search',
            'sessions',
            'storage',
            'tabhide',
            'tabs',
            'theme',
            'topsites',
            'unlimitedstorage',
            'userscripts',
            'webnavigation',
            'webrequest',
            'webrequestauthprovider',
            'webrequestblocking',
            'webrequestfilterresponse',
            'webrequestfilterresponse.serviceworkerscript',
            'locales',
            'language'
        ]

        print()

        # check if feature exists
        if feature.lower() not in action:
            print(f"[{Fore.RED}*{Fore.RESET}] Invalid feature.")
            print(f"[{Fore.RED}*{Fore.RESET}] Available features: {', '.join(action)}\n")
            return

        if not feature.lower() in ['locales', 'language', 'lang']:
            try:
                self._manager.add_permission(feature)
            except PermissionError:
                confirm = inquirer.confirm(
                    message=f"Permission {feature} already exists. Do you want to remove it?",
                )
                if confirm:
                    self._manager.remove_permission(feature)
                    print(f"[{Fore.GREEN}*{Fore.RESET}] Removed permission {feature}.")
                    return

            print(f"[{Fore.GREEN}*{Fore.RESET}] Added permission {feature}.\n")
            return

        elif feature.lower() == 'locales':
            try:
                if len(line.split(" ")) >= 2:
                    self._manager.enable_locales(line.split(" ")[1])
                else:
                    self._manager.enable_locales()

            except PermissionError as e:
                print(f"[{Fore.RED}*{Fore.RESET}] Error creating locales directory.")
                return

            except FileNotFoundError as e:
                pass

            print(f"[{Fore.GREEN}*{Fore.RESET}] Enabled locales.\n")
            return

        elif feature.lower() == 'language' or feature.lower() == 'lang':
            if os.path.exists(os.path.join(self.current_dir, "_locales")):
                try:
                    self._manager.add_language(line.split(" ")[1])

                except PermissionError:
                    print(f"[{Fore.RED}*{Fore.RESET}] Error creating language directory.")
                    return

                print(f"[{Fore.GREEN}*{Fore.RESET}] Added language {line.split(' ')[1]}.\n")

            else:
                print(f"\n[{Fore.RED}*{Fore.RESET}] No locales directory found. Use `add locales` to create it.")
                return

    # get current project
    def do_current(self, line: str):
        """\n current - Get the current project directory. \n"""
        if self._current_project != "":
            print(f"\n[{Fore.GREEN}*{Fore.RESET}] Current project: {self._current_project}\n")
            return

        print(f"\n[{Fore.RED}*{Fore.RESET}] No project directory set. Use `set <project>` to set the project.\n")
        return

    # set project
    def do_set(self, line: str) -> None:
        """\n set - Set the current project directory. \n"""
        if os.path.exists(line):
            self._current_project = line
            self._manager.initialize(os.path.join(self.current_dir, line))
            print(f"\n[{Fore.GREEN}*{Fore.RESET}] Set current project to {line}.\n")
            return

        print(f"\n[{Fore.RED}*{Fore.RESET}] Project {line} does not exist.\n")
        return

    # clear console commands
    def do_clear(self, line: str) -> None:
        """\n clear - Clear the console, equal to `cls` or `clear` os command. \n"""
        os.system('cls' if os.name == 'nt' else 'clear')
        return

    def do_cls(self, line: str) -> None:
        """\n cls - Alias for clear. \n"""
        os.system('cls' if os.name == 'nt' else 'clear')

    # quit commands
    def do_quit(self, line: str) -> None:
        """\n quit - Exit the CLI. \n"""
        print(f"[{Fore.CYAN}*{Fore.RESET}] Exiting Chromy CLI...")
        exit(0)

    def do_q(self, line: str) -> None:
        """\n q - Alias for quit. \n"""
        self.do_quit(line)

    def cmdloop(self, intro: str = None) -> None:
        """ Command Loop to handle user input."""
        while True:
            try:
                super().cmdloop(self.intro)
                break
            except KeyboardInterrupt:
                print(f"\n[{Fore.CYAN}*{Fore.RESET}] Exiting Chromy CLI...\n")
                return

    def postloop(self) -> None:
        """\n postloop - Called after the command loop exits. \n"""
        print(f"\n[{Fore.CYAN}*{Fore.RESET}] Exiting Chromy CLI...\n")
        return


# Main function to run the CLI
def main():
    shell = ChromeExtensionCli()
    if len(sys.argv) > 1:
        command = ' '.join(sys.argv[1:])
        shell.onecmd(command)
    else:
        shell.cmdloop()