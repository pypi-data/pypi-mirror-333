#include <vector>
#include "bindings.h"

BND_NurbsSurfacePointList::BND_NurbsSurfacePointList(ON_NurbsSurface* surface, const ON_ModelComponentReference& compref)
{
  m_component_reference = compref;
  m_surface = surface;
}

ON_4dPoint BND_NurbsSurfacePointList::GetControlPoint1(std::tuple<int, int> index) const
{

  int u = std::get<0>(index);
  int v = std::get<1>(index);

  return GetControlPoint2(u, v);

}

ON_4dPoint BND_NurbsSurfacePointList::GetControlPoint2(int u, int v) const
{
#if defined(ON_PYTHON_COMPILE)
  if (u >= CountU() || v >= CountV() ||
      u < 0 || v < 0)
    throw py::index_error("list index out of range");
#endif
  ON_4dPoint pt;
  m_surface->GetCV(u, v, pt);
  return pt;
}

ON_3dPoint BND_NurbsSurfacePointList::GetPoint(int u, int v) const
{
#if defined(ON_PYTHON_COMPILE)
  if (u >= CountU() || v >= CountV() ||
      u < 0 || v < 0)
    throw py::index_error("list index out of range");
#endif
  ON_3dPoint pt;
  m_surface->GetCV(u, v, pt);
  return pt;
}

void BND_NurbsSurfacePointList::SetControlPoint1(std::tuple<int, int> index, ON_4dPoint point)
{
  int u = std::get<0>(index);
  int v = std::get<1>(index);

  return SetControlPoint2(u, v, point);
}

void BND_NurbsSurfacePointList::SetControlPoint2(int u, int v, ON_4dPoint point)
{
#if defined(ON_PYTHON_COMPILE)
  if (u >= CountU() || v >= CountV() ||
     u < 0 || v < 0)
    throw py::index_error("list index out of range");
#endif
  m_surface->SetCV(u, v, point);
}

BND_NurbsSurfaceKnotList::BND_NurbsSurfaceKnotList(ON_NurbsSurface* surface, int direction, const ON_ModelComponentReference& compref)
{
  m_component_reference = compref;
  m_surface = surface;
  m_direction = direction ? 1 : 0;
}

double BND_NurbsSurfaceKnotList::GetKnot(int index) const
{
#if defined(ON_PYTHON_COMPILE)
  if (index >= Count() || index < 0)
    throw py::index_error("list index out of range");
#endif
  return m_surface->Knot(m_direction, index);
}

void BND_NurbsSurfaceKnotList::SetKnot(int index, double k)
{
#if defined(ON_PYTHON_COMPILE)
  if (index >= Count() || index < 0)
    throw py::index_error("list index out of range");
#endif
  m_surface->SetKnot(m_direction, index, k);
}

BND_TUPLE BND_NurbsSurfaceKnotList::ToList()
{

  int count =  m_surface->KnotCount(m_direction);
  if( count > 0) {
    BND_TUPLE rc = CreateTuple(count);
    for (int i = 0; i < count; i++)
      SetTuple(rc, i, m_surface->Knot(m_direction, i));

    return rc;
  }

  return NullTuple();

}

std::vector<double> BND_NurbsSurfaceKnotList::ToList2()
{
  int count = m_surface->KnotCount(m_direction);
  if( count > 0) 
  {
    return std::vector<double>(
      m_surface->m_knot[m_direction],
      m_surface->m_knot[m_direction] + m_surface->KnotCount(m_direction));
  }
  return std::vector<double>();
}

BND_NurbsSurface::BND_NurbsSurface(ON_NurbsSurface* nurbssurface, const ON_ModelComponentReference* compref)
{
  SetTrackedPointer(nurbssurface, compref);
}

void BND_NurbsSurface::SetTrackedPointer(ON_NurbsSurface* nurbssurface, const ON_ModelComponentReference* compref)
{
  m_nurbssurface = nurbssurface;
  BND_Surface::SetTrackedPointer(nurbssurface, compref);
}

