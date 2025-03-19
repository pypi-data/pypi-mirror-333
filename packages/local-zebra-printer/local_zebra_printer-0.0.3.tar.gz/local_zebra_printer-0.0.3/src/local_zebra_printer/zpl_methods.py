import requests


def get_zpl_image_via_api(zpl, height=152.4, width=101.6, dpmm=8):
    def convert_mm_to_inch(value):
        return value / 25.4

    inch_height = convert_mm_to_inch(height)
    inch_width = convert_mm_to_inch(width)
    url = f"http://api.labelary.com/v1/printers/{dpmm}dpmm/labels/{inch_width}x{inch_height}/0/"
    files = {"file": zpl}
    # headers = {'Accept' : 'application/pdf'} # omit this line to get PNG images back
    response = requests.post(url, files=files, stream=True)

    if response.status_code == 200:
        response.raw.decode_content = True
        return response.raw
    else:
        print("Error: " + response.text)


def prettify_zpl_code(zpl):
    zpl = zpl.replace("\n", "")
    zpl_commands = zpl.split("^")
    new_zpl = ""
    for line in zpl_commands:
        if line:
            # fs and xa do not need a prepended newline
            if line[0:2] not in ["FS", "XA"]:
                new_zpl += "\n"
            # give comments extra space for structure
            if line[0:2] in ["FX"]:
                new_zpl += "\n"
            new_zpl += f"^{line}"
    return new_zpl


DEFAULT_LABELARY_ZPL = """^XA

^FX Top section with logo, name and address.
^CF0,60
^FO50,50^GB100,100,100^FS
^FO75,75^FR^GB100,100,100^FS
^FO93,93^GB40,40,40^FS
^FO220,50^FDIntershipping, Inc.^FS
^CF0,30
^FO220,115^FD1000 Shipping Lane^FS
^FO220,155^FDShelbyville TN 38102^FS
^FO220,195^FDUnited States (USA)^FS
^FO50,250^GB700,3,3^FS

^FX Second section with recipient address and permit information.
^CFA,30
^FO50,300^FDJohn Doe^FS
^FO50,340^FD100 Main Street^FS
^FO50,380^FDSpringfield TN 39021^FS
^FO50,420^FDUnited States (USA)^FS
^CFA,15
^FO600,300^GB150,150,3^FS
^FO638,340^FDPermit^FS
^FO638,390^FD123456^FS
^FO50,500^GB700,3,3^FS

^FX Third section with bar code.
^BY5,2,270
^FO100,550^BC^FD12345678^FS

^FX Fourth section (the two boxes on the bottom).
^FO50,900^GB700,250,3^FS
^FO400,900^GB3,250,3^FS
^CF0,40
^FO100,960^FDCtr. X34B-1^FS
^FO100,1010^FDREF1 F00B47^FS
^FO100,1060^FDREF2 BL4H8^FS
^CF0,190
^FO470,955^FDCA^FS

^XZ
"""