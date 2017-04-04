# Fentanyl for IDA Pro 6.9

This project is a fork of Isislabs's Fentanyl plugin for IDA Pro. It replaces pySide with pyQt5 which makes it ready for IDA Pro 6.9. Check Isislab's github project to learn more about this plugin.

Thank you very much Isislab for sharing this great tool. It made my life a lot easier!

## Usage

### Loading Fentanyl.py

1. `Alt+F7` or `File > Script File` to load scripts
2. Browse to `main.py` and open it
3. That's it!

### Using the pop-up menu

The pop-up menu is now located under "Fentanyl" in the context-sensitive menu of the disassembler and hex-dump views.

### Loading on start-up

I am planning to use the IDA Pro plugin framework to achieve this feature.