import base64
import sys
if len(sys.argv) < 2:
    print("usage: ./convert64 [image_file]")
    exit()
f_name = sys.argv[1]

with open(f_name, "rb") as f:
    enc = base64.b64encode(f.read())

save_f_name = f_name.split(".")[0] + ".b64"

with open(save_f_name, "w") as f:
    f.write(enc.decode('utf-8'))
