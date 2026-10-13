---
name: winedt-setup
description: Install, restore, or verify Lance's WinEdt 10-and-above custom setup, including menu commands, templates, dictionary, formatting, and PowerToys document switching. Use for this WinEdt setup, not ordinary LaTeX editing.
---

# WinEdt Setup

Reproduce the setup successfully applied to WinEdt 11.2 on October 13, 2026. The source of truth is chapter 2, **WinEdt v10 and Above**, in `C:\Custom Program Files\WinEdt\Installation Notes\WinEdt Installation Notes.pdf`. Read that chapter when available; use the recipe below and bundled assets when restoring the recorded setup. Report material differences if the notes have changed.

## Locate and preserve

- Customization repository: `C:\Custom Program Files\WinEdt`.
- Installed application on the original machine: `C:\Program Files\WinEdt Team\WinEdt 11`.
- Original user profile: `C:\Users\lance.endres.CNPCUSA\AppData\Roaming\WinEdt Team\WinEdt 11`.
- Shared user dictionary: `C:\Custom Program Files\WinEdt\Dictionary\User.dic`.

Discover the actual installation, version, user profile, and existing PowerToys configuration on the target machine; do not assume the original username. In WinEdt, `%B` denotes the installation folder and `%b` the user folder. If WinEdt is already installed, configure it rather than reinstalling it. If the application itself is missing, obtain the installer from the official WinEdt source using the currently supported installation method.

Before changing files, create a timestamped backup of existing user overrides, templates, WinEdt settings (`WinEdt.dnt`), and any PowerToys files being modified. For each INI, use the user copy if present, otherwise copy the installed default into the user `ConfigEx` folder. Edit only the relevant sections, preserve unrelated settings and encoding, and make repeat runs idempotent. Do not replace full INIs with copies from another machine. Do not execute the custom build, cleanup, or image-conversion commands merely to verify installation.

## Apply the configuration

1. **MainMenu.ini**: Within `MENU="TeX_Menu"`, insert the menu items from [assets/MainMenu.ini](assets/MainMenu.ini) immediately after the complete `XeLaTeX` or `TeXify` item. Add only missing custom items. The repository's `src V10 and Above\MainMenu.ini`, when available, is the preferred current source. Use the real `TeXTeXify` image identifier in that asset, rather than the truncated identifier shown in the PDF code listing.

   Set these shortcuts in their existing item blocks:

   | Item | SHORTCUT value |
   | --- | --- |
   | Build_Tree | `120::F9` |
   | Compile (Tools menu) | `116::F5` |
   | Close | `16471::Ctrl+W` |
   | $Toggle_Wrap/NoWrap | `16499::Ctrl+F4` |

2. **Toolbar.ini**: Within `TOOLBAR="Toolbar_TeX"`, add `BUTTON="Save_All"` immediately after `BUTTON="Save"`. At the end of that toolbar, before its closing `END`, add a separator (`BUTTON="|"`) and buttons for `Make_Document`, `Clean_Temp_Files`, `Clean_All_Output`, and `Convert_All_Images`, in that order. Avoid duplicate buttons.

3. **Templates**: Copy `Figure.ltx`, `Eq.ltx`, and `Eql.ltx` into `%b\Templates\LaTeX`. Prefer the repository's `src V10 and Above\Templates`; fall back to [assets/Templates](assets/Templates). Preserve originals before overwriting. WinEdt resolves these user overrides ahead of installed templates.

4. **Preferences.ini**: Set `RUN_ONE_INSTANCE_ONLY=0`.
5. **Tabs.ini**: Set `TAB_ALLOW_KEYBOARD=1` (Options → Preferences → Tabs → Allow Keyboard Tabs).
6. **Dictionaries.ini** (Word Lists in Options Interface): In `DICTIONARY="User (Addon)"`, set `FILE` to the existing shared `Dictionary\User.dic` above. Confirm it exists; do not replace it or create an empty dictionary over it. If the repository has moved, use its actual path.
7. **Keywords.ini**: In the `LIST="END_LIST"` belonging to `KEYWORD_GROUP="BibTeX Fields"`, add missing lines: `assignee`, `day`, `filedday`, `filedmonth`, `filedyear`, `href`, `id`, `issuedday`, `issuedmonth`, `issuedyear`, `logline`, `pubday`, `pubmonth`, `pubyear`, `speid`, `websitename`. Add `WEBHREF` to the list for `KEYWORD_GROUP="BibTeX"`. Do not add these to similarly named groups.
8. **Paragraphs.ini**: In `[PARAGRAPHS]`, edit the block whose `PARAGRAPH` value is an actual tab character (not a space): `MODE_FILTER="*"`, `ALLOW_SOFT_WRAP=1`, `CASE_SENSITIVE=1`, `OFFSET=1`, `OFFSET_BY=4`. Preserve other paragraph blocks.

