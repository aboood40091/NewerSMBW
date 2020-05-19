#pragma once

#include <common.h>
#include <game.h>

extern const char *FlipBlockFileList[];

class daEnFlipBlock_c : public daEnBlockMain_c {
public:
	Physics::Info physicsInfo;

	int onCreate();
	int onDelete();
	int onExecute();
	int onDraw();

	void calledWhenUpMoveExecutes();
	void calledWhenDownMoveExecutes();

	void blockWasHit(bool isDown);

	bool playerOverlaps();

	mHeapAllocator_c allocator;
	nw4r::g3d::ResFile resFile;
	m3d::mdl_c model;

	int flipsRemaining;

	USING_STATES(daEnFlipBlock_c);
	DECLARE_STATE(Wait);
	DECLARE_STATE(Flipping);

	static daEnFlipBlock_c *build();
};
