import subprocess
import sys
import os

class DockerHelper:
    @staticmethod
    def check_docker():
        """Check if Docker is installed."""
        try:
            subprocess.run(['docker', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Docker is installed!")
            return True
        except subprocess.CalledProcessError:
            print("Docker is not installed.")
            return False

    @staticmethod
    def start_docker_engine():
        """Start Docker engine based on OS."""
        if sys.platform.startswith('linux'):
            subprocess.run(['sudo', 'systemctl', 'start', 'docker'], check=True)
            print("Docker engine started on Linux.")
        elif sys.platform.startswith('win'):
            subprocess.run(['sc', 'start', 'Docker'], check=True)
            print("Docker engine started on Windows.")
        else:
            print("Docker engine start not supported on this platform.")

    @staticmethod
    def install_docker():
        """Install Docker based on OS."""
        if sys.platform.startswith('linux'):
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'docker.io'], check=True)
            print("Docker installed on Linux!")
        elif sys.platform.startswith('win'):
            docker_installer_url = 'https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe'
            docker_installer_path = os.path.join(os.getenv('TEMP'), 'DockerDesktopInstaller.exe')

            subprocess.run(['curl', '-L', docker_installer_url, '-o', docker_installer_path], check=True)
            subprocess.run([docker_installer_path], check=True)
            print("Docker installed on Windows!")
        else:
            print("Docker installation not supported on this platform.")
