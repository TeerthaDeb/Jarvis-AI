import winreg

def get_installed_applications():
    """Retrieve a list of installed applications on Windows."""
    installed_applications = []
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall") as key:
        for i in range(winreg.QueryInfoKey(key)[0]):
            try:
                subkey_name = winreg.EnumKey(key, i)
                with winreg.OpenKey(key, subkey_name) as subkey:
                    app_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    installed_applications.append(app_name)
            except WindowsError:
                pass  # Some subkeys may not have the DisplayName value
    return installed_applications

# Example usage
installed_apps = get_installed_applications()
print("Installed applications:")
for app in installed_apps:
    print(app)
