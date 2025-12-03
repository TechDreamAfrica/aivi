"""
Desktop Application Control module for AIVI
Controls desktop applications like MS Word, PowerPoint, Calculator, Narrator, etc.
"""

import os
import subprocess
import platform
import time
import ctypes
import sys
from pathlib import Path

class DesktopController:
    def __init__(self):
        self.system = platform.system()
        self.apps = self._get_app_paths()

    def _is_admin(self):
        """Check if the current process is running with administrator privileges"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def _run_as_admin(self, command, params=""):
        """Run a command with administrator privileges using UAC"""
        try:
            if self.system != "Windows":
                return False, "UAC elevation only available on Windows"

            # Use ShellExecute with 'runas' verb to trigger UAC
            result = ctypes.windll.shell32.ShellExecuteW(
                None, "runas", command, params, None, 1
            )
            # ShellExecute returns > 32 on success
            return result > 32, f"Elevation result: {result}"
        except Exception as e:
            return False, f"UAC elevation failed: {str(e)}"

    def _handle_elevation_error(self, app_name, original_error):
        """Handle elevation errors with fallback methods"""
        error_msg = str(original_error).lower()

        # Check if it's an elevation error (1740 or related)
        if "1740" in error_msg or "elevation" in error_msg or "administrator" in error_msg:
            # Try alternative launch methods
            fallback_methods = self._get_fallback_methods(app_name)

            for method_name, method in fallback_methods:
                try:
                    success, message = method()
                    if success:
                        return True, f"Successfully launched {app_name} using {method_name}"
                except Exception:
                    continue

            # If all fallbacks fail, suggest UAC elevation
            return False, f"Error 1740: {app_name} requires administrator privileges. Please run AIVI as administrator or manually launch {app_name}."

        return False, f"Failed to launch {app_name}: {original_error}"

    def _get_fallback_methods(self, app_name):
        """Get fallback methods for launching applications"""
        fallback_methods = []
        app_name = app_name.lower()

        if app_name == "narrator":
            fallback_methods = [
                ("Windows Settings", lambda: self._launch_via_settings("ms-settings:easeofaccess-narrator")),
                ("Control Panel", lambda: self._launch_via_control_panel("narrator")),
                ("PowerShell", lambda: self._launch_via_powershell("Start-Process Narrator")),
            ]
        elif app_name == "onscreen_keyboard":
            fallback_methods = [
                ("Windows Settings", lambda: self._launch_via_settings("ms-settings:easeofaccess-keyboard")),
                ("Control Panel", lambda: self._launch_via_control_panel("osk")),
                ("PowerShell", lambda: self._launch_via_powershell("Start-Process osk")),
            ]
        elif app_name == "voice_recorder":
            fallback_methods = [
                ("PowerShell", lambda: self._launch_via_powershell("Get-AppxPackage *SoundRecorder* | Invoke-Item")),
                ("Direct Store", lambda: (True, self._open_store_app("9WZDNCRFHWKN"))),
            ]
        elif app_name == "camera":
            fallback_methods = [
                ("PowerShell", lambda: self._launch_via_powershell("Get-AppxPackage *Camera* | Invoke-Item")),
                ("Direct Store", lambda: (True, self._open_store_app("9WZDNCRFJBBG"))),
            ]

        return fallback_methods

    def _launch_via_settings(self, settings_uri):
        """Launch application via Windows Settings app"""
        try:
            os.system(f'start ms-settings: && start {settings_uri}')
            return True, f"Opened settings: {settings_uri}"
        except Exception as e:
            return False, f"Settings launch failed: {str(e)}"

    def _launch_via_control_panel(self, app_name):
        """Launch application via Control Panel"""
        try:
            if app_name == "narrator":
                os.system('start control /name Microsoft.EaseOfAccessCenter')
            elif app_name == "osk":
                os.system('start control /name Microsoft.EaseOfAccessCenter')
            return True, f"Opened Ease of Access Center for {app_name}"
        except Exception as e:
            return False, f"Control Panel launch failed: {str(e)}"

    def _launch_via_powershell(self, command):
        """Launch application via PowerShell"""
        try:
            ps_command = f'powershell.exe -Command "{command}"'
            subprocess.Popen(ps_command, shell=True)
            return True, f"Launched via PowerShell: {command}"
        except Exception as e:
            return False, f"PowerShell launch failed: {str(e)}"

    def _open_store_app(self, product_id):
        """Open Windows Store app by product ID"""
        try:
            store_url = f"ms-windows-store://pdp/?productid={product_id}"
            os.system(f'start "{store_url}"')
            return f"Opened Windows Store app: {product_id}"
        except Exception as e:
            return f"Store app launch failed: {str(e)}"
    
    def _get_app_paths(self):
        """Get paths to common Windows applications"""
        if self.system != "Windows":
            return {}
        
        apps = {
            # Microsoft Office
            'word': [
                r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
                r"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE",
                r"C:\Program Files\Microsoft Office\Office16\WINWORD.EXE",
                r"C:\Program Files (x86)\Microsoft Office\Office16\WINWORD.EXE"
            ],
            'powerpoint': [
                r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
                r"C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE",
                r"C:\Program Files\Microsoft Office\Office16\POWERPNT.EXE",
                r"C:\Program Files (x86)\Microsoft Office\Office16\POWERPNT.EXE"
            ],
            'excel': [
                r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
                r"C:\Program Files (x86)\Microsoft Office\root\Office16\EXCEL.EXE",
                r"C:\Program Files\Microsoft Office\Office16\EXCEL.EXE",
                r"C:\Program Files (x86)\Microsoft Office\Office16\EXCEL.EXE"
            ],
            'onenote': [
                r"C:\Program Files\Microsoft Office\root\Office16\ONENOTE.EXE",
                r"C:\Program Files (x86)\Microsoft Office\root\Office16\ONENOTE.EXE"
            ],
            
            # Windows Built-in Applications
            'calculator': [r"C:\Windows\System32\calc.exe"],
            'notepad': [r"C:\Windows\System32\notepad.exe"],
            'wordpad': [r"C:\Program Files\Windows NT\Accessories\wordpad.exe"],
            'narrator': [r"C:\Windows\System32\Narrator.exe"],
            'magnifier': [r"C:\Windows\System32\Magnify.exe"],
            'onscreen_keyboard': [r"C:\Windows\System32\osk.exe"],
            'voice_recorder': ["ms-windows-store://pdp/?productid=9WZDNCRFHWKN"],
            'camera': ["ms-windows-store://pdp/?productid=9WZDNCRFJBBG"],
            
            # Windows Accessibility
            'speech_recognition': [r"C:\Windows\Speech\Common\sapisvr.exe"],
            'ease_of_access': [r"C:\Windows\System32\utilman.exe"],
            
            # System Tools
            'control_panel': [r"C:\Windows\System32\control.exe"],
            'device_manager': [r"C:\Windows\System32\devmgmt.msc"],
            'task_manager': [r"C:\Windows\System32\taskmgr.exe"],
            'system_settings': ["ms-settings:"],
            'file_explorer': [r"C:\Windows\explorer.exe"],
            
            # Browsers
            'chrome': [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ],
            'firefox': [
                r"C:\Program Files\Mozilla Firefox\firefox.exe",
                r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
            ],
            'edge': [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"],
            
            # Media Players
            'media_player': [r"C:\Program Files\Windows Media Player\wmplayer.exe"],
            'vlc': [
                r"C:\Program Files\VideoLAN\VLC\vlc.exe",
                r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
            ],
            
            # Text Editors
            'vscode': [
                r"C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe".format(os.getenv('USERNAME', '')),
                r"C:\Program Files\Microsoft VS Code\Code.exe"
            ],
            'notepadpp': [
                r"C:\Program Files\Notepad++\notepad++.exe",
                r"C:\Program Files (x86)\Notepad++\notepad++.exe"
            ]
        }
        
        return apps
    
    def find_app_executable(self, app_name):
        """Find the executable path for an application"""
        app_name = app_name.lower().replace(' ', '_').replace('-', '_')
        
        if app_name not in self.apps:
            return None
        
        for path in self.apps[app_name]:
            if path.startswith('ms-'):
                return path  # Windows Store app
            if os.path.exists(path):
                return path
        
        return None
    
    def open_application(self, app_name):
        """Open a desktop application with enhanced error handling"""
        try:
            app_path = self.find_app_executable(app_name)
            if not app_path:
                return False, f"Application '{app_name}' not found on this system."

            # First, try normal launch
            try:
                if app_path.startswith('ms-'):
                    # Windows Store app
                    os.system(f'start "{app_path}"')
                else:
                    # Regular executable - try normal launch first
                    subprocess.Popen([app_path], shell=False)

                return True, f"Successfully opened {app_name}"

            except (OSError, subprocess.SubprocessError, PermissionError) as launch_error:
                # Check if it's an elevation error and handle accordingly
                return self._handle_elevation_error(app_name, launch_error)

        except Exception as e:
            # General error handling
            error_code = getattr(e, 'winerror', None)
            if error_code == 1740:  # ERROR_ELEVATION_REQUIRED
                return self._handle_elevation_error(app_name, e)
            return False, f"Failed to open {app_name}: {str(e)}"
    
    def open_website(self, url):
        """Open a website in the default browser"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            if self.system == "Windows":
                os.system(f'start "{url}"')
            elif self.system == "Darwin":  # macOS
                os.system(f'open "{url}"')
            else:  # Linux
                os.system(f'xdg-open "{url}"')
            
            return True, f"Opened {url} in browser"
            
        except Exception as e:
            return False, f"Failed to open website: {str(e)}"
    
    def open_file_location(self, path=None):
        """Open file explorer at a specific location"""
        try:
            if not path:
                path = os.path.expanduser("~")  # Home directory
            
            if self.system == "Windows":
                os.system(f'explorer "{path}"')
            elif self.system == "Darwin":  # macOS
                os.system(f'open "{path}"')
            else:  # Linux
                os.system(f'xdg-open "{path}"')
            
            return True, f"Opened file explorer at {path}"
            
        except Exception as e:
            return False, f"Failed to open file explorer: {str(e)}"
    
    def enable_accessibility_features(self, feature):
        """Enable Windows accessibility features with enhanced error handling"""
        try:
            feature = feature.lower()

            if feature in ['narrator', 'screen_reader']:
                try:
                    subprocess.Popen([r"C:\Windows\System32\Narrator.exe"])
                    return True, "Narrator started"
                except (OSError, subprocess.SubprocessError, PermissionError) as e:
                    return self._handle_elevation_error("narrator", e)

            elif feature in ['magnifier', 'zoom', 'magnify']:
                try:
                    subprocess.Popen([r"C:\Windows\System32\Magnify.exe"])
                    return True, "Magnifier started"
                except (OSError, subprocess.SubprocessError, PermissionError) as e:
                    return self._handle_elevation_error("magnifier", e)

            elif feature in ['on_screen_keyboard', 'virtual_keyboard', 'osk']:
                try:
                    subprocess.Popen([r"C:\Windows\System32\osk.exe"])
                    return True, "On-Screen Keyboard started"
                except (OSError, subprocess.SubprocessError, PermissionError) as e:
                    return self._handle_elevation_error("onscreen_keyboard", e)

            elif feature in ['high_contrast']:
                try:
                    # Toggle high contrast mode
                    os.system('reg add "HKCU\\Control Panel\\Accessibility\\HighContrast" /v "Flags" /t REG_SZ /d "126" /f')
                    return True, "High contrast mode enabled"
                except Exception as e:
                    # Registry changes might need elevation
                    if "1740" in str(e) or "access" in str(e).lower():
                        return False, "High contrast requires administrator privileges. Please run AIVI as administrator or enable manually in Settings."
                    raise

            else:
                return False, f"Unknown accessibility feature: {feature}"

        except Exception as e:
            error_code = getattr(e, 'winerror', None)
            if error_code == 1740:
                return self._handle_elevation_error(feature, e)
            return False, f"Failed to enable {feature}: {str(e)}"
    
    def get_available_apps(self):
        """Get list of available applications on this system"""
        available = {}
        for app_name, paths in self.apps.items():
            app_path = self.find_app_executable(app_name)
            if app_path:
                available[app_name] = app_path
        
        return available

