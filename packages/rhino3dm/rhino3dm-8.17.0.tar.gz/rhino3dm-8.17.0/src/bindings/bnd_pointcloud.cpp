#include "bindings.h"

#if defined(ON_WASM_COMPILE)
template<typename T>
std::vector<T> Tuple_To_Vector(BND_TUPLE array) 
{
  return emscripten::vecFromJSArray<T>(array);
}
#endif

static void ON_PointCloud_FixPointCloud(ON_PointCloud* pPointCloud, bool ensureNormals, bool ensureColors, bool ensureHidden, bool ensureValues)
{
  if (pPointCloud)
  {
    int pointCount = pPointCloud->m_P.Count();

    if ((pPointCloud->m_N.Count() > 0) || ensureNormals)
    {
      if (pPointCloud->m_N.Count() != pointCount)
      {
        pPointCloud->m_N.Reserve(pointCount);
        pPointCloud->m_N.SetCount(pointCount);
      }
    }

    if ((pPointCloud->m_C.Count() > 0) || ensureColors)
    {
      if (pPointCloud->m_C.Count() != pointCount)
      {
        pPointCloud->m_C.Reserve(pointCount);
        pPointCloud->m_C.SetCount(pointCount);
      }
    }

    if ((pPointCloud->m_H.Count() > 0) || ensureHidden)
    {
      if (pPointCloud->m_H.Count() != pointCount)
      {
        pPointCloud->m_H.Reserve(pointCount);
        pPointCloud->m_H.SetCount(pointCount);
      }
    }

    if ((pPointCloud->m_V.Count() > 0) || ensureValues)
    {
      if (pPointCloud->m_V.Count() != pointCount)
      {
        pPointCloud->m_V.Reserve(pointCount);
        pPointCloud->m_V.SetCount(pointCount);
      }
    }

  }
}

BND_PointCloudItem::BND_PointCloudItem(int index, ON_PointCloud* pointcloud, const ON_ModelComponentReference& compref)
{
  m_index = index;
  m_component_reference = compref;
  m_pointcloud = pointcloud;
}

void BND_PointCloudItem::SetLocation(const ON_3dPoint& pt)
{
  m_pointcloud->m_P[m_index] = pt;
  m_pointcloud->InvalidateBoundingBox();
}

ON_3dVector BND_PointCloudItem::GetNormal() const
{
  if( m_index>=0 && m_index<m_pointcloud->m_N.Count())
    return m_pointcloud->m_N[m_index];
  return ON_3dVector::UnsetVector;
}

void BND_PointCloudItem::SetNormal(const ON_3dVector& v)
{
  if((m_index >= 0) && (m_index < m_pointcloud->m_P.Count()))
  {
    ON_PointCloud_FixPointCloud(m_pointcloud, true, false, false, false);
    m_pointcloud->m_N[m_index] = v;
  }
}

BND_Color BND_PointCloudItem::GetColor() const
{
  if (m_index >= 0 && m_index < m_pointcloud->m_C.Count())
    return ON_Color_to_Binding(m_pointcloud->m_C[m_index]);
  return ON_Color_to_Binding(ON_Color::UnsetColor);
}

void BND_PointCloudItem::SetColor(const BND_Color& color)
{
  if ((m_index >= 0) && (m_index < m_pointcloud->m_P.Count()))
  {
    ON_PointCloud_FixPointCloud(m_pointcloud, false, true, false, false);
    m_pointcloud->m_C[m_index] = Binding_to_ON_Color(color);
  }
}

double BND_PointCloudItem::GetValue() const
{
  if (m_index >= 0 && m_index < m_pointcloud->m_V.Count())
    return m_pointcloud->m_V[m_index];
  return ON_UNSET_VALUE;
}

void BND_PointCloudItem::SetValue(double value)
{
  if ((m_index >= 0) && (m_index < m_pointcloud->m_V.Count()))
  {
    ON_PointCloud_FixPointCloud(m_pointcloud, false, true, false, false);
    m_pointcloud->m_V[m_index] = value;
  }
}

bool BND_PointCloudItem::GetHidden() const
{
  if (m_index >= 0 && m_index < m_pointcloud->m_H.Count())
    return m_pointcloud->m_H[m_index];
  return false;
}
void BND_PointCloudItem::SetHidden(bool b)
{
  if ((m_index >= 0) && (m_index < m_pointcloud->m_P.Count()))
  {
    ON_PointCloud_FixPointCloud(m_pointcloud, false, false, true, false);
    m_pointcloud->SetHiddenPointFlag(m_index, b);
  }
}


BND_PointCloud::BND_PointCloud()
{
  SetTrackedPointer(new ON_PointCloud(), nullptr);
}

BND_PointCloud::BND_PointCloud(ON_PointCloud* pointcloud, const ON_ModelComponentReference* compref)
{
  SetTrackedPointer(pointcloud, compref);
}

BND_PointCloud::BND_PointCloud(const std::vector<ON_3dPoint>& points)
{
  int count = (int)points.size();
  ON_PointCloud* pc = new ON_PointCloud(count);
  const ON_3dPoint* pts = points.data();
  pc->m_P.Append(count, pts);
  SetTrackedPointer(pc, nullptr);
}

