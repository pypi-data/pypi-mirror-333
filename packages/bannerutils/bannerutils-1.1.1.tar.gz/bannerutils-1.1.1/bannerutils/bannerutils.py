import os
import subprocess
import pyfiglet
import pyperclip

class BannerUtils:
    def __init__(self):
        """Initialize BannerUtils and ensure required packages are installed."""
        self._install_dependencies()
    
    def _install_dependencies(self):
        """Ensure required dependencies are installed."""
        required_packages = ["pyfiglet", "pyperclip"]
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                print(f"[*] Installing missing package: {package}...")
                subprocess.run(["pip", "install", package], check=True)

    def list_fonts(self):
        """List all available fonts from pyfiglet."""
        print("\nAvailable Fonts:\n")
        for font in sorted(pyfiglet.getFonts()):
            print(font)
        print("\nFor a full list, use: python -m pyfiglet -l\n")

    def generate_banner(self, text, font="standard", align="left"):
        """Generate an ASCII banner with the specified font and alignment."""
        try:
            banner = pyfiglet.figlet_format(text, font=font)
        except pyfiglet.FontNotFound:
            print(f"[!] Font '{font}' not found! Using 'standard' font instead.")
            banner = pyfiglet.figlet_format(text, font="standard")

        # Calculate width for alignment
        width = max(len(line) for line in banner.split("\n"))  
        if align == "center":
            lines = [line.center(width) for line in banner.split("\n")]
            banner = "\n".join(lines)
        elif align == "right":
            lines = [line.rjust(width) for line in banner.split("\n")]
            banner = "\n".join(lines)

        return banner

    def copy_to_clipboard(self, text):
        """Copy text to clipboard if possible."""
        try:
            pyperclip.copy(text)
            print("\n[*] Banner copied to clipboard!")
        except pyperclip.PyperclipException:
            print("\n[!] Copying failed. Ensure 'xclip' or 'xsel' is installed (Linux users).")

# Command-line interface (CLI) execution
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Advanced ASCII Banner Generator",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("text", type=str, help="The text to convert into an ASCII banner.")
    parser.add_argument("-f", "--font", type=str, default="standard", help="Font name (default: standard). Use -fh to list available fonts.")
    parser.add_argument("-fh", "--fonthelp", action="store_true", help="List available fonts.")
    parser.add_argument("-a", "--align", type=str, choices=["left", "center", "right"], default="left", help="Text alignment: left, center, or right.")

    args = parser.parse_args()
    banner_util = BannerUtils()

    if args.fonthelp:
        banner_util.list_fonts()
    else:
        os.system("cls" if os.name == "nt" else "clear")
        print("\n")
        banner = banner_util.generate_banner(args.text, args.font, args.align)
        print(banner)

        copy_choice = input("\n[*] Copy banner to clipboard? (y/n): ").strip().lower()
        if copy_choice == "y":
            banner_util.copy_to_clipboard(banner)
