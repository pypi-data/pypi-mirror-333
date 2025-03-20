#include "bindings.h"

#pragma once

#if defined(ON_PYTHON_COMPILE)

void initDefines(rh3dmpymodule& m);

py::dict PointToDict(const ON_3dPoint& point);
py::dict VectorToDict(const ON_3dVector& vector);
py::dict PlaneToDict(const ON_Plane& plane);
ON_3dPoint PointFromDict(py::dict& dict);
ON_3dVector VectorFromDict(py::dict& dict);
ON_Plane PlaneFromDict(py::dict& dict);

#else
void initDefines(void* m);

emscripten::val PointToDict(const ON_3dPoint& point);
emscripten::val VectorToDict(const ON_3dVector& vector);
emscripten::val PlaneToDict(const ON_Plane& plane);

#endif