# Global desktop controller instance
desktop_controller = DesktopController()

def open_app(app_name):
    """Open a desktop application by name"""
    return desktop_controller.open_application(app_name)

def open_website(url):
    """Open a website"""
    return desktop_controller.open_website(url)

def open_file_explorer(path=None):
    """Open file explorer"""
    return desktop_controller.open_file_location(path)

def enable_accessibility(feature):
    """Enable accessibility feature"""
    return desktop_controller.enable_accessibility_features(feature)

def get_available_applications():
    """Get list of available applications"""
    return desktop_controller.get_available_apps()

def check_admin_status():
    """Check if AIVI is running with administrator privileges"""
    return desktop_controller._is_admin()

def get_elevation_help():
    """Get help text for elevation issues"""
    is_admin = check_admin_status()

    if is_admin:
        return "✅ AIVI is running with administrator privileges."
    else:
        return """❌ AIVI is not running with administrator privileges.

Some system applications (Narrator, On-Screen Keyboard, Voice Recorder, Camera) may require administrator rights.

To fix elevation errors:
1. Right-click on AIVI and select "Run as administrator"
2. Or use the fallback methods provided when applications fail to launch
3. Or manually enable these features through Windows Settings > Ease of Access

Note: AIVI will try alternative launch methods automatically if elevation is needed."""

def quick_shortcuts():
    """Provide quick access to common shortcuts"""
    shortcuts = {
        'documents': lambda: desktop_controller.open_file_location(os.path.expanduser("~/Documents")),
        'downloads': lambda: desktop_controller.open_file_location(os.path.expanduser("~/Downloads")),
        'desktop': lambda: desktop_controller.open_file_location(os.path.expanduser("~/Desktop")),
        'pictures': lambda: desktop_controller.open_file_location(os.path.expanduser("~/Pictures")),
        'music': lambda: desktop_controller.open_file_location(os.path.expanduser("~/Music")),
        'videos': lambda: desktop_controller.open_file_location(os.path.expanduser("~/Videos")),
    }
    return shortcuts
