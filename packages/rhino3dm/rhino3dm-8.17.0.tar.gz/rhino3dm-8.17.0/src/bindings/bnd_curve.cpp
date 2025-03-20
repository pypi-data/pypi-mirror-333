#include "bindings.h"




BND_Curve::BND_Curve()
{

}

BND_Curve::BND_Curve(ON_Curve* curve, const ON_ModelComponentReference* compref)
{
  SetTrackedPointer(curve, compref);
}

void BND_Curve::SetTrackedPointer(ON_Curve* curve, const ON_ModelComponentReference* compref)
{
  m_curve = curve;
  BND_GeometryBase::SetTrackedPointer(curve, compref);
}

BND_Curve* BND_Curve::CreateControlPointCurve1(const BND_Point3dList& points, int degree)
{
  int count = points.m_polyline.Count();
  if (count < 2)
    return nullptr;

  if (2 == count)
    return new BND_LineCurve(points.m_polyline[0], points.m_polyline[1]);

  if (1 == degree && count > 2)
    return new BND_PolylineCurve(points);

  return BND_NurbsCurve::Create1(false, degree, points);
}

BND_Curve* BND_Curve::CreateControlPointCurve2(const std::vector<ON_3dPoint>& points, int degree)
{
  BND_Point3dList list;
  for (int i = 0; i < points.size(); i++)
  {
    list.Add(points[i].x, points[i].y, points[i].z);
  }
  return CreateControlPointCurve1(list, degree);
}


#if defined(ON_WASM_COMPILE)
BND_Curve* BND_Curve::CreateControlPointCurve3(emscripten::val points, int degree)
{
  bool isArray = points.hasOwnProperty("length");
  if( isArray ) 
  {
    const std::vector<ON_3dPoint> array = emscripten::vecFromJSArray<ON_3dPoint>(points);
    return CreateControlPointCurve2( array, degree ); 
  }
  else
    return CreateControlPointCurve1( points.as<const BND_Point3dList&>(), degree ); 
}
#endif


void BND_Curve::SetDomain(const BND_Interval& i)
{
  m_curve->SetDomain(i.m_t0, i.m_t1);
}

BND_Interval BND_Curve::GetDomain() const
{
  return BND_Interval(m_curve->Domain());
}

BND_Polyline* BND_Curve::TryGetPolyline() const
{
  ON_SimpleArray<ON_3dPoint> pts;
  if (m_curve->IsPolyline(&pts) > 1)
  {
    BND_Polyline* rc = new BND_Polyline();
    rc->m_polyline = pts;
    return rc;
  }
  return nullptr;
}

BND_Arc* BND_Curve::TryGetArc(double tolerance) const
{
  ON_Arc arc;
  if (m_curve->IsArc(nullptr, &arc, tolerance))
  {
    BND_Arc* rc = new BND_Arc(arc);
    return rc;
  }
  return nullptr;
}

bool BND_Curve::IsCircle(double tolerance) const
{
  ON_Arc arc;
  if (m_curve->IsArc(nullptr, &arc, tolerance))
  {
    return arc.IsCircle();
  }
  return false;
}

BND_Circle* BND_Curve::TryGetCircle(double tolerance) const
{
  ON_Arc arc;
  if (m_curve->IsArc(nullptr, &arc, tolerance) && arc.IsCircle())
  {
    BND_Circle* rc = new BND_Circle(0);
    rc->m_circle = arc;
    return rc;
  }
  return nullptr;
}

BND_Ellipse* BND_Curve::TryGetEllipse(double tolerance) const
{
  ON_Ellipse ellipse;
  if (m_curve->IsEllipse(nullptr, &ellipse, tolerance))
  {
    BND_Ellipse* rc = new BND_Ellipse();
    rc->m_ellipse = ellipse;
    return rc;
  }
  return nullptr;
}

