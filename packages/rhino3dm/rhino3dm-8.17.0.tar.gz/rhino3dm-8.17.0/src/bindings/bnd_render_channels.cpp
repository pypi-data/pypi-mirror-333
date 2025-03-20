
#include "bindings.h"

BND_File3dmRenderChannels::BND_File3dmRenderChannels()
{
  _rch = new ON_RenderChannels;
  _owned = true;
}

BND_File3dmRenderChannels::BND_File3dmRenderChannels(const BND_File3dmRenderChannels& rch)
{
   // see bnd_ground_plane.cpp for justification
  _rch = rch._rch;

  if (rch._owned)
  {
    // Tell the original owner that it no longer owns it.
    const_cast<BND_File3dmRenderChannels&>(rch)._owned = false;

    // This object now owns it instead.
    _owned = true;
  }

  // Old code makes an actual copy of the native object -- which means changes don't stick.
  //_rch = new ON_RenderChannels(*rch._rch);
  //_owned = true;
}

BND_File3dmRenderChannels::BND_File3dmRenderChannels(ON_RenderChannels* rch)
: _rch(rch)
{
}

BND_TUPLE BND_File3dmRenderChannels::GetCustomList() const
{
  ON_SimpleArray<ON_UUID> list;
  _rch->GetCustomList(list);

  const int count = list.Count();
  BND_TUPLE tuple = CreateTuple(count);
  for (int i = 0; i < count; i++)
  {
    SetTuple(tuple, i, ON_UUID_to_Binding(list[i]));
  }

  return tuple;
}

std::vector<BND_UUID> BND_File3dmRenderChannels::GetCustomList2() const
{
  ON_SimpleArray<ON_UUID> list;
  _rch->GetCustomList(list);

  const int count = list.Count();
  std::vector<BND_UUID> uuids;
  for (int i = 0; i < count; i++)
  {
    uuids.push_back(ON_UUID_to_Binding(list[i]));
  }

  return uuids;
}

void BND_File3dmRenderChannels::SetCustomList(BND_TUPLE tuple)
{
  ON_SimpleArray<ON_UUID> list;

  // John C - compiler complaining here. are you trying to use BND_Tuple?
  /*
  for (auto elem: tuple)
  {
    list.Append(Binding_to_ON_UUID(elem.cast<BND_UUID>()));
  }

  _rch->SetCustomList(list);
  */
}

//#endif

//////////////////////////////////////////////////////////////////////////////

#if defined(ON_PYTHON_COMPILE)

void initRenderChannelsBindings(rh3dmpymodule& m)
{
  py::class_<BND_File3dmRenderChannels>(m, "RenderChannels")
    .def(py::init<>())
    .def(py::init<const BND_File3dmRenderChannels&>(), py::arg("other"))
    .def_property("Mode", &BND_File3dmRenderChannels::GetMode, &BND_File3dmRenderChannels::SetMode)
    .def_property("CustomIds", &BND_File3dmRenderChannels::GetCustomList, &BND_File3dmRenderChannels::SetCustomList)
    .def_property_readonly("CustomIds", &BND_File3dmRenderChannels::GetCustomList2)
   ;
}

#endif

#if defined(ON_WASM_COMPILE)
using namespace emscripten;

void initRenderChannelsBindings(void*)
{
  class_<BND_File3dmRenderChannels>("RenderChannels")
    //.constructor<>()
    //.constructor<const BND_File3dmRenderChannels&>()
    .property("mode", &BND_File3dmRenderChannels::GetMode, &BND_File3dmRenderChannels::SetMode)
    //.property("customIds", &BND_File3dmRenderChannels::GetCustomList, &BND_File3dmRenderChannels::SetCustomList)
    .property("customIds", &BND_File3dmRenderChannels::GetCustomList)
    ;
}
#endif