BND_PointCloud::BND_PointCloud(const class BND_Point3dList& points)
{
  int count = points.GetCount();
  ON_PointCloud* pc = new ON_PointCloud(count);
  pc->m_P.Append(count, points.m_polyline.Array());
  SetTrackedPointer(pc, nullptr);
}

#if defined(ON_WASM_COMPILE)
BND_PointCloud::BND_PointCloud(emscripten::val points)
{

  ON_PointCloud* pc;
  int count;

  bool isArray = points.hasOwnProperty("length");
  if( isArray ) 
  {
    const std::vector<ON_3dPoint> array = emscripten::vecFromJSArray<ON_3dPoint>(points);
    count = (int)array.size();
    pc = new ON_PointCloud(count);
    const ON_3dPoint* pts = array.data();
    pc->m_P.Append(count, pts);
  }
  else
  {
    BND_Point3dList list = points.as<const BND_Point3dList&>();
    count = list.GetCount();
    pc = new ON_PointCloud(count);
    pc->m_P.Append(count, list.m_polyline.Array());
  }

  SetTrackedPointer(pc, nullptr);

}
#endif

void BND_PointCloud::SetTrackedPointer(ON_PointCloud* pointcloud, const ON_ModelComponentReference* compref)
{
  m_pointcloud = pointcloud;
  BND_GeometryBase::SetTrackedPointer(pointcloud, compref);
}


BND_PointCloudItem BND_PointCloud::GetItem(int index)
{
#if defined(ON_PYTHON_COMPILE)
  if (index < 0 || index >= m_pointcloud->PointCount())
    throw py::index_error();
#endif

  return BND_PointCloudItem(index, m_pointcloud, m_component_ref);
}

BND_PointCloudItem BND_PointCloud::AppendNew()
{
  Add1(ON_3dPoint::Origin);
  int index = m_pointcloud->m_P.Count() - 1;
  return BND_PointCloudItem(index, m_pointcloud, m_component_ref);
}

BND_PointCloudItem BND_PointCloud::InsertNew(int index)
{
  Insert1(index, ON_3dPoint::Origin);
  return BND_PointCloudItem(index, m_pointcloud, m_component_ref);
}

void BND_PointCloud::Merge(const BND_PointCloud& other)
{
  bool ensureNormals = (other.m_pointcloud->m_N.Count() > 0);
  bool ensureColors = (other.m_pointcloud->m_C.Count() > 0);
  bool ensureHidden = (other.m_pointcloud->m_H.Count() > 0);
  bool ensureValues= (other.m_pointcloud->m_V.Count() > 0);

  ON_PointCloud_FixPointCloud(m_pointcloud, ensureNormals, ensureColors, ensureHidden, ensureValues);

  // Merge points.
  int count = other.m_pointcloud->m_P.Count();
  if (other.m_pointcloud->m_P.Count() > 0)
    m_pointcloud->m_P.Append(count, other.m_pointcloud->m_P.Array());


  // Merge normals.
  count = other.m_pointcloud->m_N.Count();
  if (count > 0)
    m_pointcloud->m_N.Append(count, other.m_pointcloud->m_N.Array());


  // Merge color.
  count = other.m_pointcloud->m_C.Count();
  if (count > 0)
    m_pointcloud->m_C.Append(count, other.m_pointcloud->m_C.Array());


  // Merge hidden.
  count = other.m_pointcloud->m_H.Count();
  if (count > 0)
  {
    m_pointcloud->m_H.Append(count, other.m_pointcloud->m_H.Array());
    m_pointcloud->m_hidden_count = 0;
    count = m_pointcloud->m_H.Count();
    for (int i = 0; i < count; i++)
    {
      if (m_pointcloud->m_H[i])
        m_pointcloud->m_hidden_count++;
    }
  }

  ON_PointCloud_FixPointCloud(m_pointcloud, false, false, false, false);
  m_pointcloud->InvalidateBoundingBox();
}

void BND_PointCloud::Add1(ON_3dPoint point)
{
  m_pointcloud->m_P.Append(point);
  ON_PointCloud_FixPointCloud(m_pointcloud, false, false, false, false);
  m_pointcloud->InvalidateBoundingBox();
}

void BND_PointCloud::Add2(ON_3dPoint point, ON_3dVector normal)
{
  m_pointcloud->m_P.Append(point);
  ON_PointCloud_FixPointCloud(m_pointcloud, true, false, false, false);
  m_pointcloud->InvalidateBoundingBox();

  if (m_pointcloud->m_N.Count() > 0)
  {
    int index = m_pointcloud->m_N.Count() - 1;
    m_pointcloud->m_N[index] = normal;
  }
}

void BND_PointCloud::Add3(ON_3dPoint point, BND_Color color)
{
  m_pointcloud->m_P.Append(point);
  ON_PointCloud_FixPointCloud(m_pointcloud, false, true, false, false);
  m_pointcloud->InvalidateBoundingBox();

  if (m_pointcloud->m_C.Count() > 0)
  {
    int index = m_pointcloud->m_C.Count() - 1;
    m_pointcloud->m_C[index] = Binding_to_ON_Color(color);
  }
}

