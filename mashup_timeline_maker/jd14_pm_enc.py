import struct, json, os
from unidecode import unidecode

try:
    os.mkdir('input')
    os.mkdir('output')

except:
    pass

codename=input("Enter a map to encrypt: ")
codenamelow=codename.lower()

with open(codenamelow+"pm.tpl.ckd") as f:
    tape=json.load(f)

enc=open("ENCRYPTED_"+codenamelow+"pm.tpl.ckd","wb")
tapecount=len(tape["COMPONENTS"][0]["BlockDescriptorVector"])
print(tapecount)
tape_version=int(tapecount*2000)
#header
enc.write(b'\x00\x00\x00\x01'+struct.pack(">I",tape_version)+b'\x1B\x85\x7B\xCE\x00\x00\x00\xAC\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x5B\x64\x8E\x44\x00\x00\x00\x2C')
if tape["COMPONENTS"][0]["IsMashUp"]==1:
    enc.write(b'\x00\x00\x00\x01\x00\x00\x00\x00')
elif tape["COMPONENTS"][0]["IsPartyMaster"]==1:
    enc.write(b'\x00\x00\x00\x00\x00\x00\x00\x01')
else:
    enc.write(b'\x00\x00\x00\x00\x00\x00\x00\x00')

#blockflow tapes
tapeclips=struct.pack(">I",tapecount)
for blockflow in tape["COMPONENTS"][0]["BlockDescriptorVector"]:
        tapeclips+=b'\x00\x00\x01\xA8\x00\x00\x01\x94'
        basemapname=unidecode(blockflow["BaseBlock"]["songName"])
        tapeclips+=struct.pack(">I",len(basemapname))+basemapname.encode()
        tapeclips+=struct.pack(">I",blockflow["BaseBlock"]["jdVersion"])
        tapeclips+=struct.pack(">i",blockflow["BaseBlock"]["frstBeat"])
        tapeclips+=struct.pack(">i",blockflow["BaseBlock"]["lastBeat"])
        tapeclips+=struct.pack(">I",blockflow["BaseBlock"]["songSwitch"])
        tapeclips+=struct.pack(">f",blockflow["BaseBlock"]["videoCoachOffset"][0])
        tapeclips+=struct.pack(">f",blockflow["BaseBlock"]["videoCoachOffset"][1])
        tapeclips+=struct.pack(">f",blockflow["BaseBlock"]["videoCoachScale"])
        basemovename=unidecode(blockflow["BaseBlock"]["danceStepName"])
        tapeclips+=struct.pack(">I",len(basemovename))+basemovename.encode()
        tapeclips+=struct.pack(">I",len(blockflow["AlternativeBlocks"]))
        for altblock in blockflow["AlternativeBlocks"]:
            tapeclips+=b'\x00\x00\x01\x94'
            altmapname=unidecode(altblock["songName"])
            tapeclips+=struct.pack(">I",len(altmapname))+altmapname.encode()
            tapeclips+=struct.pack(">I",altblock["jdVersion"])
            tapeclips+=struct.pack(">i",altblock["frstBeat"])
            tapeclips+=struct.pack(">i",altblock["lastBeat"])
            tapeclips+=struct.pack(">I",altblock["songSwitch"])
            tapeclips+=struct.pack(">f",altblock["videoCoachOffset"][0])
            tapeclips+=struct.pack(">f",altblock["videoCoachOffset"][1])
            tapeclips+=struct.pack(">f",altblock["videoCoachScale"])
            altmovename=unidecode(altblock["danceStepName"])
            tapeclips+=struct.pack(">I",len(altmovename))+altmovename.encode()

enc.write(tapeclips)