## PowerToys document switching

The desired mapping is **Ctrl+Tab → Shift+F2**, targeting only the WinEdt process. Shift+F2 already invokes `Toggle_Window` / `ActivateNextChild(1,1)` in the standard WinEdt menu. Preserve that binding.

- Reuse installed PowerToys. If missing, obtain the current official Microsoft release for the machine's architecture, preferably per user. Verify Microsoft's signature and the release hash when provided before installing. Do not pin the recorded version `0.101.2362.0`; it was simply the release installed during the original setup.
- Enable Keyboard Manager and ensure PowerToys runs in the background and starts at login. Preserve unrelated PowerToys configuration.
- Add an application-specific shortcut for `winedt.exe` through Keyboard Manager → Remap a shortcut. If using its configuration files instead, first inspect the installed version's schema and merge the row from [assets/PowerToys WinEdt Remapping.json](assets/PowerToys%20WinEdt%20Remapping.json), rather than overwriting existing remappings. This recorded profile uses virtual-key sequences `17;9` → `16;113` and `targetApp="winedt.exe"`. The original profile lives at `%LOCALAPPDATA%\Microsoft\PowerToys\Keyboard Manager\default.json`; select the actual active profile from the module's `settings.json`.
- Once the mapping is ready, in WinEdt `MainMenu.ini`, clear the **entire** `SHORTCUT` value in `ITEM="Next_MDI_Window"` to `SHORTCUT=""`. The default value was `16393::Ctrl+Tab`. Do not leave the numeric prefix behind. Preserve the other MDI shortcuts.
- When configuration files are edited externally, activate them using the application's supported reload mechanism; if restarting PowerToys, avoid interrupting unrelated work. Confirm Keyboard Manager's engine is running.

## Load and verify

Saving INIs alone does not activate them. Load each changed script in the Options Interface, or create a small WinEdt `.edt` macro with absolute paths:

```text
LoadConfig("<user profile>\ConfigEx\MainMenu.ini");
LoadConfig("<user profile>\ConfigEx\Toolbar.ini");
LoadConfig("<user profile>\ConfigEx\Preferences.ini");
LoadConfig("<user profile>\ConfigEx\Tabs.ini");
LoadConfig("<user profile>\ConfigEx\Dictionaries.ini");
LoadConfig("<user profile>\ConfigEx\Keywords.ini");
LoadConfig("<user profile>\ConfigEx\Paragraphs.ini");
SaveSettings;
```

Open the macro in WinEdt and invoke **Tools → Macros → Execute Current Macro**, normally Ctrl+Shift+F9. Main menu must load before toolbar. Inspect any error dialogs; do not claim success from file writes alone. For Windows UI automation, read the available computer-use skill and follow its app/window selection workflow. Explain visible actions before carrying them out so the user understands the work.

Verify the four TeX menu commands and new toolbar buttons are visible, Allow Keyboard Tabs is checked, all three templates match their intended sources, the dictionary path and INI changes are correct, and settings were saved. Create an empty temporary document alongside an existing saved document and verify Ctrl+Tab switches between them; close the empty test document without modifying user documents. PowerToys must remain running for the remapping to work.

The menu commands reference external batch files: `run_make_document.bat` in the document's project directory, plus `clean_temp_files.bat`, `clean_all_output.bat`, and `convert_all_images.bat` resolved by their configured working directories/PATH. Installing menu items does not supply these project tools. If the user asks to validate their operation, inspect availability separately and report missing dependencies without running cleanup commands.

Report what was applied, verification results, backup location, and any unfinished step. Preserve this workflow's scope: do not install unrelated repository files such as autocomplete macros unless the user requests them or updated notes require them.