void BND_PointCloud::Add4(ON_3dPoint point, ON_3dVector normal, BND_Color color)
{
  m_pointcloud->m_P.Append(point);
  ON_PointCloud_FixPointCloud(m_pointcloud, true, true, false, false);
  m_pointcloud->InvalidateBoundingBox();

  if (m_pointcloud->m_N.Count() > 0)
  {
    int index = m_pointcloud->m_N.Count() - 1;
    m_pointcloud->m_N[index] = normal;
  }

  if (m_pointcloud->m_C.Count() > 0)
  {
    int index = m_pointcloud->m_C.Count() - 1;
    m_pointcloud->m_C[index] = Binding_to_ON_Color(color);
  }
}

void BND_PointCloud::Add5(ON_3dPoint point, double value)
{
  m_pointcloud->m_P.Append(point);
  ON_PointCloud_FixPointCloud(m_pointcloud, false, false, false, true);
  m_pointcloud->InvalidateBoundingBox();

  if (m_pointcloud->m_V.Count() > 0)
  {
    int index = m_pointcloud->m_V.Count() - 1;
    m_pointcloud->m_V[index] = value;
  }
}

void BND_PointCloud::Add6(ON_3dPoint point, ON_3dVector normal, BND_Color color, double value)
{
  m_pointcloud->m_P.Append(point);
  ON_PointCloud_FixPointCloud(m_pointcloud, true, true, false, true);
  m_pointcloud->InvalidateBoundingBox();

  if (m_pointcloud->m_N.Count() > 0)
  {
    int index = m_pointcloud->m_N.Count() - 1;
    m_pointcloud->m_N[index] = normal;
  }

  if (m_pointcloud->m_C.Count() > 0)
  {
    int index = m_pointcloud->m_C.Count() - 1;
    m_pointcloud->m_C[index] = Binding_to_ON_Color(color);
  }

  if (m_pointcloud->m_V.Count() > 0)
  {
    int index = m_pointcloud->m_V.Count() - 1;
    m_pointcloud->m_V[index] = value;
  }
}

void BND_PointCloud::AddRangePoints(const std::vector<ON_3dPoint>& points)
{
  int count = (int)points.size();
  if (count > 0)
  {
    m_pointcloud->m_P.Append(count, points.data());
    ON_PointCloud_FixPointCloud(m_pointcloud, false, false, false, false);
    m_pointcloud->InvalidateBoundingBox();
  }
}

void BND_PointCloud::AddRangePointsNormals(const std::vector<ON_3dPoint>& points, const std::vector<ON_3dVector>& normals)
{
  if (points.size() != normals.size())
    return;
  int count = (int)points.size();
  if (count > 0)
  {
    m_pointcloud->m_P.Append(count, points.data());
    m_pointcloud->m_N.Append(count, normals.data());
    ON_PointCloud_FixPointCloud(m_pointcloud, false, false, false, false);
    m_pointcloud->InvalidateBoundingBox();
  }
}

void BND_PointCloud::AddRangePointsColors(const std::vector<ON_3dPoint>& points, const std::vector<BND_Color>& colors)
{
  if (points.size() != colors.size())
    return;
  int count = (int)points.size();
  if (count > 0)
  {
    m_pointcloud->m_P.Append(count, points.data());
    for (int i = 0; i < count; i++)
    {
      ON_Color c = Binding_to_ON_Color(colors[i]);
      m_pointcloud->m_C.Append(c);
    }
    ON_PointCloud_FixPointCloud(m_pointcloud, false, true, false, false);
    m_pointcloud->InvalidateBoundingBox();
  }
}

void BND_PointCloud::AddRangePointsValues(const std::vector<ON_3dPoint>& points, const std::vector<double>& values)
{
  if (points.size() != values.size())
    return;
  int count = (int)points.size();
  const ON_3dPoint* _points = points.data();
  const double* _values= values.data();
  if (count > 0)
  {
    m_pointcloud->m_P.Append(count, _points);
    m_pointcloud->m_V.Append(count, _values);
    ON_PointCloud_FixPointCloud(m_pointcloud, false, false, false, false);
    m_pointcloud->InvalidateBoundingBox();
  }
}

void BND_PointCloud::AddRangePointsNormalsColors(const std::vector<ON_3dPoint>& points, const std::vector<ON_3dVector>& normals, const std::vector<BND_Color>& colors)
{
  if (points.size() != normals.size() || points.size() != colors.size())
    return;
  int count = (int)points.size();

  if (count > 0)
  {
    m_pointcloud->m_P.Append(count, points.data());
    m_pointcloud->m_N.Append(count, normals.data());

    for (int i = 0; i < count; i++)
    {
      ON_Color c = Binding_to_ON_Color(colors[i]);
      m_pointcloud->m_C.Append(c);
    }
    ON_PointCloud_FixPointCloud(m_pointcloud, true, true, false, false);
    m_pointcloud->InvalidateBoundingBox();
  }
}

void BND_PointCloud::AddRangePointsNormalsColorsValues(const std::vector<ON_3dPoint>& points, const std::vector<ON_3dVector>& normals, const std::vector<BND_Color>& colors, const std::vector<double>& values)
{
  if (points.size() != normals.size() || points.size() != colors.size() != values.size())
    return;
  int count = (int)points.size();

  if (count > 0)
  {
    m_pointcloud->m_P.Append(count, points.data());
    m_pointcloud->m_N.Append(count, normals.data());
    m_pointcloud->m_V.Append(count, values.data());

    for (int i = 0; i < count; i++)
    {
      ON_Color c = Binding_to_ON_Color(colors[i]);
      m_pointcloud->m_C.Append(c);
    }
    ON_PointCloud_FixPointCloud(m_pointcloud, true, true, false, true);
    m_pointcloud->InvalidateBoundingBox();
  }
}

