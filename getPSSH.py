import subprocess, base64


ID128 = "edef8ba979d64acea3c827dcd51d21ed"
psshstr = bytearray([0, 0, 0, 50, 112, 115, 115, 104, 0, 0, 0, 0])
str1 = bytearray([0, 0, 0, 18, 18, 16])

def dump_kid(path):
    process = subprocess.Popen(["bin/mp4dump.exe", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    result = process.communicate()[0]

    if "default_KID = [" in result:
        text = result.split("default_KID = [")[1].split("]")[0].replace(" ", "")
        textKid= get_pssh(text)
    else:
        textKid = "KID not found."
    return textKid


def get_pssh(kid):
    try:
        bytes_array = bytearray()
        bytes_array.extend(psshstr)
        bytes_array.extend(bytes.fromhex(ID128))
        bytes_array.extend(str1)
        bytes_array.extend(bytes.fromhex(kid))
        text = base64.b64encode(bytes_array).decode('utf-8')
        print("PSSH: "+text)
    except:
        text = "PSSH not found."
    return text