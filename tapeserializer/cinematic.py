import struct, os, json, zlib

print("JD2014 CINE SERIALIZER")
print("BY: JACKLSUMMER15 & RYANL181095")
codename=input("Enter your mapname: ")
codenamelow=codename.lower()

outputdirectory="output/"+codename
try:
    os.makedirs(outputdirectory)

except:
    pass

with open("input/"+codenamelow+"_mainsequence.tape.ckd") as f:
  ctape=json.load(f)
  
  tape={
    "__class": "Tape",
    "Clips": [],
    "TapeClock": 2,
    "TapeBarCount": 1,
    "FreeResourcesAfterPlay": 0,
    "MapName": codename,
    "SoundwichEvent": ""
  }

#only reading soundsetclips and removing other clips
for cine_clips in ctape["Clips"]:
  if cine_clips["__class"] == "SoundSetClip":
    cineid=cine_clips["Id"]
    cinetrackid=cine_clips["TrackId"]
    cineisactive=cine_clips["IsActive"]
    cinestarttime=cine_clips["StartTime"]
    cineduration=cine_clips["Duration"]
    cinesoundsetpath=cine_clips["SoundSetPath"].replace("maps","jd5")

    tape["Clips"].append({
            "__class": "SoundSetClip",
            "Id": cineid,
            "TrackId": cinetrackid,
            "IsActive": cineisactive,
            "StartTime": cinestarttime,
            "Duration": cineduration,
            "SoundSetPath": cinesoundsetpath,
            "SoundChannel": 0,
            "StartOffset": 0,
            "StopsOnEnd": 0,
            "AccountedForDuration": 0
        })

cineenc=open(outputdirectory+"/"+codenamelow+"_mainsequence.tape.ckd","wb")
tape_len=len(tape["Clips"])
tape_version=int((224*tape_len)+166)
cineenc.write(struct.pack(">I",1)+struct.pack(">I",tape_version)+b'\x9E\x84\x54\x60\x00\x00\x00\xAC')

clips=struct.pack(">I",len(tape["Clips"]))
for clip in tape["Clips"]:
  if clip['__class']=='SoundSetClip':
    filename=clip['SoundSetPath'].split("/")[-1]
    pathname=clip['SoundSetPath'].replace(filename,"")
    clips+=b'\x2D\x8C\x88\x5B\x00\x00\x00\x88'
    clips+=struct.pack(">I",clip["Id"])
    clips+=struct.pack(">I",clip["TrackId"])
    clips+=struct.pack(">I",clip["IsActive"])
    clips+=struct.pack(">i",clip["StartTime"])
    clips+=struct.pack(">i",clip["Duration"])
    clips+=b'\x00\x00\x00\x00'
    clips+=struct.pack(">I",len(pathname))+pathname.encode()+struct.pack(">I",len(filename))+filename.encode()+struct.pack("<I",zlib.crc32(filename.encode()))
    clips+=b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
cineenc.write(clips)

cineenc.write(struct.pack(">I",0)+struct.pack(">I",tape["TapeClock"]))
cineenc.close()