BND_NurbsSurface* BND_NurbsSurface::Create(int dimension, bool isRational, int order0, int order1, int controlPointCount0, int controlPointCount1)
{
  ON_NurbsSurface* ns = ON_NurbsSurface::New(dimension, isRational, order0, order1, controlPointCount0, controlPointCount1);
  if (nullptr == ns)
    return nullptr;
  return new BND_NurbsSurface(ns, nullptr);
}
BND_NurbsSurface* BND_NurbsSurface::CreateFromCone(const BND_Cone& cone)
{
  ON_NurbsSurface* ns = ON_NurbsSurface::New();
  if (0 == cone.m_cone.GetNurbForm(*ns))
  {
    delete ns;
    return nullptr;
  }
  return new BND_NurbsSurface(ns, nullptr);
}
BND_NurbsSurface* BND_NurbsSurface::CreateFromCylinder(const BND_Cylinder& cylinder)
{
  ON_NurbsSurface* ns = ON_NurbsSurface::New();
  if( 0 == cylinder.m_cylinder.GetNurbForm(*ns) )
  {
    delete ns;
    return nullptr;
  }
  return new BND_NurbsSurface(ns, nullptr);
}
BND_NurbsSurface* BND_NurbsSurface::CreateFromSphere(const BND_Sphere& sphere)
{
  ON_NurbsSurface* ns = ON_NurbsSurface::New();
  if (0 == sphere.m_sphere.GetNurbForm(*ns))
  {
    delete ns;
    return nullptr;
  }
  return new BND_NurbsSurface(ns, nullptr);
}
//BND_NurbsSurface* BND_NurbsSurface::CreateFromTorus(const BND_Torus& torus)
//{
//  ON_NurbsSurface* ns = ON_NurbsSurface::New();
//  if (0 == torus.m_torus.GetNurbForm(*ns))
//  {
//    delete ns;
//    return nullptr;
//  }
//  return new BND_NurbsSurface(ns, nullptr);
//}


BND_NurbsSurface* BND_NurbsSurface::CreateRuledSurface(const class BND_Curve* curveA, const class BND_Curve* curveB)
{
  if (nullptr == curveA || nullptr == curveB)
    return nullptr;
  ON_NurbsSurface* ns = new ON_NurbsSurface();
  const ON_Curve* a = curveA->m_curve;
  const ON_Curve* b = curveB->m_curve;
  if (0 == ns->CreateRuledSurface(*a, *b))
  {
    delete ns;
    return nullptr;
  }
  return new BND_NurbsSurface(ns, nullptr);
}

BND_NurbsSurfaceKnotList BND_NurbsSurface::KnotsU()
{
  return BND_NurbsSurfaceKnotList(m_nurbssurface, 0, m_component_ref);
}

BND_NurbsSurfaceKnotList BND_NurbsSurface::KnotsV()
{
  return BND_NurbsSurfaceKnotList(m_nurbssurface, 1, m_component_ref);
}

BND_NurbsSurfacePointList BND_NurbsSurface::Points()
{
  return BND_NurbsSurfacePointList(m_nurbssurface, m_component_ref);
}


#if defined(ON_PYTHON_COMPILE)

