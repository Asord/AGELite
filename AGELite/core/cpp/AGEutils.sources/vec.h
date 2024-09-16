#include <stdfloat>
#include <math.h>

/*
Crude implementation of a incomplete vector2 and vector3 classes.
These only implements operations needed in the bake_tangants() function.
*/

class vec2 {
public:
	float x;
	float y;

	vec2();
	vec2(const float x,const float y);
	vec2(const float* ptr);

	vec2 operator*(const float rhs) const;
	inline friend vec2 operator*(const float lhs, const vec2 rhs) { return rhs * lhs; }

	vec2 operator+(const vec2 rhs) const;
	vec2 operator+(const float rhs) const;
	inline friend vec2 operator+(const float lhs, const vec2 rhs) { return rhs + lhs; }
	
	vec2 operator-(const vec2 rhs) const;
	vec2 operator-(const float rhs) const;
	inline friend vec2 operator-(const float lhs, const vec2 rhs) { return rhs - lhs; }

	vec2 normalize() const;
};


class vec3 {
public:
	float x;
	float y;
	float z;

	vec3();
	vec3(const float x, const float y, const float z);
	vec3(const float* ptr);

	vec3 operator*(const float rhs) const;
	inline friend vec3 operator*(const float lhs, const vec3 rhs) { return rhs * lhs; }

	vec3 operator+(const vec3 rhs) const;
	vec3 operator+(const float rhs) const;
	inline friend vec3 operator+(const float lhs, const vec3 rhs) { return rhs + lhs; }

	vec3 operator-(const vec3 rhs) const;
	vec3 operator-(const float rhs) const;
	inline friend vec3 operator-(const float lhs, const vec3 rhs) { return rhs - lhs; }

	vec3 normalize() const;
};

