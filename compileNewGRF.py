import pandas as pd
import math
import os

import pysrc.newTrack as new

main = open('indtrak.pnml', 'w')#w overrides, a appends
main.write("#include \"src/header.pnml\"\n" +
"#include \"src/template.pnml\"\n" +
"#include \"src/tt-table.pnml\"\n" +
"#include \"src/gui.pnml\"\n" +
"spriteset (NO_fences, \"grf/ISR_DPRK_S.png\") {\n" +
"	tmpl_no_fences()\n" +
"}")
main.close()

trackList = pd.read_table("pysrc/all.csv", sep = ',')
amountHouses = trackList.shape[0]
for i in range(24):
	new.addTracks(csvID = i)


main = open('indtrak.pnml', 'a')#w overrides, a appends
main.write("\n\n#include \"src/compatibility.pnml\"\n")
main.close()



#Outputs the final grf file
os.system('make -B')