CurveOrientation BND_Curve::ClosedCurveOrientation() const
{
  if (m_curve)
  {
    int rc = ON_ClosedCurveOrientation(*m_curve, nullptr);
    if (1 == rc)
      return CurveOrientation::CounterClockwise;
    if (-1 == rc)
      return CurveOrientation::Clockwise;
  }
  return CurveOrientation::Undefined;
}

CurveOrientation BND_Curve::ClosedCurveOrientation3(BND_Plane plane) const
{
  if (m_curve)
  {
    ON_Plane pl = plane.ToOnPlane();
    int rc = ON_ClosedCurveOrientation(*m_curve, pl);
    if (1 == rc)
      return CurveOrientation::CounterClockwise;
    if (-1 == rc)
      return CurveOrientation::Clockwise;
  }
  return CurveOrientation::Undefined;
}


BND_TUPLE BND_Curve::FrameAt(double t) const
{
  ON_Plane plane;
  bool success = m_curve->FrameAt(t, plane);
#if defined(ON_PYTHON_COMPILE) && defined(NANOBIND)
  BND_TUPLE rc = py::make_tuple(success, BND_Plane::FromOnPlane(plane));
#else
  BND_TUPLE rc = CreateTuple(2);
  SetTuple(rc, 0, success);
  SetTuple(rc, 1, BND_Plane::FromOnPlane(plane));
#endif
  return rc;
}

BND_TUPLE BND_Curve::DerivativeAt(double t, int derivativeCount) const
{
  return DerivativeAt2(t, derivativeCount, CurveEvaluationSide::Default);
}

BND_TUPLE BND_Curve::DerivativeAt2(double t, int derivativeCount, CurveEvaluationSide side) const
{
  BND_TUPLE rc = CreateTuple(derivativeCount);
  ON_SimpleArray<ON_3dPoint> outVectors;
  outVectors.Reserve(derivativeCount + 1);
  if (m_curve->Evaluate(t, derivativeCount, 3, &outVectors.Array()->x, (int)side, nullptr))
  {
    outVectors.SetCount(derivativeCount + 1);
    for (int i = 0; i < outVectors.Count(); i++)
    {
      SetTuple(rc, i, outVectors[i]);
    }
  }
  return rc;
}
//TODO: CLEANUP
std::vector<ON_3dPoint> BND_Curve::DerivativeAt3(double t, int derivativeCount) const
{
  return DerivativeAt4(t, derivativeCount, CurveEvaluationSide::Default);
}

std::vector<ON_3dPoint> BND_Curve::DerivativeAt4(double t, int derivativeCount, CurveEvaluationSide side) const
{
  std::vector<ON_3dPoint> rc;
  ON_SimpleArray<ON_3dPoint> outVectors;
  outVectors.Reserve(derivativeCount + 1);
  if (m_curve->Evaluate(t, derivativeCount, 3, &outVectors.Array()->x, (int)side, nullptr))
  {
    outVectors.SetCount(derivativeCount + 1);
    rc.reserve(outVectors.Count());
    for (int i = 0; i < outVectors.Count(); i++)
    {
      rc.push_back(outVectors[i]);
    }
  }
  return rc;
}

BND_TUPLE BND_Curve::GetCurveParameterFromNurbsFormParameter(double nurbsParameter)
{
  double curve_t = 0;
  bool success = m_curve->GetCurveParameterFromNurbFormParameter(nurbsParameter, &curve_t);
#if defined(ON_PYTHON_COMPILE) && defined(NANOBIND)
  BND_TUPLE rc = py::make_tuple(success, curve_t);
#else
  BND_TUPLE rc = CreateTuple(2);
  SetTuple(rc, 0, success);
  SetTuple(rc, 1, curve_t);
#endif
  return rc;
}