void initNurbsSurfaceBindings(rh3dmpymodule& m)
{
#if defined(NANOBIND)
  py::class_<BND_NurbsSurfaceKnotList>(m, "NurbsSurfaceKnotList")
#else
  py::class_<BND_NurbsSurfaceKnotList>(m, "NurbsSurfaceKnotList", py::buffer_protocol())
#endif
    .def("__len__", &BND_NurbsSurfaceKnotList::Count)
    .def("__getitem__", &BND_NurbsSurfaceKnotList::GetKnot)
    .def("__setitem__", &BND_NurbsSurfaceKnotList::SetKnot)
    .def("ToList", &BND_NurbsSurfaceKnotList::ToList)
    .def("ToList2", &BND_NurbsSurfaceKnotList::ToList2)
#if !defined(NANOBIND)
    .def_buffer([](BND_NurbsSurfaceKnotList& kl) -> py::buffer_info
      {
        return py::buffer_info
        (
          kl.GetSurface()->m_knot[kl.GetDirection()],  /* Pointer to buffer */
          sizeof(double),                           /* Size of one scalar */
          py::format_descriptor<double>::format(),  /* Python struct-style format descriptor */
          1,                                        /* Number of dimensions */
          {kl.Count()},                             /* Buffer dimensions */
          {sizeof(double)}                          /* Strides (in bytes) for each index */
        );
      })
#endif
    .def("InsertKnot", &BND_NurbsSurfaceKnotList::InsertKnot, py::arg("value"), py::arg("multiplicity"))
    .def("KnotMultiplicity", &BND_NurbsSurfaceKnotList::KnotMultiplicity, py::arg("index"))
    .def("CreateUniformKnots", &BND_NurbsSurfaceKnotList::CreateUniformKnots, py::arg("knotSpacing"))
    .def("CreatePeriodicKnots", &BND_NurbsSurfaceKnotList::CreatePeriodicKnots, py::arg("knotSpacing"))
    .def_property_readonly("IsClampedStart", &BND_NurbsSurfaceKnotList::IsClampedStart)
    .def_property_readonly("IsClampedEnd", &BND_NurbsSurfaceKnotList::IsClampedEnd)
    .def("SuperfluousKnot", &BND_NurbsSurfaceKnotList::SuperfluousKnot, py::arg("start"))
    ;

#if defined(NANOBIND)
  py::class_<BND_NurbsSurfacePointList>(m, "NurbsSurfacePointList")
#else
  py::class_<BND_NurbsSurfacePointList>(m, "NurbsSurfacePointList", py::buffer_protocol())
#endif
    .def("__len__", &BND_NurbsSurfacePointList::Count)
    .def_property_readonly("CountU", &BND_NurbsSurfacePointList::CountU)
    .def_property_readonly("CountV", &BND_NurbsSurfacePointList::CountV)
    .def("__getitem__", &BND_NurbsSurfacePointList::GetControlPoint1)
    .def("GetPoint", &BND_NurbsSurfacePointList::GetPoint, py::arg("u"), py::arg("v") )
    .def("GetControlPoint", &BND_NurbsSurfacePointList::GetControlPoint2, py::arg("u"), py::arg("v") )
    .def("__setitem__", &BND_NurbsSurfacePointList::SetControlPoint1)
#if !defined(NANOBIND)
    .def_buffer([](BND_NurbsSurfacePointList& pl) -> py::buffer_info
    {
      return py::buffer_info
      (
        pl.GetSurface()->m_cv,                    /* Pointer to buffer */
        sizeof(double),                           /* Size of one scalar */
        py::format_descriptor<double>::format(),  /* Python struct-style format descriptor */
        3,                                        /* Number of dimensions */
        {pl.CountU(), pl.CountV(), pl.GetCVDims() },  /* Buffer dimensions */
        {
          pl.GetSurface()->m_cv_stride[0] * sizeof(double),
          pl.GetSurface()->m_cv_stride[1] * sizeof(double),
          sizeof(double)
        }                                         /* Strides (in bytes) for each index */
      );
    })
#endif
    .def("MakeRational", &BND_NurbsSurfacePointList::MakeRational)
    .def("MakeNonRational", &BND_NurbsSurfacePointList::MakeNonRational)
    ;
  py::class_<BND_NurbsSurface, BND_Surface>(m, "NurbsSurface")
    .def_static("Create", &BND_NurbsSurface::Create, py::arg("dimension"), py::arg("isRational"), py::arg("order0"), py::arg("order1"), py::arg("controlPointCount0"), py::arg("controlPointCount1"))
    .def_static("CreateFromCone", &BND_NurbsSurface::CreateFromCone, py::arg("cone"))
    .def_static("CreateFromSphere", &BND_NurbsSurface::CreateFromSphere, py::arg("sphere"))
    .def_static("CreateFromCylinder", &BND_NurbsSurface::CreateFromCylinder, py::arg("cylinder"))
    .def_static("CreateRuledSurface", &BND_NurbsSurface::CreateRuledSurface, py::arg("curveA"), py::arg("curveB"))
    .def_property_readonly("IsRational", &BND_NurbsSurface::IsRational)
    .def("MakeRational", &BND_NurbsSurface::MakeRational)
    .def("MakeNonRational", &BND_NurbsSurface::MakeNonRational)
    .def("IncreaseDegreeU", &BND_NurbsSurface::IncreaseDegreeU, py::arg("desiredDegree"))
    .def("IncreaseDegreeV", &BND_NurbsSurface::IncreaseDegreeV, py::arg("desiredDegree"))
    .def_property_readonly("OrderU", &BND_NurbsSurface::OrderU)
    .def_property_readonly("OrderV", &BND_NurbsSurface::OrderV)
    .def_property_readonly("KnotsU", &BND_NurbsSurface::KnotsU)
    .def_property_readonly("KnotsV", &BND_NurbsSurface::KnotsV)
    .def_property_readonly("Points", &BND_NurbsSurface::Points)
    ;
}

