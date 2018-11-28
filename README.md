# pydmg

This project is work in progress, not much to say for now.

Use pypy for performance. Make sure SDL is installed.

```
pacman -S sdl sdl_ttf sdl_gfx sdl_mixer sdl_image sdl_sound portmidi
virtualenv3 -p /usr/bin/pypy3 pypy
pip install -r requirements.txt
pypy/bin/pypy pydmg.py --help
```

# Resources

Boot ROM disassemlby
https://gist.github.com/drhelius/6063288

The Ultimate Game Boy Talk (33c3)
https://www.youtube.com/watch?v=HyzD8pNlpwI

Game Boy CPU Manual
http://marc.rawer.de/Gameboy/Docs/GBCPUman.pdf

Game Boy instruction set
http://www.pastraiser.com/cpu/gameboy/gameboy_opcodes.html

Pan Docs
http://bgb.bircd.org/pandocs.htm

RealBoy
https://realboyemulator.wordpress.com/

Game Boy Development Wiki
http://gbdev.gg8.se/wiki/articles/Main_Page

Game Boy Developers Kit
http://gbdk.sourceforge.net/


## Similar projects

https://github.com/Baekalfen/PyBoy