BND_TUPLE BND_Curve::GetNurbsFormParameterFromCurveParameter(double curveParameter)
{
  double nurbs_t = 0;
  bool success = m_curve->GetNurbFormParameterFromCurveParameter(curveParameter, &nurbs_t);
#if defined(ON_PYTHON_COMPILE) && defined(NANOBIND)
  BND_TUPLE rc = py::make_tuple(success, nurbs_t);
#else
  BND_TUPLE rc = CreateTuple(2);
  SetTuple(rc, 0, success);
  SetTuple(rc, 1, nurbs_t);
#endif
  return rc;
}

BND_Curve* BND_Curve::Trim(double t0, double t1) const
{
  ON_Curve* crv = m_curve->DuplicateCurve();
  if (!crv->Trim(ON_Interval(t0, t1)))
  {
    delete crv;
    return nullptr;
  }
  BND_Curve* rc = dynamic_cast<BND_Curve*>(BND_CommonObject::CreateWrapper(crv, nullptr));
  return rc;
}

BND_TUPLE BND_Curve::Split(double t) const
{
  ON_Curve* left = nullptr;
  ON_Curve* right = nullptr;
  if (m_curve->Split(t, left, right))
  {
#if defined(ON_PYTHON_COMPILE) && defined(NANOBIND)
    BND_TUPLE rc = py::make_tuple(BND_CommonObject::CreateWrapper(left, nullptr), BND_CommonObject::CreateWrapper(right, nullptr));
#else
    BND_TUPLE rc = CreateTuple(2);
    SetTuple(rc, 0, BND_CommonObject::CreateWrapper(left, nullptr));
    SetTuple(rc, 1, BND_CommonObject::CreateWrapper(right, nullptr));
#endif
    return rc;
  }
  return NullTuple();

}


BND_NurbsCurve* BND_Curve::ToNurbsCurve() const
{
  ON_NurbsCurve* nc = m_curve->NurbsCurve();
  if (nullptr == nc)
    return nullptr;
  return new BND_NurbsCurve(nc, nullptr);
}

BND_NurbsCurve* BND_Curve::ToNurbsCurve2(BND_Interval subdomain) const
{
  ON_Interval _subdomain(subdomain.m_t0, subdomain.m_t1);
  ON_NurbsCurve* nc = m_curve->NurbsCurve(nullptr, 0, &_subdomain);
  if (nullptr == nc)
    return nullptr;
  return new BND_NurbsCurve(nc, nullptr);
}


#if defined(ON_PYTHON_COMPILE)