#endif

#if defined(ON_WASM_COMPILE)
using namespace emscripten;

void initNurbsSurfaceBindings(void*)
{
  class_<BND_NurbsSurfaceKnotList>("NurbsSurfaceKnotList")
    .property("count", &BND_NurbsSurfaceKnotList::Count)
    .function("get", &BND_NurbsSurfaceKnotList::GetKnot)
    .function("set", &BND_NurbsSurfaceKnotList::SetKnot)
    .function("toList", &BND_NurbsSurfaceKnotList::ToList)
    .function("insertKnot", &BND_NurbsSurfaceKnotList::InsertKnot)
    .function("knotMultiplicity", &BND_NurbsSurfaceKnotList::KnotMultiplicity)
    .function("createUniformKnots", &BND_NurbsSurfaceKnotList::CreateUniformKnots)
    .function("createPeriodicKnots", &BND_NurbsSurfaceKnotList::CreatePeriodicKnots)
    .property("isClampedStart", &BND_NurbsSurfaceKnotList::IsClampedStart)
    .property("isClampedEnd", &BND_NurbsSurfaceKnotList::IsClampedEnd)
    .function("superfluousKnot", &BND_NurbsSurfaceKnotList::SuperfluousKnot)
    ;

  class_<BND_NurbsSurfacePointList>("NurbsSurfacePointList")
    .property("count", &BND_NurbsSurfacePointList::Count)
    .property("countU", &BND_NurbsSurfacePointList::CountU)
    .property("countV", &BND_NurbsSurfacePointList::CountV)
    .function("get", &BND_NurbsSurfacePointList::GetControlPoint2)
    .function("getPoint", &BND_NurbsSurfacePointList::GetPoint)
    .function("set", &BND_NurbsSurfacePointList::SetControlPoint2)
    .function("makeRational", &BND_NurbsSurfacePointList::MakeRational)
    .function("makeNonRational", &BND_NurbsSurfacePointList::MakeNonRational)
    ;

  class_<BND_NurbsSurface, base<BND_Surface>>("NurbsSurface")
    .class_function("create", &BND_NurbsSurface::Create, allow_raw_pointers())
    .class_function("createFromCone", &BND_NurbsSurface::CreateFromCone, allow_raw_pointers())
    .class_function("createFromSphere", &BND_NurbsSurface::CreateFromSphere, allow_raw_pointers())
    .class_function("createFromCylinder", &BND_NurbsSurface::CreateFromCylinder, allow_raw_pointers())
    .class_function("createRuledSurface", &BND_NurbsSurface::CreateRuledSurface, allow_raw_pointers())
    .property("isRational", &BND_NurbsSurface::IsRational)
    .function("makeRational", &BND_NurbsSurface::MakeRational)
    .function("makeNonRational", &BND_NurbsSurface::MakeNonRational)
    .function("increaseDegreeU", &BND_NurbsSurface::IncreaseDegreeU)
    .function("increaseDegreeV", &BND_NurbsSurface::IncreaseDegreeV)
    .property("orderU", &BND_NurbsSurface::OrderU)
    .property("orderV", &BND_NurbsSurface::OrderV)
    .function("knotsU", &BND_NurbsSurface::KnotsU)
    .function("knotsV", &BND_NurbsSurface::KnotsV)
    .function("points", &BND_NurbsSurface::Points, allow_raw_pointers())
    ;
}
#endif
