from pathlib import Path
import re, shutil
base=Path(r'C:\Program Files\WinEdt Team\WinEdt 11')
user=Path(r'C:\Users\lance.endres.CNPCUSA\AppData\Roaming\WinEdt Team\WinEdt 11')
repo=Path(__file__).parent
names=['MainMenu','Toolbar','Preferences','Tabs','Dictionaries','Keywords','Paragraphs']
(user/'ConfigEx').mkdir(exist_ok=True)
backup=user/'Customization Backup 2026-10-13'
backup.mkdir(exist_ok=True)
def block(s,label,key,fn):
    pattern=rf'(?m)^([ \t]*){label}="{re.escape(key)}"[^\n]*\n.*?(?=^\1(?:{label}|END)=|\Z)'
    s,n=re.subn(pattern,lambda m:fn(m.group()),s,flags=re.S)
    assert n==1,(label,key,n)
    return s
for name in names:
    target=user/'ConfigEx'/f'{name}.ini'
    source=target if target.exists() else base/'ConfigEx'/f'{name}.ini'
    shutil.copy2(source,backup/f'{name}.ini')
    s=source.read_bytes().decode('utf-8-sig')
    if name=='MainMenu':
        if 'ITEM="Make_Document"' not in s:
            custom=(repo/'src V10 and Above'/'MainMenu.ini').read_text()
            s=block(s,'ITEM','XeLaTeX',lambda b:b+custom+'\n')
        for key,value in [('Build_Tree','120::F9'),('Compile','116::F5'),('Close','16471::Ctrl+W'),('$Toggle_Wrap/NoWrap','16499::Ctrl+F4')]:
            s=block(s,'ITEM',key,lambda b:re.sub(r'SHORTCUT="[^"]*"',f'SHORTCUT="{value}"',b))
    elif name=='Toolbar':
        s=block(s,'TOOLBAR','Toolbar_TeX',lambda b:b.replace('  BUTTON="Save"','  BUTTON="Save"\n  BUTTON="Save_All"')+'\n  BUTTON="|"\n'+''.join(f'  BUTTON="{k}"\n' for k in ['Make_Document','Clean_Temp_Files','Clean_All_Output','Convert_All_Images']))
    elif name=='Preferences': s=s.replace('RUN_ONE_INSTANCE_ONLY=1','RUN_ONE_INSTANCE_ONLY=0')
    elif name=='Tabs': s=s.replace('TAB_ALLOW_KEYBOARD=0','TAB_ALLOW_KEYBOARD=1')
    elif name=='Dictionaries':
        s=block(s,'DICTIONARY','User (Addon)',lambda b:b.replace('FILE="%b\\Dict\\User.dic"','FILE="C:\\Custom Program Files\\WinEdt\\Dictionary\\User.dic"'))
    elif name=='Keywords':
        for group,items in [('BibTeX',['WEBHREF']),('BibTeX Fields','assignee day filedday filedmonth filedyear href id issuedday issuedmonth issuedyear logline pubday pubmonth pubyear speid websitename'.split())]:
            s=block(s,'KEYWORD_GROUP',group,lambda b:b.replace('\nEND_LIST', '\n'+'\n'.join(x for x in items if not re.search(rf'(?m)^{x}$',b))+'\nEND_LIST'))
    elif name=='Paragraphs':
        s=block(s,'PARAGRAPH','\t',lambda b:b.replace('ALLOW_SOFT_WRAP=0','ALLOW_SOFT_WRAP=1').replace('OFFSET_BY=0','OFFSET_BY=4'))
    target.write_bytes(s.replace('\r\n','\n').replace('\n','\r\n').encode('utf-8-sig'))
templates=user/'Templates'/'LaTeX'
templates.mkdir(parents=True,exist_ok=True)
for source in (repo/'src V10 and Above'/'Templates').glob('*'):
    target=templates/source.name
    if target.exists(): shutil.copy2(target,backup/source.name)
    shutil.copy2(source,target)
macro=repo/'Load Customizations.edt'
macro.write_text('\n'.join(f'LoadConfig("{user}\\ConfigEx\\{n}.ini");' for n in names)+'\nSaveSettings;\n',encoding='utf-8')
print('Installed seven configuration files and three templates. Backup:',backup)