void BND_PointCloud::InsertRangePoints(int index, const std::vector<ON_3dPoint>& points)
{
  int count = (int)points.size();
  if (index >= 0 && (index <= m_pointcloud->m_P.Count()) && count > 0)
  {
    if (index == m_pointcloud->m_P.Count())
    {
      AddRangePoints(points);
      return;
    }

    int oldcount = m_pointcloud->m_P.Count();
    int newcount = oldcount + count;
    m_pointcloud->m_P.Reserve(newcount);
    ON_PointCloud_FixPointCloud(m_pointcloud, false, false, false, false);

    m_pointcloud->m_P.SetCount(newcount);
    ON_3dPoint* pPoints = m_pointcloud->m_P.Array();
    const ON_3dPoint* pSource = pPoints + index;
    ON_3dPoint* pDest = pPoints + oldcount;
    ::memcpy(pDest, pSource, (oldcount - index) * sizeof(ON_3dPoint));

    bool insertNormals = (m_pointcloud->m_N.Count() > 0);
    bool insertColors = (m_pointcloud->m_C.Count() > 0);
    bool insertHiddenFlags = (m_pointcloud->m_H.Count() > 0);

    for (int i = 0; i < count; i++)
    {
      m_pointcloud->m_P[index + i] = points[i];
      if (insertNormals)
        m_pointcloud->m_N.Insert(index + i, ON_3dVector(0, 0, 0));
      if (insertColors)
        m_pointcloud->m_C.Insert(index + i, ON_Color(0, 0, 0));
      if (insertHiddenFlags)
        m_pointcloud->m_H.Insert(index + i, false);
    }
    ON_PointCloud_FixPointCloud(m_pointcloud, false, false, false, false);
    m_pointcloud->InvalidateBoundingBox();
  }
}

#if defined(ON_WASM_COMPILE)

void BND_PointCloud::AddRange1(BND_TUPLE points)
{
  //AddRangePoints( tuple_to_vector3dPoint( points ) );
  AddRangePoints( Tuple_To_Vector<ON_3dPoint>( points ) );
}

void BND_PointCloud::AddRange2(BND_TUPLE points, BND_TUPLE normals)
{
  //AddRangePointsNormals( tuple_to_vector3dPoint(points), tuple_to_vector3dVector(normals) );
  AddRangePointsNormals( Tuple_To_Vector<ON_3dPoint>(points), Tuple_To_Vector<ON_3dVector>(normals) );
}

void BND_PointCloud::AddRange3(BND_TUPLE points, BND_TUPLE colors)
{
  //AddRangePointsColors( tuple_to_vector3dPoint(points), tuple_to_vectorColor(colors) );
  AddRangePointsColors( Tuple_To_Vector<ON_3dPoint>(points), Tuple_To_Vector<BND_Color>(colors) );
}

void BND_PointCloud::AddRange4(BND_TUPLE points, BND_TUPLE values)
{
  AddRangePointsValues( Tuple_To_Vector<ON_3dPoint>(points), Tuple_To_Vector<double>(values) );
}

void BND_PointCloud::AddRange5(BND_TUPLE points, BND_TUPLE normals, BND_TUPLE colors)
{
  AddRangePointsNormalsColors( Tuple_To_Vector<ON_3dPoint>(points), Tuple_To_Vector<ON_3dVector>(normals), Tuple_To_Vector<BND_Color>(colors) );
}

void BND_PointCloud::AddRange6(BND_TUPLE points, BND_TUPLE normals, BND_TUPLE colors, BND_TUPLE values)
{
  AddRangePointsNormalsColorsValues( Tuple_To_Vector<ON_3dPoint>(points), Tuple_To_Vector<ON_3dVector>(normals), Tuple_To_Vector<BND_Color>(colors), Tuple_To_Vector<double>(values) );
}

void BND_PointCloud::InsertRange(int index, BND_TUPLE points )
{
  InsertRangePoints( index, Tuple_To_Vector<ON_3dPoint>(points) );
}

#endif

void BND_PointCloud::Insert1(int index, const ON_3dPoint& point)
{
  if (index >= 0)
  {
    m_pointcloud->m_P.Insert(index, point);
    ON_PointCloud_FixPointCloud(m_pointcloud, false, false, false, false);
    m_pointcloud->InvalidateBoundingBox();
  }
}

void BND_PointCloud::Insert2(int index, const ON_3dPoint& point, const ON_3dVector& normal)
{
  m_pointcloud->m_P.Insert(index, point);
  ON_PointCloud_FixPointCloud(m_pointcloud, true, false, false, false);
  m_pointcloud->InvalidateBoundingBox();

  if (m_pointcloud->m_N.Count() > index)
  {
    m_pointcloud->m_N[index] = normal;
  }
}

void BND_PointCloud::Insert3(int index, const ON_3dPoint& point, const BND_Color& color)
{
  if (index >= 0)
  {
    m_pointcloud->m_P.Insert(index, point);
    ON_PointCloud_FixPointCloud(m_pointcloud, false, true, false, false);
    m_pointcloud->InvalidateBoundingBox();

    if (m_pointcloud->m_C.Count() > index)
      m_pointcloud->m_C[index] = Binding_to_ON_Color(color);
  }
}

