

disk = open('KSDU_016.img', 'rb')

#400 - something named (MULTISOUNDS? - WTB = WAVETABLES?)
#       theres 10 of them, ecah taking up 40 bytes

#800 - SYS1
#840 - SYS2
#880 - SYS3
#8C0 - SYS 4
#900 - WTBLIST?
#940 - GMIDIPARASAV (global midi parameters?)
#980 - More WTBs

#2000 - System A programs (each 8 bytes - stops at 2400 maybe..?)
#       The manual says 32 programs per system
#2C00 - System B programs (with some extras at the start..?)
#4C00 - System C programs (again, some extra at the start)
#5800 - System D programs

#6400 - Multisound name list
#       Manual says 16 of these max

#7000 - PCM data

disk.seek(0x7000)
data = disk.read(0x79000)

output = []
for i in range(0, len(data), 3):
  

disk.close()