#pragma once
#include <stdint.h>

namespace size_of {
	// size of elements in bytes

	const uint8_t flt32 = 4;
	const uint8_t pos =  3 * flt32;
	const uint8_t norm = 3 * flt32;
	const uint8_t tan =  3 * flt32;
	const uint8_t bit =  3 * flt32;
	const uint8_t uv =   2 * flt32;

	const uint8_t inVert  = pos + norm + uv;
	const uint8_t outVert = inVert + bit + tan;
	const uint8_t inFace  = 3 * inVert;
	const uint8_t outFace = 3 * outVert;
}