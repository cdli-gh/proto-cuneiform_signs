import os
import shutil
import sys

# Convert the PNGs to SVGs
def conv_to_svg(folder_path):
    folder_prefix = folder_path
    print("Converting the PNGs to SVGs for the folder " + folder_path)
    for filename in os.listdir(folder_path):
      if filename[-4:] in [".png", ".jpg", ".peg"]:
        file_id = os.path.splitext(filename)[0]
        file_id = file_id.replace('/', ' ') # necessary because of how UNIX file structures work
        print("Converting " + file_id + " ...")

        svg_path = 'svg_' + folder_prefix + '/' + file_id
        svg_path += '.svg'

        pnm_filepath = "misc_files/" + file_id + ".pnm"
        recolor_filepath = "misc_files/" + file_id + "_recolor.png"
        if os.path.exists(svg_path):
          print("   SVG file already exists! Converting anyway...")
          #continue

        cmds = []

        # Convert PNG into nongrayscale version so that imgmagick can read it properly
        if not os.path.exists(recolor_filepath):
          cmds.append('convert -density 300 "' + folder_path + '/' + filename + '" -quality 90 -colorspace RGB -background white -alpha remove -alpha off "' + recolor_filepath + '"')
        else:
          print("Recolored PNGs already exist!")

        # Convert PNG into PNM
        if not os.path.exists(pnm_filepath):
          cmds.append('convert "' + recolor_filepath + '" "' + pnm_filepath + '"')
        else:
          print("PNM files already exist!")

        # Potrace turns the PNM img to SVG (Potrace can't use PNG files)
        cmds.append('potrace "' + pnm_filepath + '" -s -o "' + svg_path + '"')

        # Remove the unneeded intermediate files (optional)
        #pt4 = "rm intermediate_files/*"
        # If you uncomment the above line, the code will use up a lot less space. But it's often helpful to keep the intermediate files to speed up subsequent conversion tasks

        for cmd in cmds:
          #print(cmd)
          os.system(cmd)

dir_name = str(input("Enter name of folder with PNG/JPG files: "))
conv_to_svg(dir_name)
