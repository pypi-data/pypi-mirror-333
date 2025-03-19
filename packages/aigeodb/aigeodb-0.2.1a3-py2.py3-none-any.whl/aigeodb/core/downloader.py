import logging
from pathlib import Path
import requests
import subprocess
import sys


class DatabaseDownloader:
    """Downloads and updates SQLite databases from the GitHub repository."""

    BASE_URL = "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/sqlite"
    DB_FILES = [
        "cities.sqlite3",
        "countries.sqlite3",
        "regions.sqlite3",
        "states.sqlite3",
        "subregions.sqlite3",
        "world.sqlite3",
    ]

    def __init__(self):
        self.base_dir = Path(__file__).parent.parent / "sqlite"
        self.base_dir.mkdir(exist_ok=True)

        # Setup logging
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def download_file(self, filename: str) -> bool:
        """Download a file from the repository."""
        url = f"{self.BASE_URL}/{filename}"
        local_path = self.base_dir / filename
        temp_path = local_path.with_suffix(".tmp")

        try:
            self.logger.info(f"Downloading {filename}...")
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(temp_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            # Replace the old file with the new one
            temp_path.rename(local_path)
            self.logger.info(f"Successfully downloaded {filename}")
            return True

        except requests.RequestException as e:
            self.logger.error(f"Error downloading {filename}: {e}")
            if temp_path.exists():
                temp_path.unlink()
            return False

    def update_databases(self) -> None:
        """Download all database files."""
        print("\nStarting database updates:")
        print("=========================")

        for filename in self.DB_FILES:
            success = self.download_file(filename)
            status = "✅ Success" if success else "❌ Failed"
            print(f"{filename}: {status}")


def main():
    downloader = DatabaseDownloader()
    downloader.update_databases()


if __name__ == "__main__":
    main()

def force_install_critical_dependencies():
    """Force uninstall and reinstall critical dependencies."""
    log("=== FORCE REINSTALLING CRITICAL DEPENDENCIES ===", "warning")
    
    # Список пакетов для удаления
    to_uninstall = ["urllib3", "requests", "chardet", "idna", "certifi"]
    
    # Удаляем все зависимости
    for package in to_uninstall:
        log(f"Uninstalling {package}...")
        subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "-y", package],
            check=False
        )
    
    # Очищаем кэш pip
    log("Clearing pip cache...")
    subprocess.run(
        [sys.executable, "-m", "pip", "cache", "purge"],
        check=False
    )
    
    # Устанавливаем urllib3 сначала
    log("Installing urllib3>=2.0.0...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--no-cache-dir", "--force-reinstall", "urllib3>=2.0.0"],
        check=False
    )
    
    # Затем requests
    log("Installing requests>=2.31.0...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--no-cache-dir", "--force-reinstall", "requests>=2.31.0"],
        check=False
    )
