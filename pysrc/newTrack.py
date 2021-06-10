import pandas as pd
import math

def addTracks(csvID = 0):	
	trackList = pd.read_table("pysrc/all.csv", sep = ',')
	Name = trackList.at[csvID,"Name"]
	electrified = trackList.at[csvID,"Elec"]
	trackSet = trackList.at[csvID,"Set"]
	gauge = trackList.at[csvID,"Gauge"]
	if (electrified == "E"):
		spriteName = trackList.at[csvID,"Unelec"]
	else:
		spriteName = Name
		
	main = open('indtrak.pnml', 'a')#w overrides, a appends
	main.write("\n#include \"" + "src/tracks/" + Name + ".pnml" + "\"")
	main.close()
	f = open("src/tracks/" + Name + ".pnml", 'w')#w overrides, a appends
	
	if (electrified == "N"):
		f.write("//DPRK\n" +
		"spriteset (" + Name + "_DPRK_underlay, \"grf/" + trackSet + "_DPRK_" + gauge + ".png\") {\n" +
		"	tmpl_underlay_track_types()\n" +
		"}\n" +
		"spriteset (" + Name + "_DPRK_overlay, \"grf/" + trackSet + "_DPRK_" + gauge + ".png\") {\n" +
		"	tmpl_overlay_track_types()\n" +
		"}\n" +
		"spriteset (" + Name + "_DPRK_bridge, \"grf/" + trackSet + "_DPRK_" + gauge + ".png\") {\n" +
		"	tmpl_bridges_overlay()\n" +
		"}\n" +
		"//JP\n" +
		"spriteset (" + Name + "_JP_underlay, \"grf/" + trackSet + "_JP_" + gauge + ".png\") {\n" +
		"	tmpl_underlay_track_types()\n" +
		"}\n" +
		"spriteset (" + Name + "_JP_overlay, \"grf/" + trackSet + "_JP_" + gauge + ".png\") {\n" +
		"	tmpl_overlay_track_types()\n" +
		"}\n" +
		"spriteset (" + Name + "_JP_bridge, \"grf/" + trackSet + "_JP_" + gauge + ".png\") {\n" +
		"	tmpl_bridges_overlay()\n" +
		"}\n")
		
		if (gauge == "N"):
			f.write("spriteset (" + Name + "_JP_F_underlay, \"grf/" + trackSet + "_JP_" + gauge + "_F.png\") {\n" +
			"	tmpl_underlay_track_types()\n" +
			"}\n" +
			"spriteset (" + Name + "_JP_F_overlay, \"grf/" + trackSet + "_JP_" + gauge + "_F.png\") {\n" +
			"	tmpl_overlay_track_types()\n" +
			"}\n" +
			"spriteset (" + Name + "_JP_F_bridge, \"grf/" + trackSet + "_JP_" + gauge + "_F.png\") {\n" +
			"	tmpl_bridges_overlay()\n" +
			"}\n")
		
		f.write("//Univ\n" +
		"switch(FEAT_RAILTYPES, SELF, switch_" + Name + "_underlay,PARAM_STYLE) {\n" +
		"	2: " + Name + "_DPRK_underlay;\n")
		if (gauge == "N"):
			f.write("	1: " + Name + "_JP_F_underlay;\n")
		elif (gauge == "S"):
			f.write("	1: N" + Name[1:] + "_JP_underlay;\n")
		f.write("	" + Name + "_JP_underlay;\n" +
		"}\n" +
		"switch(FEAT_RAILTYPES, SELF, switch_" + Name + "_overlay,PARAM_STYLE) {\n" +
		"	2: " + Name + "_DPRK_overlay;\n")
		if (gauge == "N"):
			f.write("	1: " + Name + "_JP_F_overlay;\n")
		elif (gauge == "S"):
			f.write("	1: N" + Name[1:] + "_JP_overlay;\n")
		f.write("	" + Name + "_JP_overlay;\n" +
		"}\n" +
		"switch(FEAT_RAILTYPES, SELF, switch_" + Name + "_bridge,PARAM_STYLE) {\n" +
		"	2: " + Name + "_DPRK_bridge;\n")
		if (gauge == "N"):
			f.write("	1: " + Name + "_JP_F_bridge;\n")
		elif (gauge == "S"):
			f.write("	1: N" + Name[1:] + "_JP_bridge;\n")
		f.write("	" + Name + "_JP_bridge;\n" +
		"}\n\n")
	
	if (electrified == "N"):
		elecAvail = "2"
	else:
		elecAvail = "1"
	
	if (gauge == "S"):
		gaugeCheck = "PARAM_GAUGE != 1 && PARAM_GAUGE != 4"
	elif (gauge == "N"):
		gaugeCheck = "PARAM_GAUGE != 0 && PARAM_GAUGE != 4"
	elif (gauge == "D"):
		gaugeCheck = "PARAM_GAUGE == 3 || PARAM_GAUGE == 4"
	
	f.write("if(PARAM_" + trackSet + " == 1 && (PARAM_ELEC == 0 || PARAM_ELEC == " + elecAvail + ") && (" + gaugeCheck + ")){\n" +
	"item(FEAT_RAILTYPES, " + Name + "_ID, " + str(trackList.at[csvID,"Num"]) + ") {\n" +
	"     property {\n" +
	"         label:                      \"" + Name + "\";\n" +
	"         name:                       string(STR_" + Name + ");\n" +
	"         menu_text:                  string(STR_" + Name + ");\n" +
	"         build_window_caption:       string(STR_" + Name + "_BUILD_CAPTION);\n" +
	"         autoreplace_text:           string(STR_" + Name + "_AUTOREPLACE);\n" +
	"         new_engine_text:            string(STR_" + Name + "_NEW_ENGINE);\n" +
	"		 toolbar_caption:			 string(STR_" + Name + "_TB_CAPTION);\n" +
	"         compatible_railtype_list:   " + trackList.at[csvID,"RTC"] + ";\n" +
	"         powered_railtype_list:      " + trackList.at[csvID,"RTP"] + ";\n" +
	"		 alternative_railtype_list:  " + trackList.at[csvID,"RTA"] + ";\n" +
	"         speed_limit:                (0 == 0) ? 121 : 70 km/h;\n" +
	"         introduction_date:			 date(1800,1,1);\n" +
	"		 map_colour:				 " + trackList.at[csvID,"Colour"] + ";\n" +
	"         station_graphics:           RAILTYPE_STATION_NORMAL; \n" +
	"         acceleration_model:         ACC_MODEL_RAIL;\n" +
	"         construction_cost:          COSTPARAM(" + str(trackList.at[csvID,"CC"]) + ",PARAM_CONST);\n" +
	"		 maintenance_cost:		     COSTPARAM(" + str(trackList.at[csvID,"MC"]) + ",PARAM_MAINT);\n" +
	"		 sort_order:				 " + trackList.at[csvID,"Sort"] + ";\n")
	if (electrified == "E"):
		f.write("         railtype_flags: bitmask(RAILTYPE_FLAG_CATENARY);\n")
	
	f.write("     }\n" +
	"     graphics {\n" +
	"         track_overlay:		switch_" + spriteName + "_overlay;				// defines the sprites drawn as overlay for junctions and highlight\n" +
	"         underlay:			switch_" + spriteName + "_underlay;				// defines the usual tracks and the underlay for junctions\n" +
	"         level_crossings:			switch_cross_" + gauge + ";				// defines the usual tracks for crosings\n" +
	"         bridge_surfaces:	switch_" + spriteName + "_bridge;					// defines the overlay drawn over bridges\n" +
	"		 gui:				" + trackSet + "_" + electrified + "_gui;							// defines the gui sprites\n" +
	"         fences:         	NO_fences;       					// Custom Fences since v2\n")
	
	if (electrified == "E"):
		f.write("         catenary_wire:		switch_wires;\n" +
		"         catenary_pylons:		switch_poles;\n")
	
	f.write("     }\n" +
	" }\n" +
	" }\n")
	
	f.close()