void BND_PointCloud::Insert4(int index, const ON_3dPoint& point, const ON_3dVector& normal, const BND_Color& color)
{
  if (index >= 0)
  {
    m_pointcloud->m_P.Insert(index, point);
    ON_PointCloud_FixPointCloud(m_pointcloud, true, true, false, false);
    m_pointcloud->InvalidateBoundingBox();

    if (m_pointcloud->m_N.Count() > index)
    {
      m_pointcloud->m_N[index] = normal;
    }
    if (m_pointcloud->m_C.Count() > index)
    {
      m_pointcloud->m_C[index] = Binding_to_ON_Color(color);
    }
  }
}

void BND_PointCloud::Insert5(int index, const ON_3dPoint& point, const double& value)
{
  m_pointcloud->m_P.Insert(index, point);
  ON_PointCloud_FixPointCloud(m_pointcloud, false, false, false, true);
  m_pointcloud->InvalidateBoundingBox();

  if (m_pointcloud->m_V.Count() > index)
  {
    m_pointcloud->m_V[index] = value;
  }
}

void BND_PointCloud::Insert6(int index, const ON_3dPoint& point, const ON_3dVector& normal, const BND_Color& color, const double& value)
{
  if (index >= 0)
  {
    m_pointcloud->m_P.Insert(index, point);
    ON_PointCloud_FixPointCloud(m_pointcloud, true, true, false, true);
    m_pointcloud->InvalidateBoundingBox();

    if (m_pointcloud->m_N.Count() > index)
    {
      m_pointcloud->m_N[index] = normal;
    }
    if (m_pointcloud->m_C.Count() > index)
    {
      m_pointcloud->m_C[index] = Binding_to_ON_Color(color);
    }
    if (m_pointcloud->m_V.Count() > index)
    {
      m_pointcloud->m_V[index] = value;
    }
  }
}

void BND_PointCloud::RemoveAt(int index)
{
  if (index >= 0 && index < m_pointcloud->m_P.Count())
  {
    int oldCount = m_pointcloud->m_P.Count();
    m_pointcloud->m_P.Remove(index);
    if (oldCount == m_pointcloud->m_C.Count())
      m_pointcloud->m_C.Remove(index);

    if (oldCount == m_pointcloud->m_N.Count())
      m_pointcloud->m_N.Remove(index);

    if (oldCount == m_pointcloud->m_H.Count())
    {
      bool was_hidden = m_pointcloud->m_H[index];
      m_pointcloud->m_H.Remove(index);
      if (was_hidden)
      {
        m_pointcloud->m_hidden_count = 0;
        int count = m_pointcloud->m_H.Count();
        for (int i = 0; i < count; i++)
        {
          if (m_pointcloud->m_H[i])
            m_pointcloud->m_hidden_count++;
        }
      }
    }

    m_pointcloud->InvalidateBoundingBox();
  }
}

BND_TUPLE BND_PointCloud::GetPoints() const
{

  int count = m_pointcloud->m_P.Count();
  if( count > 0) {
    BND_TUPLE rc = CreateTuple(count);
    for (int i = 0; i < count; i++)
      SetTuple(rc, i, m_pointcloud->m_P[i]);

    return rc;
  }

  return NullTuple();
}

std::vector<ON_3dPoint> BND_PointCloud::GetPoints2() const
{
  std::vector<ON_3dPoint> rc;
  int count = m_pointcloud->m_P.Count();
  rc.reserve(count);
  for (int i = 0; i < count; i++)
    rc.push_back(m_pointcloud->m_P[i]);
    
  return rc;
}

ON_3dPoint BND_PointCloud::PointAt(int index) const
{
  if (index >= 0 && index < m_pointcloud->m_P.Count())
    return m_pointcloud->m_P[index];
  return ON_3dPoint::UnsetPoint;
}

BND_TUPLE BND_PointCloud::GetNormals() const
{

  if (m_pointcloud->HasPointNormals())
  {

    int count = m_pointcloud->m_N.Count();
    BND_TUPLE rc = CreateTuple(count);
    for (int i = 0; i < count; i++)
      SetTuple(rc, i, m_pointcloud->m_N[i]);

    return rc;
  }
  return NullTuple();
}

std::vector<ON_3dVector> BND_PointCloud::GetNormals2() const
{
  if (m_pointcloud->HasPointNormals())
  {
    std::vector<ON_3dVector> rc;
    int count = m_pointcloud->m_N.Count();
    rc.reserve(count);
    for (int i = 0; i < count; i++)
      rc.push_back(m_pointcloud->m_N[i]);

    return rc;
  }
  return std::vector<ON_3dVector>();
}

BND_TUPLE BND_PointCloud::GetColors() const
{

  if( m_pointcloud->HasPointColors() ) {

    int count = m_pointcloud->m_C.Count();
    BND_TUPLE rc = CreateTuple(count);
    for (int i = 0; i < count; i++)
      SetTuple(rc, i, ON_Color_to_Binding(m_pointcloud->m_C[i]));

    return rc;
  }

  return NullTuple();
  
}

std::vector<BND_Color> BND_PointCloud::GetColors2() const
{
  if (m_pointcloud->HasPointColors())
  {
    std::vector<BND_Color> rc;
    int count = m_pointcloud->m_C.Count();
    rc.reserve(count);
    for (int i = 0; i < count; i++)
      rc.push_back(ON_Color_to_Binding(m_pointcloud->m_C[i]));

    return rc;
  }
  return std::vector<BND_Color>();
}