void initCurveBindings(rh3dmpymodule& m)
{
  py::enum_<CurveEvaluationSide>(m, "CurveEvaluationSide")
    .value("Default", CurveEvaluationSide::Default)
    .value("Below", CurveEvaluationSide::Below)
    .value("Above", CurveEvaluationSide::Above)
    ;

  py::enum_<BlendContinuity>(m, "BlendContinuity")
    .value("Position", BlendContinuity::Position)
    .value("Tangency", BlendContinuity::Tangency)
    .value("Curvature", BlendContinuity::Curvature)
    ;

  py::enum_<CurveOffsetCornerStyle>(m, "CurveOffsetCornerStyle")
    .value("None", CurveOffsetCornerStyle::None)
    .value("Sharp", CurveOffsetCornerStyle::Sharp)
    .value("Round", CurveOffsetCornerStyle::Round)
    .value("Smooth", CurveOffsetCornerStyle::Smooth)
    .value("Chamfer", CurveOffsetCornerStyle::Chamfer)
    ;

  py::enum_<CurveKnotStyle>(m, "CurveKnotStyle")
    .value("Uniform", CurveKnotStyle::Uniform)
    .value("Chord", CurveKnotStyle::Chord)
    .value("ChordSquareRoot", CurveKnotStyle::ChordSquareRoot)
    .value("UniformPeriodic", CurveKnotStyle::UniformPeriodic)
    .value("ChordPeriodic", CurveKnotStyle::ChordPeriodic)
    .value("ChordSquareRootPeriodic", CurveKnotStyle::ChordSquareRootPeriodic)
    ;

  py::enum_<CurveOrientation>(m, "CurveOrientation")
    .value("Undefined", CurveOrientation::Undefined)
    .value("Clockwise", CurveOrientation::Clockwise)
    .value("CounterClockwise", CurveOrientation::CounterClockwise)
    ;

  py::enum_<PointContainment>(m, "PointContainment")
    .value("Unset", PointContainment::Unset)
    .value("Inside", PointContainment::Inside)
    .value("Outside", PointContainment::Outside)
    .value("Coincident", PointContainment::Coincident)
    ;

  py::enum_<RegionContainment>(m, "RegionContainment")
    .value("Disjoint", RegionContainment::Disjoint)
    .value("MutualIntersection", RegionContainment::MutualIntersection)
    .value("AInsideB", RegionContainment::AInsideB)
    .value("BInsideA", RegionContainment::BInsideA)
    ;

  py::enum_<CurveExtensionStyle>(m, "CurveExtensionStyle")
    .value("Line", CurveExtensionStyle::Line)
    .value("Arc", CurveExtensionStyle::Arc)
    .value("Smooth", CurveExtensionStyle::Smooth)
    ;

  py::class_<BND_Curve, BND_GeometryBase>(m, "Curve")
    .def_static("CreateControlPointCurve", &BND_Curve::CreateControlPointCurve2, py::arg("points"), py::arg("degree")=3)
    .def_static("CreateControlPointCurve", &BND_Curve::CreateControlPointCurve1, py::arg("points"), py::arg("degree")=3)
    .def_property("Domain", &BND_Curve::GetDomain, &BND_Curve::SetDomain)
    .def_property_readonly("Dimension", &BND_GeometryBase::Dimension)
    .def("ChangeDimension", &BND_Curve::ChangeDimension, py::arg("desiredDimension"))
    .def_property_readonly("SpanCount", &BND_Curve::SpanCount)
    .def_property_readonly("Degree", &BND_Curve::Degree)
    .def("IsLinear", &BND_Curve::IsLinear, py::arg("tolerance")=ON_ZERO_TOLERANCE)
    .def("IsPolyline", &BND_Curve::IsPolyline)
    .def("TryGetPolyline", &BND_Curve::TryGetPolyline)
    .def("IsArc", &BND_Curve::IsArc, py::arg("tolerance")=ON_ZERO_TOLERANCE)
    .def("TryGetArc", &BND_Curve::TryGetArc, py::arg("tolerance")=ON_ZERO_TOLERANCE)
    .def("IsCircle", &BND_Curve::IsCircle, py::arg("tolerance")=ON_ZERO_TOLERANCE)
    .def("TryGetCircle", &BND_Curve::TryGetCircle, py::arg("tolerance")=ON_ZERO_TOLERANCE)
    .def("IsEllipse", &BND_Curve::IsEllipse, py::arg("tolerance")=ON_ZERO_TOLERANCE)
    .def("TryGetEllipse", &BND_Curve::TryGetEllipse, py::arg("tolerance")=ON_ZERO_TOLERANCE)
    .def("IsPlanar", &BND_Curve::IsPlanar, py::arg("tolerance")=ON_ZERO_TOLERANCE)
    .def("ChangeClosedCurveSeam", &BND_Curve::ChangeClosedCurveSeam, py::arg("t"))
    .def_property_readonly("IsClosed", &BND_Curve::IsClosed)
    .def_property_readonly("IsPeriodic", &BND_Curve::IsPeriodic)
    .def("IsClosable", &BND_Curve::IsClosable, py::arg("tolerance"), py::arg("minimumAbsoluteSize")=0, py::arg("minimumRelativeSize")=10)
    .def("Reverse", &BND_Curve::Reverse)
    .def("ClosedCurveOrientation", &BND_Curve::ClosedCurveOrientation)
    .def("ClosedCurveOrientation", &BND_Curve::ClosedCurveOrientation3, py::arg("plane"))
    .def("PointAt", &BND_Curve::PointAt, py::arg("t"))
    .def_property_readonly("PointAtStart", &BND_Curve::PointAtStart)
    .def_property_readonly("PointAtEnd", &BND_Curve::PointAtEnd)
    .def("SetStartPoint", &BND_Curve::SetStartPoint, py::arg("point"))
    .def("SetEndPoint", &BND_Curve::SetEndPoint, py::arg("point"))
    .def("TangentAt", &BND_Curve::TangentAt, py::arg("t"))
    .def_property_readonly("TangentAtStart", &BND_Curve::TangentAtStart)
    .def_property_readonly("TangentAtEnd", &BND_Curve::TangentAtEnd)
    .def("CurvatureAt", &BND_Curve::CurvatureAt, py::arg("t"))
    .def("FrameAt", &BND_Curve::FrameAt, py::arg("t"))
    //.def("DerivativeAt", &BND_Curve::DerivativeAt, py::arg("t"), py::arg("derivativeCount"))
    //.def("DerivativeAt", &BND_Curve::DerivativeAt2, py::arg("t"), py::arg("derivativeCount"), py::arg("side"))
    .def("DerivativeAt", &BND_Curve::DerivativeAt3, py::arg("t"), py::arg("derivativeCount"))
    .def("DerivativeAt", &BND_Curve::DerivativeAt4, py::arg("t"), py::arg("derivativeCount"), py::arg("side"))
    .def("GetCurveParameterFromNurbsFormParameter", &BND_Curve::GetCurveParameterFromNurbsFormParameter, py::arg("nurbsParameter"))
    .def("GetNurbsFormParameterFromCurveParameter", &BND_Curve::GetNurbsFormParameterFromCurveParameter, py::arg("curveParameter"))
    .def("Trim", &BND_Curve::Trim, py::arg("t0"), py::arg("t1"))
    .def("Split", &BND_Curve::Split, py::arg("t"))
    .def("ToNurbsCurve", &BND_Curve::ToNurbsCurve)
    .def("ToNurbsCurve", &BND_Curve::ToNurbsCurve2, py::arg("subdomain"))
    ;
}
#endif

