import struct, json, os

try:
    os.mkdir('input')
    os.mkdir('output')

except:
    pass

codename=input("Enter a map to decrypt: ")
codenamelow=codename.lower()

f = open("input/"+codenamelow+"mu.tpl.ckd","rb")

mutpl={
    "__class": "Actor_Template",
    "WIP": 0,
    "LOWUPDATE": 0,
    "UPDATE_LAYER": 0,
    "PROCEDURAL": 0,
    "STARTPAUSED": 0,
    "FORCEISENVIRONMENT": 0,
    "COMPONENTS": [{
            "__class": "JD_BlockFlowTemplate",
            "IsMashUp": 1,
            "IsPartyMaster": 0,
            "BlockDescriptorVector": []}]}

#header
f.read(64)

#info
maptapes = struct.unpack('>I', f.read(4))[0]
print(maptapes)
for x in range(maptapes):
    #base input
    baseclassentry = f.read(8)

    len_basesongname = struct.unpack('>I', f.read(4))[0]

    basesongname = f.read(len_basesongname).decode("utf-8")

    basejdversion = struct.unpack('>I', f.read(4))[0]

    basefirstbeat = struct.unpack('>i', f.read(4))[0]

    baselastbeat = struct.unpack('>I', f.read(4))[0]

    basesongswitch = struct.unpack('>I', f.read(4))[0]

    basevideooff1 = struct.unpack('>f', f.read(4))[0]

    basevideooff2 = struct.unpack('>f', f.read(4))[0]

    basevideoscale = struct.unpack('>f', f.read(4))[0]

    len_basemovename=struct.unpack('>I', f.read(4))[0]

    basemovename=f.read(len_basemovename).decode("utf-8")

    baseblockclip={"__class":"JD_BlockDescriptor","songName": basesongname,"jdVersion": basejdversion,"frstBeat": basefirstbeat,"lastBeat": baselastbeat,"songSwitch": basesongswitch,"videoCoachOffset": [basevideooff1, basevideooff2],"videoCoachScale": basevideoscale,"danceStepName": basemovename}

    blockreplaceclip={
    "__class": "JD_BlockReplacements",
    "BaseBlock": baseblockclip,
    "AlternativeBlocks": []
    }

    #replacing parts

    altblock = struct.unpack('>I', f.read(4))[0]
    for x in range(altblock):

        altclassentry = f.read(4)

        len_altsongname = struct.unpack('>I', f.read(4))[0]

        altsongname = f.read(len_altsongname).decode("utf-8")

        altjdversion = struct.unpack('>I', f.read(4))[0]

        altfirstbeat = struct.unpack('>i', f.read(4))[0]

        altlastbeat = struct.unpack('>I', f.read(4))[0]

        altsongswitch = struct.unpack('>I', f.read(4))[0]

        altvideooff1 = struct.unpack('>f', f.read(4))[0]

        altvideooff2 = struct.unpack('>f', f.read(4))[0]

        altvideoscale = struct.unpack('>f', f.read(4))[0]

        len_altmovename=struct.unpack('>I', f.read(4))[0]

        altmovename=f.read(len_altmovename).decode("utf-8")

        altblockclip={"__class":"JD_BlockDescriptor","songName":altsongname,"jdVersion": altjdversion,"frstBeat":altfirstbeat,"lastBeat":altlastbeat,"songSwitch":altsongswitch,"videoCoachOffset":[altvideooff1,altvideooff2],"videoCoachScale":altvideoscale,"danceStepName":altmovename}

        blockreplaceclip["AlternativeBlocks"].append(altblockclip)

    mutpl["COMPONENTS"][0]["BlockDescriptorVector"].append(blockreplaceclip)

f.close()

mudec = open("output/"+codenamelow+"mu.tpl.ckd", "w")
mudec.write(json.dumps(mutpl))
mudec.close()
