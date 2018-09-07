#!/usr/bin/env python
# Intel ME Manufacturing Mode Detection Tools (Positive Technologies)
# https://github.com/ptresearch/mmdetect

import os, platform, sys
import argparse, subprocess, tempfile
import re, shutil
import requests
import zipfile

PCIUTILSVER = "3.5.5"
PCIUTILSFILENAME = "pciutils-" + PCIUTILSVER + "-win32"
PCIUTILSFILENAMEEX = PCIUTILSFILENAME+".zip"
LSPCIURL = "https://eternallybored.org/misc/pciutils/releases/"
FULLURL = LSPCIURL + PCIUTILSFILENAMEEX

def GetPCIUtils():
    pciUtilsReq = requests.get(FULLURL)
    if pciUtilsReq.status_code != requests.codes.ok:
        print("[-] Error: Cannot download PCIUtils")
        sys.exit(-1)
    print("[+] PCIUtils downloaded successfully")
    return pciUtilsReq.content

def FindMEDevice(fileName):
    PCIREGEX = r'(?P<pci_bdf>[0-9a-fA-F]{2}:[0-9a-fA-F]{2}\.[0-9a-fA-F])\ (?P<pci_class>[\w+\ \&\[\]\:\(\)\&\-\/]+)\: (?P<pci_name>[\w+\ \&\[\]\:\(\)\&\-\/]+)'
    try:
        lspci = subprocess.Popen([fileName],  stdout=subprocess.PIPE)
    except OSError(e):
        print("[-] Error: lspci not found")
        sys.exit(-1)
    output = lspci.communicate()[0]
    if lspci.returncode != 0:
        print("[-] Error: Couldn't run lspci (try again as admin)")
        sys.exit(-1)
    param = output.splitlines()
    pciRegExp = re.compile(PCIREGEX)
    for i in param:
        pciDevDesc = pciRegExp.search(str(i))
        if pciDevDesc.group("pci_class") == "Communication controller":
               if pciDevDesc.group("pci_name").find("ME Interface")!=-1 or (pciDevDesc.group("pci_name").find("HECI")!=-1 ):
                    return pciDevDesc.group("pci_bdf")
    return ""

def MeGetStatus(bdf, fileName):
    PCIREGEX = r'40\:\ (?P<me_fwsts1>[0-9a-fA-F]{2})'
    lspci = subprocess.Popen([fileName, "-s", bdf, "-xxx"],  stdout=subprocess.PIPE)
    output = lspci.communicate()[0]
    if lspci.returncode != 0:
        print("[-] Error: Couldn't run lspci")
        sys.exit(-1)
    pciRegExp = re.compile(PCIREGEX)
    regexp = pciRegExp.search(str(output))
    if (regexp == None):
        print("[-] Error: Couldn't get extended register (try again as root)")
        sys.exit(-1)
    val = regexp.group("me_fwsts1")
    return (int(val) & 1 << 4) != 0

def ParseArguments():
    parser = argparse.ArgumentParser(description='Manufecturing mode detection tool.')
    parser.add_argument('--path', metavar='PATH', help='path to lspci binary', type=str, default="")
    return parser.parse_args().path;

lspciName = {
    "Windows": ["lspci.exe"],
    "Linux":   ["lspci"],
}

def CheckPlatform():
   osType = platform.system()
   if not  osType in lspciName:
        print("[-] Error: Sorry, your platform isn't supported (%s)" % osType)
        sys.exit(-1)
   return osType

def InstallPCIUtils():
    if os.path.isfile(lspciName["Windows"][0]):
        print("[+] PCIUtils found")
        return "."
    print("[!] PCIUtils not found. Do you want install automatically (Y/N) [N]")
    ans = sys.stdin.read(1)
    if ans!="Y" and ans!="y":
        print("[!] Please install PCIUtils manually and try again")
        sys.exit(-1)
    pciUtilsZip = GetPCIUtils()
    pciUtilsDir =tempfile.mkdtemp()
    pciUtilsFileName = os.path.join(pciUtilsDir,"pciutils.zip")
    pciUtilsFile = open(pciUtilsFileName, "wb")
    pciUtilsFile.write(pciUtilsZip)
    pciUtilsFile.close()

    pciUtilsArch = zipfile.ZipFile(pciUtilsFileName)
    pciUtilsArch.extractall(path=pciUtilsDir)
    pciUtilsArch.close()

    os.remove(pciUtilsFileName)

    print("[+] PCIUtils extracted successfully")
    return os.path.join(pciUtilsDir,PCIUTILSFILENAME)

def main():
    lspciPath =  ParseArguments()
    osType = CheckPlatform()
    if osType == "Windows":
       lspciPath = InstallPCIUtils()

    lspciBin = lspciName[osType][0]

    if lspciPath!="":
        lspciBin = os.path.join(lspciPath,lspciBin)

    meBDF = FindMEDevice(lspciBin)
    if meBDF == "":
        print("[-] Error: ME device not found (hidden)")
        sys.exit(-1)

    print("[+] Intel ME device found: %s\n" % meBDF)

    if MeGetStatus(meBDF, lspciBin):
        print("[!] THIS SYSTEM IS VULNERABLE!!!")
    else:
        print("[+] This system isn't vulnerable.")

if __name__=="__main__":
    main()