#if defined(ON_WASM_COMPILE)
using namespace emscripten;

void initCurveBindings(void*)
{

  enum_<CurveEvaluationSide>("CurveEvaluationSide")
    .value("Default", CurveEvaluationSide::Default)
    .value("Below", CurveEvaluationSide::Below)
    .value("Above", CurveEvaluationSide::Above)
    ;

  enum_<BlendContinuity>("BlendContinuity")
    .value("Position", BlendContinuity::Position)
    .value("Tangency", BlendContinuity::Tangency)
    .value("Curvature", BlendContinuity::Curvature)
    ;

  enum_<CurveOffsetCornerStyle>("CurveOffsetCornerStyle")
    .value("None", CurveOffsetCornerStyle::None)
    .value("Sharp", CurveOffsetCornerStyle::Sharp)
    .value("Round", CurveOffsetCornerStyle::Round)
    .value("Smooth", CurveOffsetCornerStyle::Smooth)
    .value("Chamfer", CurveOffsetCornerStyle::Chamfer)
    ;

  enum_<CurveKnotStyle>("CurveKnotStyle")
    .value("Uniform", CurveKnotStyle::Uniform)
    .value("Chord", CurveKnotStyle::Chord)
    .value("ChordSquareRoot", CurveKnotStyle::ChordSquareRoot)
    .value("UniformPeriodic", CurveKnotStyle::UniformPeriodic)
    .value("ChordPeriodic", CurveKnotStyle::ChordPeriodic)
    .value("ChordSquareRootPeriodic", CurveKnotStyle::ChordSquareRootPeriodic)
    ;

  enum_<CurveOrientation>("CurveOrientation")
    .value("Undefined", CurveOrientation::Undefined)
    .value("Clockwise", CurveOrientation::Clockwise)
    .value("CounterClockwise", CurveOrientation::CounterClockwise)
    ;

  enum_<PointContainment>("PointContainment")
    .value("Unset", PointContainment::Unset)
    .value("Inside", PointContainment::Inside)
    .value("Outside", PointContainment::Outside)
    .value("Coincident", PointContainment::Coincident)
    ;

  enum_<RegionContainment>("RegionContainment")
    .value("Disjoint", RegionContainment::Disjoint)
    .value("MutualIntersection", RegionContainment::MutualIntersection)
    .value("AInsideB", RegionContainment::AInsideB)
    .value("BInsideA", RegionContainment::BInsideA)
    ;

  enum_<CurveExtensionStyle>("CurveExtensionStyle")
    .value("Line", CurveExtensionStyle::Line)
    .value("Arc", CurveExtensionStyle::Arc)
    .value("Smooth", CurveExtensionStyle::Smooth)
    ;

  class_<BND_Curve, base<BND_GeometryBase>>("Curve")
    .class_function("createControlPointCurve", &BND_Curve::CreateControlPointCurve3, allow_raw_pointers())
    .property("domain", &BND_Curve::GetDomain, &BND_Curve::SetDomain)
    .property("dimension", &BND_GeometryBase::Dimension)
    .function("changeDimension", &BND_Curve::ChangeDimension)
    .property("spanCount", &BND_Curve::SpanCount)
    .property("degree", &BND_Curve::Degree)
    .function("isLinear", &BND_Curve::IsLinear)
    .function("isPolyline", &BND_Curve::IsPolyline)
    .function("tryGetPolyline", &BND_Curve::TryGetPolyline, allow_raw_pointers())
    .function("isArc", &BND_Curve::IsArc)
    .function("tryGetArc", &BND_Curve::TryGetArc, allow_raw_pointers())
    .function("isCircle", &BND_Curve::IsCircle)
    .function("tryGetCircle", &BND_Curve::TryGetCircle, allow_raw_pointers())
    .function("isEllipse", &BND_Curve::IsEllipse)
    .function("isPlanar", &BND_Curve::IsPlanar)
    .function("changeClosedCurveSeam", &BND_Curve::ChangeClosedCurveSeam)
    .property("isClosed", &BND_Curve::IsClosed)
    .property("isPeriodic", &BND_Curve::IsPeriodic)
    .function("reverse", &BND_Curve::Reverse)
    .function("closedCurveOrientation", &BND_Curve::ClosedCurveOrientation)
    .function("closedCurveOrientationPlane", &BND_Curve::ClosedCurveOrientation3)
    .function("pointAt", &BND_Curve::PointAt)
    .property("pointAtStart", &BND_Curve::PointAtStart)
    .property("pointAtEnd", &BND_Curve::PointAtEnd)
    .function("setStartPoint", &BND_Curve::SetStartPoint)
    .function("setEndPoint", &BND_Curve::SetEndPoint)
    .function("tangentAt", &BND_Curve::TangentAt)
    .property("tangentAtStart", &BND_Curve::TangentAtStart)
    .property("tangentAtEnd", &BND_Curve::TangentAtEnd)
    .function("curvatureAt", &BND_Curve::CurvatureAt)
    .function("frameAt", &BND_Curve::FrameAt)
    .function("derivativeAt", &BND_Curve::DerivativeAt)
    .function("derivativeAtSide", &BND_Curve::DerivativeAt2)
    .function("getCurveParameterFromNurbsFormParameter", &BND_Curve::GetCurveParameterFromNurbsFormParameter)
    .function("getNurbsFormParameterFromCurveParameter", &BND_Curve::GetNurbsFormParameterFromCurveParameter)
    .function("trim", &BND_Curve::Trim, allow_raw_pointers())
    .function("split", &BND_Curve::Split, allow_raw_pointers())
    .function("toNurbsCurve", &BND_Curve::ToNurbsCurve, allow_raw_pointers())
    .function("toNurbsCurveSubDomain", &BND_Curve::ToNurbsCurve2, allow_raw_pointers())
    ;
}
#endif