BND_TUPLE BND_PointCloud::GetValues() const
{

  if( m_pointcloud->HasPointValues() ) {

    int count = m_pointcloud->m_V.Count();
    BND_TUPLE rc = CreateTuple(count);
    for (int i = 0; i < count; i++)
      SetTuple(rc, i, m_pointcloud->m_V[i]);

    return rc;
  }

  return NullTuple();
  
}

std::vector<double> BND_PointCloud::GetValues2() const
{
  if (m_pointcloud->HasPointValues())
  {
    std::vector<double> rc;
    int count = m_pointcloud->m_V.Count();
    rc.reserve(count);
    for (int i = 0; i < count; i++)
      rc.push_back(m_pointcloud->m_V[i]);

    return rc;
  }
  return std::vector<double>();
}

int BND_PointCloud::ClosestPoint(const ON_3dPoint& testPoint)
{
  int index = -1;
  if ( m_pointcloud->GetClosestPoint(testPoint, &index) )
      return index;
  return -1;
}

#if defined(ON_WASM_COMPILE)


BND_DICT BND_PointCloud::ToThreejsJSON() const
{
  ON_PointCloud* p_pointcloud = m_pointcloud;

  emscripten::val attributes(emscripten::val::object());

  // positions
  emscripten::val position(emscripten::val::object());
  position.set("itemSize", 3);
  position.set("type", "Float32Array");
  emscripten::val positionList(emscripten::val::array());
  for (int i = 0; i < p_pointcloud->m_P.Count(); i++)
  {
    positionList.set(i * 3, p_pointcloud->m_P[i].x);
    positionList.set(i * 3+1, p_pointcloud->m_P[i].y);
    positionList.set(i * 3+2, p_pointcloud->m_P[i].z);
  }
  position.set("array", positionList);
  attributes.set("position", position);

  //colors
  if (p_pointcloud->HasPointColors())
  {
    emscripten::val colors(emscripten::val::object());
    colors.set("itemSize", 3);
    colors.set("type", "Float32Array");
    emscripten::val colorList(emscripten::val::array());
    for (int i = 0; i < p_pointcloud->m_C.Count(); i++)
    {
      colorList.set(i * 3, p_pointcloud->m_C[i].Red() / 255.0);
      colorList.set(i * 3 + 1, p_pointcloud->m_C[i].Green() / 255.0);
      colorList.set(i * 3 + 2, p_pointcloud->m_C[i].Blue() / 255.0);
    }
    colors.set("array", colorList);
    attributes.set("color",colors);
  }

  if (m_pointcloud->HasPointNormals())
  {
    emscripten::val normal(emscripten::val::object());
    normal.set("itemSize", 3);
    normal.set("type", "Float32Array");
    emscripten::val normalList(emscripten::val::array());
    for (int i = 0; i < p_pointcloud->m_N.Count(); i++)
    {
      normalList.set(i * 3, p_pointcloud->m_N[i].x);
      normalList.set(i * 3 + 1, p_pointcloud->m_N[i].y);
      normalList.set(i * 3 + 2, p_pointcloud->m_N[i].z);
    }
    normal.set("array", normalList);
    attributes.set("normal", normal);
  }

  emscripten::val data(emscripten::val::object());
  data.set("attributes", attributes);

  emscripten::val rc(emscripten::val::object());
  rc.set("data", data);
  
  return rc;

}

BND_PointCloud* BND_PointCloud::CreateFromThreejsJSON(BND_DICT json)
{
   if (emscripten::val::undefined() == json["data"])
    return nullptr;
  emscripten::val attributes = json["data"]["attributes"];

  std::vector<double> position_array = emscripten::vecFromJSArray<double>(attributes["position"]["array"]);

  std::vector<double> normal_array;
  if (emscripten::val::undefined() != attributes["normal"])
  {
    normal_array = emscripten::vecFromJSArray<double>(attributes["normal"]["array"]);
  }

  std::vector<double> color_array;
  int colorChannels = 3; // could be RGB (3) or RGBA (4)
  if (emscripten::val::undefined() != attributes["color"])
  {
    color_array = emscripten::vecFromJSArray<double>(attributes["color"]["array"]);
    colorChannels = attributes["color"]["itemSize"].as<int>();
  }

  ON_PointCloud* pc = new ON_PointCloud();

  const int vertex_count = position_array.size() / 3;
  pc->m_P.SetCapacity(vertex_count);
  pc->m_P.SetCount(vertex_count);
  memcpy(pc->m_P.Array(), position_array.data(), sizeof(double) * position_array.size());

  const int normal_count = normal_array.size() / 3;
  pc->m_N.SetCapacity(normal_count);
  pc->m_N.SetCount(normal_count);
  memcpy(pc->m_N.Array(), normal_array.data(), sizeof(double) * normal_array.size());

  const int color_count = color_array.size() / colorChannels;
  pc->m_C.SetCapacity(color_count);
  pc->m_C.SetCount(color_count);
  std::transform(color_array.begin(), color_array.end(), color_array.begin(),[](double color) { return color * 255.0; });

  ON_Color* color_array_ptr = pc->m_C.Array();
  for (int i = 0; i < color_count; ++i) {
      int r = static_cast<int>(color_array[i * colorChannels]);
      int g = static_cast<int>(color_array[i * colorChannels + 1]);
      int b = static_cast<int>(color_array[i * colorChannels + 2]);
      if(colorChannels == 4)
      {
        int a = static_cast<int>(color_array[i * colorChannels + 3]);
        color_array_ptr[i] = ON_Color(r, g, b, 255-a);
      }
      else
        color_array_ptr[i] = ON_Color(r, g, b);
  }

  //memcpy(pc->m_C.Array(), color_array.data(), sizeof(ON_Color) * color_array.size());

  // ON_Xform rotation(1);
  // rotation.RotationZYX(0.0, 0.0, ON_PI / 2.0);
  // pc->Transform(rotation);

  return new BND_PointCloud(pc, nullptr);
}



