#pragma once

#include <game.h>
#include "profileid.h"

struct SpriteData
{
    u16 profileId;
    s32 xoffs;
    s32 yoffs;
    Recti spawnRange;
    u16 _1C;
    u16 _1E;
    u16 _20;
    u16 _22;
    u16 flags;
};

class Profile
{
public:
    Profile(dActor_c* (*buildFunc)(), u32 spriteId, const SpriteData& spriteData, u16 unk1, u16 unk2, const char* name, const char** files=NULL);

    dActor_c* (*buildFunc)();
    u16 _4;
    u16 _6;
};

extern "C" SpriteData originalSprites[483];
extern "C" SpriteData sprites[];

extern "C" Profile* originalProfiles[750];
extern "C" Profile* profiles[];
