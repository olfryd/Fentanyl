"""
main.py

IDAPython script to patch binaries. 

IDAPython: https://code.google.com/p/idapython/
Helfpul if you want to run scripts on startup: https://code.google.com/p/idapython/source/browse/trunk/examples/idapythonrc.py

Alt F7 to load scripts

File > Produce file > Create DIF file
Edit > Patch program > Apply patches to input file

Keybindings:
    Shift-N: Convert instruction to nops
    Shift-X: Nop all xrefs to this function
    Shift-J: Invert conditional jump
    Shift-U: Make jump unconditional
    Shift-P: Patch instruction
    Shift-Z: Undo modification (Won't always work. Should still be careful editing.)
    Shift-Y: Redo modification (Won't always work. Should still be careful editing.)

"""

import os
import idaapi
import idc
import re
from Hooks import Hooks
from Handler import Handler
import Fentanyl
import AssembleForm
import CodeCaveFinder
import Util
import Neuter

""" Main """

ftl_path = os.path.dirname(__file__)

ftl = Fentanyl.Fentanyl()
asf = AssembleForm.AssembleForm()
ftln = Neuter.Neuter(ftl)

#Interfaces to the methods in ftl
def nopout():
    start, end = Util.get_pos()
    ftl.nopout(start, end - start)

import traceback
def assemble():
    try: assemble_()
    except e:
        print traceback.format_exc()

def assemble_():
    success = False
    while not success:
        v = asf.process()
        if not v or not v['inp'].strip(): return

        start, end = Util.get_pos()
        lines = [i.strip() for i in v['inp'].replace(';', '\n').strip().split('\n')]
        success, data = ftl.assemble(start, lines, v['opt_chk']['fixup'], v['opt_chk']['nopout'])

        if not success:
            print data

def togglejump():
    start, end = Util.get_pos()
    ftl.togglejump(start)

def uncondjump():
    start, end = Util.get_pos()
    ftl.uncondjump(start)

def nopxrefs():
    start, end = Util.get_pos()
    func = idaapi.get_func(start)
    if func:
        ftl.nopxrefs(func.startEA)

def undo():
    if ftl.undo() is None:
        print "Nothing to undo"

def redo():
    if ftl.redo() is None:
        print "Nothing to redo"

def savefile():
    output_file = AskFile(1, "*", "Output File")
    if not output_file:
        return
    Util.save_file(output_file)

#Interface to spelunky
def openspelunky():
    window = CodeCaveFinder.CodeCaveWindow()
    window.Show("Spelunky")

def neuter():
    ftl.neuter()

#Hotkey definitions
hotkeys = [
    ('my:nopout', 'Replace with nops', True , 'Alt+N', 'nopout.png', nopout),
    ('my:nopxrefs', 'Nops all Xrefs'   , True , 'Alt+X', 'nopxrefs.png', nopxrefs),
    ('my:assemble', 'Assemble'         , True , 'Alt+P', 'assemble.png', assemble),
    ('my:togglejmp', 'Toggle jump'      , True , 'Alt+J', 'togglejump.png', togglejump),
    ('my:forcejmp', 'Force jump'       , True , 'Ctrl+Alt+F', 'uncondjump.png', uncondjump),
    ('my:undo', 'Undo Patch'       , False, 'Alt+Z', None, undo),
    ('my:redo', 'Redo Patch'       , False, 'Alt+Y', None, redo),
    ('my:save', 'Save File'        , False, 'Alt+S', None, savefile),
    ('my:codecave', 'Find Code Caves'  , False, 'Alt+C', None, openspelunky),
    ('my:neuter', 'Neuter Binary'    , False, 'Ctrl+Alt+N', None, neuter)
]

menu_entries = []

# Register actions and add to context menus
for act_id, text , in_menu, keys, icon, func in hotkeys:
    handler = Handler(func)

    # load custom icon
    icon_id = -1 # default for no icon
    if icon is not None:
        icon_id = idaapi.load_custom_icon(os.path.join(ftl_path, 'icons', icon))

    action_desc = idaapi.action_desc_t(
        act_id,   # The action name. This acts like an ID and must be unique
        text,  # The action text.
        handler,   # The action handler.
        keys,      # Optional: the action shortcut
        None,  # Optional: the action tooltip (available in menus/toolbar)
        icon_id)           # Optional: the action icon (shows when in menus/toolbars)

    # Register the action
    idaapi.register_action(action_desc)

    # attach to menus
    if in_menu:
        menu_entries.append(act_id)

hooks = Hooks(menu_entries)
hooks.hook()