#endif

//////////////////////////////////////////////////////////////////////////////

#if defined(ON_PYTHON_COMPILE)

void initPointCloudBindings(rh3dmpymodule& m)
{
  py::class_<BND_PointCloudItem>(m, "PointCloudItem")
    .def_property("Location", &BND_PointCloudItem::GetLocation, &BND_PointCloudItem::SetLocation)
    .def_property("X", &BND_PointCloudItem::GetX, &BND_PointCloudItem::SetX)
    .def_property("Y", &BND_PointCloudItem::GetY, &BND_PointCloudItem::SetY)
    .def_property("Z", &BND_PointCloudItem::GetZ, &BND_PointCloudItem::SetZ)
    .def_property("Normal", &BND_PointCloudItem::GetNormal, &BND_PointCloudItem::SetNormal)
    .def_property("Color", &BND_PointCloudItem::GetColor, &BND_PointCloudItem::SetColor)
    .def_property("Hidden", &BND_PointCloudItem::GetHidden, &BND_PointCloudItem::SetHidden)
    .def_property("Value", &BND_PointCloudItem::GetValue, &BND_PointCloudItem::SetValue)
    .def_property_readonly("Index", &BND_PointCloudItem::GetIndex)
    ;

  py::class_<BND_PointCloud, BND_GeometryBase>(m, "PointCloud")
    .def(py::init<>())
    .def(py::init<const std::vector<ON_3dPoint>&>())
    .def(py::init<const class BND_Point3dList&>())
    .def_property_readonly("Count", &BND_PointCloud::Count)
    .def("__len__", &BND_PointCloud::Count)
    .def("__getitem__", &BND_PointCloud::GetItem)
    .def_property_readonly("HiddenPointCount", &BND_PointCloud::HiddenPointCount)
    .def_property_readonly("ContainsColors", &BND_PointCloud::ContainsColors)
    .def_property_readonly("ContainsNormals", &BND_PointCloud::ContainsNormals)
    .def_property_readonly("ContainsValues", &BND_PointCloud::ContainsValues)
    .def_property_readonly("ContainsHiddenFlags", &BND_PointCloud::ContainsHiddenFlags)
    .def("ClearColors", &BND_PointCloud::ClearColors)
    .def("ClearNormals", &BND_PointCloud::ClearNormals)
    .def("ClearHiddenFlags", &BND_PointCloud::ClearHiddenFlags)
    .def("AppendNew", &BND_PointCloud::AppendNew)
    .def("InsertNew", &BND_PointCloud::InsertNew, py::arg("index"))
    .def("Merge", &BND_PointCloud::Merge, py::arg("other"))
    .def("Add", &BND_PointCloud::Add1, py::arg("point"))
    .def("Add", &BND_PointCloud::Add2, py::arg("point"), py::arg("normal"))
    .def("Add", &BND_PointCloud::Add3, py::arg("point"), py::arg("color"))
    .def("Add", &BND_PointCloud::Add4, py::arg("point"), py::arg("normal"), py::arg("color"))
    .def("Add", &BND_PointCloud::Add5, py::arg("point"), py::arg("value"))
    .def("Add", &BND_PointCloud::Add6, py::arg("point"), py::arg("normal"), py::arg("normal"), py::arg("value"))
    .def("AddRange", &BND_PointCloud::AddRangePoints, py::arg("points"))
    .def("AddRange", &BND_PointCloud::AddRangePointsNormals, py::arg("points"), py::arg("normals"))
    .def("AddRange", &BND_PointCloud::AddRangePointsColors, py::arg("points"), py::arg("colors"))
    .def("AddRange", &BND_PointCloud::AddRangePointsValues, py::arg("points"), py::arg("values"))
    .def("AddRange", &BND_PointCloud::AddRangePointsNormalsColors, py::arg("points"), py::arg("normals"), py::arg("colors"))
    .def("AddRange", &BND_PointCloud::AddRangePointsNormalsColorsValues, py::arg("points"), py::arg("normals"), py::arg("colors"), py::arg("values"))
    .def("Insert", &BND_PointCloud::Insert1, py::arg("index"), py::arg("point"))
    .def("Insert", &BND_PointCloud::Insert2, py::arg("index"), py::arg("point"), py::arg("normal"))
    .def("Insert", &BND_PointCloud::Insert3, py::arg("index"), py::arg("point"), py::arg("color"))
    .def("Insert", &BND_PointCloud::Insert4, py::arg("index"), py::arg("point"), py::arg("normal"), py::arg("color"))
    .def("Insert", &BND_PointCloud::Insert5, py::arg("index"), py::arg("point"), py::arg("value"))
    .def("Insert", &BND_PointCloud::Insert6, py::arg("index"), py::arg("point"), py::arg("normal"), py::arg("color"), py::arg("value"))
    .def("InsertRange", &BND_PointCloud::InsertRangePoints, py::arg("index"), py::arg("points"))
    .def("RemoveAt", &BND_PointCloud::RemoveAt, py::arg("index"))
    .def("GetPoints", &BND_PointCloud::GetPoints)
    .def("GetPoints2", &BND_PointCloud::GetPoints2)
    .def("PointAt", &BND_PointCloud::PointAt, py::arg("index"))
    .def("GetNormals", &BND_PointCloud::GetNormals)
    .def("GetNormals2", &BND_PointCloud::GetNormals2)
    .def("GetColors", &BND_PointCloud::GetColors)
    .def("GetColors2", &BND_PointCloud::GetColors2)
    .def("GetValues", &BND_PointCloud::GetValues)
    .def("GetValues2", &BND_PointCloud::GetValues2)
    .def("ClosestPoint", &BND_PointCloud::ClosestPoint, py::arg("testPoint"))
    ;
}

