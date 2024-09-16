#include "vec.h"

vec2::vec2()
{
	this->x = 0.0f;
	this->y = 0.0f;
}

vec2::vec2(const float x, const float y)
{
	this->x = x;
	this->y = y;
}

vec2::vec2(const float* ptr)
{
	this->x = *ptr;
	this->y = *ptr + 1;
}

vec2 vec2::operator*(const float rhs) const
{
	return vec2(this->x * rhs, this->y * rhs);
}

vec2 vec2::operator+(const vec2 rhs) const
{
	return vec2(this->x + rhs.x, this->y + rhs.y);
}

vec2 vec2::operator+(const float rhs) const
{
	return vec2(this->x + rhs, this->y + rhs);
}

vec2 vec2::operator-(const vec2 rhs) const
{
	return vec2(this->x - rhs.x, this->y - rhs.y);
}

vec2 vec2::operator-(const float rhs) const
{
	return vec2(this->x - rhs, this->y - rhs);
}

vec2 vec2::normalize() const {
	float magnitude = sqrt((this->x * this->x) + (this->y * this->y));
	return vec2(this->x / magnitude, this->y / magnitude);
}


vec3::vec3()
{
	this->x = 0.0f;
	this->y = 0.0f;
	this->z = 0.0f;
}

vec3::vec3(const float x, const float y, const float z)
{
	this->x = x;
	this->y = y;
	this->z = z;
}

vec3::vec3(const float* ptr)
{
	this->x = *ptr;
	this->y = *ptr + 1;
	this->z = *ptr + 2;
}

vec3 vec3::operator*(const float rhs) const
{
	return vec3(this->x * rhs, this->y * rhs, this->z * rhs);
}

vec3 vec3::operator+(const vec3 rhs) const
{
	return vec3(this->x + rhs.x, this->y + rhs.y, this->z + rhs.z);
}

vec3 vec3::operator+(const float rhs) const
{
	return vec3(this->x + rhs, this->y + rhs, this->z + rhs);
}

vec3 vec3::operator-(const vec3 rhs) const
{
	return vec3(this->x - rhs.x, this->y - rhs.y, this->z - rhs.z);
}

vec3 vec3::operator-(const float rhs) const
{
	return vec3(this->x - rhs, this->y - rhs, this->z - rhs);
}

vec3 vec3::normalize() const {
	float magnitude = sqrt((this->x * this->x) + (this->y * this->y) + (this->z * this->z));
	return vec3(this->x / magnitude, this->y / magnitude, this->z / magnitude);
}