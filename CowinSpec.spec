# -*- mode: python -*-

block_cipher = None


a = Analysis(['C:\\Users\\mohanlal.prajapati\\OneDrive - Dana Incorporated\\Python\\Cowin\\Slot_By_Maharashtra_District.py'],
             pathex=['C:\\Python36\\Scripts'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
			 noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
		  a.binaries,
          a.zipfiles,
          a.datas,		  
		  [],          
          name='CowinApp_Pune',
          debug=False,
          strip=False,
		  runtime_tmpdir=None,
          upx=True,
          console=True)