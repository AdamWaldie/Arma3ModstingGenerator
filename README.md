This script allows arma 3 preset exports from the launcher to be turned into ID strings for workshop downloads. if you set up your server to save the mod folder as the workshop ID of the mod, you can also use this tool to generate a mod load order comptabale with that setup for quick, repeatable access. This stops the random folder rename bullshit commonly associated with A3 modding.

Ive also Added an example bat for how you might handle downloading workshop items and saving them under their own IDs in your mod folder.

# Arma 3 Mod ID Extractor

A tool for extracting and sanitizing Arma 3 mod IDs and names from preset `.html` files. This tool ensures compatibility by sanitizing mod names and provides various output options for easy use. 

I provide a downloadable Python version, as well as a web app version for ease of use.

## Features
- Extract mod IDs and display names from Arma 3 preset files.
- Sanitize mod names for compatibility with file systems.
- Highlight mods that required sanitization so that you can validate any which may have or need sanitation to work in your command line.
- Toggle between mod names or IDs in the output.
- Save the extracted list in various formats (newline, semicolon, or comma-separated).

## Usage
1. **Load File**: Click "Load .html File" and select your Arma 3 preset file.
2. **Configurable Options**:
   - Choice to include `@` prefix for entries.
   - Show mod names or IDs in the output.
   - Choose the desired output format (newline, semicolon, or comma-separated).
3. **View Results**:
   - Extracted data will appear in the "Extracted Output" section.
   - Any sanitized mods will be listed in the "Sanitized Mods" section.
4. **Save List**: Click "Save List" to download the output as a text file.

## Live Web App
[Try the tool here!](https://adamwaldie.github.io/Arma3ModstingGenerator/Arma3ModstingGeneratorWebApp)

## Screenshots
### Python Interface
![Python Interface](https://raw.githubusercontent.com/AdamWaldie/Arma3ModstingGenerator/refs/heads/main/coverimage.png)

### Web App Interface
![Web App Interface](https://raw.githubusercontent.com/AdamWaldie/Arma3ModstingGenerator/refs/heads/main/coverimage2.png)

## Credits
Developed by Waldo.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
