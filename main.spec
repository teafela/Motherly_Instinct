# -*- mode: python -*-
a = Analysis(['C:\\Users\\Scott Todd\\Documents\\Dropbox\\GameJam-2012-Oct-27\\Code and stuff\\main.py'],
             pathex=['C:\\Users\\Scott Todd\\Desktop\\pyinstaller-2.0'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)

a.datas += [
            ("resources/game-bg.png","C:/Users/Scott Todd/Documents/Dropbox/GameJam-2012-Oct-27/Code and stuff/resources/game-bg.png","DATA"),
            ("resources/ant.png","C:/Users/Scott Todd/Documents/Dropbox/GameJam-2012-Oct-27/Code and stuff/resources/ant.png","DATA"),
            ("resources/eggs.png","C:/Users/Scott Todd/Documents/Dropbox/GameJam-2012-Oct-27/Code and stuff/resources/eggs.png","DATA"),
            ("resources/pause.png","C:/Users/Scott Todd/Documents/Dropbox/GameJam-2012-Oct-27/Code and stuff/resources/pause.png","DATA"),
            ("resources/web_node.png","C:/Users/Scott Todd/Documents/Dropbox/GameJam-2012-Oct-27/Code and stuff/resources/web_node.png","DATA"),
            ("resources/spider.png","C:/Users/Scott Todd/Documents/Dropbox/GameJam-2012-Oct-27/Code and stuff/resources/spider.png","DATA"),
            ("resources/instructions-arcade.png","C:/Users/Scott Todd/Documents/Dropbox/GameJam-2012-Oct-27/Code and stuff/resources/instructions-arcade.png","DATA"),
            ("resources/instructions-keyboard.png","C:/Users/Scott Todd/Documents/Dropbox/GameJam-2012-Oct-27/Code and stuff/resources/instructions-keyboard.png","DATA"),
            ("resources/HUD/hud-bg.png","C:/Users/Scott Todd/Documents/Dropbox/GameJam-2012-Oct-27/Code and stuff/resources/HUD/hud-bg.png","DATA"),
            ("resources/HUD/venom-base.png","C:/Users/Scott Todd/Documents/Dropbox/GameJam-2012-Oct-27/Code and stuff/resources/HUD/venom-base.png","DATA"),
            ("resources/HUD/venom-fill.png","C:/Users/Scott Todd/Documents/Dropbox/GameJam-2012-Oct-27/Code and stuff/resources/HUD/venom-fill.png","DATA"),
            ("resources/HUD/web-base.png","C:/Users/Scott Todd/Documents/Dropbox/GameJam-2012-Oct-27/Code and stuff/resources/HUD/web-base.png","DATA"),
            ("resources/HUD/web-fill.png","C:/Users/Scott Todd/Documents/Dropbox/GameJam-2012-Oct-27/Code and stuff/resources/HUD/web-fill.png","DATA"),
            ("resources/HUD/Spiderfingers.ttf","C:/Users/Scott Todd/Documents/Dropbox/GameJam-2012-Oct-27/Code and stuff/resources/HUD/Spiderfingers.ttf","DATA"),
           ]

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'Motherly Instinct.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True )
          
          