#endif

#if defined(ON_WASM_COMPILE)
using namespace emscripten;

void initPointCloudBindings(void*)
{
  class_<BND_PointCloudItem>("PointCloudItem")
    .property("location", &BND_PointCloudItem::GetLocation, &BND_PointCloudItem::SetLocation)
    .property("x", &BND_PointCloudItem::GetX, &BND_PointCloudItem::SetX)
    .property("y", &BND_PointCloudItem::GetY, &BND_PointCloudItem::SetY)
    .property("z", &BND_PointCloudItem::GetZ, &BND_PointCloudItem::SetZ)
    .property("normal", &BND_PointCloudItem::GetNormal, &BND_PointCloudItem::SetNormal)
    .property("color", &BND_PointCloudItem::GetColor, &BND_PointCloudItem::SetColor)
    .property("hidden", &BND_PointCloudItem::GetHidden, &BND_PointCloudItem::SetHidden)
    .property("value", &BND_PointCloudItem::GetValue, &BND_PointCloudItem::SetValue)
    .property("index", &BND_PointCloudItem::GetIndex)
    ;

  class_<BND_PointCloud, base<BND_GeometryBase>>("PointCloud")
    .constructor<>()
    .constructor<emscripten::val>()
    .property("count", &BND_PointCloud::Count)
    .property("hiddenPointCount", &BND_PointCloud::HiddenPointCount)
    .property("containsColors", &BND_PointCloud::ContainsColors)
    .property("containsNormals", &BND_PointCloud::ContainsNormals)
    .property("containsValues", &BND_PointCloud::ContainsValues)
    .property("containsHiddenFlags", &BND_PointCloud::ContainsHiddenFlags)
    .function("clearColors", &BND_PointCloud::ClearColors)
    .function("clearNormals", &BND_PointCloud::ClearNormals)
    .function("clearHiddenFlags", &BND_PointCloud::ClearHiddenFlags)
    .function("appendNew", &BND_PointCloud::AppendNew)
    .function("insertNew", &BND_PointCloud::InsertNew)
    .function("merge", &BND_PointCloud::Merge)
    
    .function("add", &BND_PointCloud::Add1)
    .function("addPointNormal", &BND_PointCloud::Add2)
    .function("addPointColor", &BND_PointCloud::Add3)
    .function("addPointNormalColor", &BND_PointCloud::Add4)
    .function("addPointValue", &BND_PointCloud::Add5)
    .function("addPointNormalColorValue", &BND_PointCloud::Add6)

    .function("addRangePoints", &BND_PointCloud::AddRange1)
    .function("addRangePointsNormals", &BND_PointCloud::AddRange2)
    .function("addRangePointsColors", &BND_PointCloud::AddRange3)
    .function("addRangePointsValues", &BND_PointCloud::AddRange4)
    .function("addRangePointsNormalsColors", &BND_PointCloud::AddRange5)
    .function("addRangePointsNormalsColorsValues", &BND_PointCloud::AddRange6)

    .function("insert", &BND_PointCloud::Insert1)
    .function("insertPointNormal", &BND_PointCloud::Insert2)
    .function("insertPointColor", &BND_PointCloud::Insert3)
    .function("insertPointNormalColor", &BND_PointCloud::Insert4)
    .function("insertPointValue", &BND_PointCloud::Insert5)
    .function("insertPointNormalColorValue", &BND_PointCloud::Insert6)

    .function("insertRange", &BND_PointCloud::InsertRange)

    .function("removeAt", &BND_PointCloud::RemoveAt)
    .function("getPoints", &BND_PointCloud::GetPoints)
    .function("pointAt", &BND_PointCloud::PointAt)
    .function("getNormals", &BND_PointCloud::GetNormals)
    .function("getColors", &BND_PointCloud::GetColors)
    .function("getValues", &BND_PointCloud::GetValues)
    .function("closestPoint", &BND_PointCloud::ClosestPoint)
    .function("toThreejsJSON", &BND_PointCloud::ToThreejsJSON)
    .class_function("createFromThreejsJSON", &BND_PointCloud::CreateFromThreejsJSON, allow_raw_pointers())
    ;
}
#endif
