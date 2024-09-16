# Program shader hotswap

## Current implementation
Loads the new shader mgl.program once to detect potential errors then if there is no error, release the old mgl.program and load once again the new one before assiging it to the Program object.

```py
(...)
try:
    _program = self.ctx.program(self.vertex_shader, self.fragment_shader)
    _program.release()
except Exception as e:
    print(f"Error compiling {self.vertex_shader} and {self.fragment_shader}: {e}")
else:
    self.program.release()
    self.program = self.ctx.program(self.vertex_shader, self.fragment_shader)
```

## Issue
mgl.VAOs are initialized with a mgl.program. It bind the mgl.program automatically before rendering.
But if we don't free the previous program before assigning a new one, the new one's glo will be different.

If we try to create a new mgl.program before releasing the old one, the new mgl.program will have a different
glo and it can't be saved as "our program" (or we have to recreate all VAOs)

We can't store the new (possibly errored) mgl.program and the old one at the same time. As
mgl.program.release() free the glo of the program which can be taked by the new one and 
therefore be assigned to all the VAOs.


```py
p: mgl.Program = None
try:
    p = self.ctx.program(self.vertex_shader, self.fragment_shader)
except Exception as e:
    print(f"Error compiling {self.vertex_shader} and {self.fragment_shader}: {e}")
else:
    self.program.release()
    self.program = p
```

```py
p: mgl.Program = None
self.program.release()
try:
    p = self.ctx.program(self.vertex_shader, self.fragment_shader)
except Exception as e:
    print(f"Error compiling {self.vertex_shader} and {self.fragment_shader}: {e}")
    p = self.ctx.program(self.previous_vertex_shader, self.previous_fragment_shader)
else:
    self.program = p
```
These two examples leads both to the mgl.program.glo being altered and therefore breaks all existing VAOs.
