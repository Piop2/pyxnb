import os
import sys

from PIL import Image

import xnb
import graphics

if len(sys.argv) != 2:
    print('Usage: {:s} <input_folder_path>'.format(sys.argv[0]))
    sys.exit(1)

input_path = sys.argv[1]
output_path = sys.argv[1] + "_out"

if not os.path.exists(output_path):
    os.mkdir(output_path)

for (root, directories, files) in os.walk(input_path):
    for directory in directories:
        directory_path = f"{output_path}{root[len(input_path):]}\\{directory}"
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)

    for file in files:
        file_path = os.path.join(root, file)
        if not file_path.endswith(".xnb"):
            break

        try:
            xnb_file = xnb.XNBFile(file_path)
        except NotImplementedError:
            print(f"PASSED: {file_path}")
            break

        xnb_grapic_object = xnb_file.primaryObject

        assert isinstance(xnb_grapic_object, graphics.Texture2D), "Expected graphics.Texture2D in XNB file"

        if xnb_grapic_object.surface_format != graphics.Texture2D.FORMAT_COLOR:
            raise NotImplementedError("Only the 'COLOR' texture format is supported right now")

        image = Image.frombytes(
            "RGBA", 
            (
                xnb_grapic_object.width, 
                xnb_grapic_object.height
            ), 
            xnb_grapic_object.mips[0]
        )

        image.save(f"{output_path}{root[len(input_path):]}\\{file.split(".")[0]}.png")
