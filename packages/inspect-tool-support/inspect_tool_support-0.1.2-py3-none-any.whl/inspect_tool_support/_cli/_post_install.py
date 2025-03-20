import subprocess


def post_install() -> None:
    _install_playwright()


def _install_playwright() -> None:
    subprocess.run(["playwright", "install", "--with-deps", "chromium"], check=True)
    print("Successfully ran 'playwright install'")
    subprocess.run(["playwright", "install-deps"], check=True)
    print("Successfully ran 'playwright install-deps'")
