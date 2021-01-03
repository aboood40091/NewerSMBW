#pragma once

#include <game.h>
#include <profileid.h>

struct SpriteData
{
    u16 profileId;

    s32 xoffs;
    s32 yoffs;
    s32 spawnRangeOffset[2];
    s32 spawnRangeSize[2];
    u16 _1C;
    u16 _1E;
    u16 _20;
    u16 _22;
    u16 flags;
};

class Profile
{
public:
    Profile(dActor_c* (*buildFunc)(), u32 spriteId, const SpriteData& spriteData, u16 executeOrderProfileId, u16 drawOrderProfileId, const char* name, const char** files=NULL);

    dActor_c* (*buildFunc)();
    u16 executeOrderProfileId;
    u16 drawOrderProfileId;
};

extern SpriteData originalSprites[483];
extern SpriteData sprites[];

extern Profile* originalProfiles[750];
extern Profile* profiles[];
