
#include "bindings.h"

BND_File3dmRenderContent::BND_File3dmRenderContent()
{
  #if defined(ON_PYTHON_COMPILE)
    throw py::type_error("Unable to create an instance of RenderContent. Try creating RenderMaterial, RenderEnvironment, or RenderTexture");
  #endif
}

BND_File3dmRenderContent::BND_File3dmRenderContent(ON_RenderContent* rc)
{
  if (nullptr == rc)
  {
  #if defined(ON_PYTHON_COMPILE)
    throw py::value_error("NULL RenderContent");
  #endif
  }

  rc->SetId();

  SetTrackedPointer(rc, nullptr);
}

BND_File3dmRenderContent::BND_File3dmRenderContent(ON_RenderContent* rc, const ON_ModelComponentReference* compref)
{
  SetTrackedPointer(rc, compref);
}

BND_File3dmRenderContent::BND_File3dmRenderContent(const BND_File3dmRenderContent& other)
{
  SetTrackedPointer(other.m_rc->NewRenderContent(), nullptr);
}

BND_File3dmRenderContent::~BND_File3dmRenderContent()
{
}

void BND_File3dmRenderContent::SetTrackedPointer(ON_RenderContent* rc, const ON_ModelComponentReference* compref)
{
  m_rc = rc;

  BND_ModelComponent::SetTrackedPointer(rc, compref);
}

std::wstring BND_File3dmRenderContent::Kind() const
{
  return std::wstring(static_cast<const wchar_t*>(m_rc->Kind()));
}

std::wstring BND_File3dmRenderContent::TypeName() const
{
  return std::wstring(static_cast<const wchar_t*>(m_rc->TypeName()));
}

void BND_File3dmRenderContent::SetTypeName(const std::wstring& s)
{
  m_rc->SetTypeName(s.c_str());
}

BND_UUID BND_File3dmRenderContent::Id() const
{
  return ON_UUID_to_Binding(m_rc->Id());
}

std::wstring BND_File3dmRenderContent::Name() const
{
  return std::wstring(static_cast<const wchar_t*>(m_rc->Name()));
}

void BND_File3dmRenderContent::SetName(const std::wstring& s)
{
  m_rc->SetName(s.c_str());
}

BND_UUID BND_File3dmRenderContent::TypeId() const
{
  return ON_UUID_to_Binding(m_rc->TypeId());
}

void BND_File3dmRenderContent::SetTypeId(const BND_UUID& u)
{
  m_rc->SetTypeId(Binding_to_ON_UUID(u));
}

BND_UUID BND_File3dmRenderContent::RenderEngineId() const
{
  return ON_UUID_to_Binding(m_rc->RenderEngineId());
}

void BND_File3dmRenderContent::SetRenderEngineId(const BND_UUID& u)
{
  m_rc->SetRenderEngineId(Binding_to_ON_UUID(u));
}

BND_UUID BND_File3dmRenderContent::PlugInId() const
{
  return ON_UUID_to_Binding(m_rc->PlugInId());
}

void BND_File3dmRenderContent::SetPlugInId(const BND_UUID& u)
{
  m_rc->SetPlugInId(Binding_to_ON_UUID(u));
}

std::wstring BND_File3dmRenderContent::Notes() const
{
  return std::wstring(static_cast<const wchar_t*>(m_rc->Notes()));
}

void BND_File3dmRenderContent::SetNotes(const std::wstring& s)
{
  m_rc->SetNotes(s.c_str());
}

std::wstring BND_File3dmRenderContent::Tags() const
{
  return std::wstring(static_cast<const wchar_t*>(m_rc->Tags()));
}

void BND_File3dmRenderContent::SetTags(const std::wstring& s)
{
  m_rc->SetTags(s.c_str());
}

BND_UUID BND_File3dmRenderContent::GroupId() const
{
  return ON_UUID_to_Binding(m_rc->GroupId());
}

void BND_File3dmRenderContent::SetGroupId(const BND_UUID& u)
{
  m_rc->SetGroupId(Binding_to_ON_UUID(u));
}

bool BND_File3dmRenderContent::Hidden(void) const
{
  return m_rc->Hidden();
}

void BND_File3dmRenderContent::SetHidden(bool b)
{
  m_rc->SetHidden(b);
}

bool BND_File3dmRenderContent::Reference() const
{
  return m_rc->Reference();
}

void BND_File3dmRenderContent::SetReference(bool b)
{
  m_rc->SetReference(b);
}

bool BND_File3dmRenderContent::AutoDelete() const
{
  return m_rc->AutoDelete();
}

void BND_File3dmRenderContent::SetAutoDelete(bool b)
{
  return m_rc->SetAutoDelete(b);
}

static BND_File3dmRenderContent* NewRenderContentBinding(ON_RenderContent* rc)
{
  if (nullptr == rc)
    return nullptr;

  // I can't figure out the ownership again. If I don't make a copy it crashes later (double delete).
  // So -- I make a copy. No problem, except that now setters have no effect. So my question is:
  // what is the correct way to do this so that:
  // 1. It doesn't crash
  // 2. Setting data persists in the original object.

  auto* copy = rc->NewRenderContent();
  if (nullptr != copy)
  {
    *copy = *rc;

    if (rc->Kind() == ON_KIND_MATERIAL)
    {
      return new BND_File3dmRenderMaterial(copy, nullptr);
    }
    else
    if (rc->Kind() == ON_KIND_ENVIRONMENT)
    {
      return new BND_File3dmRenderEnvironment(copy, nullptr);
    }
    else
    if (rc->Kind() == ON_KIND_TEXTURE)
    {
      return new BND_File3dmRenderTexture(copy, nullptr);
    }
  }

  return nullptr;
}

BND_File3dmRenderContent* BND_File3dmRenderContent::Parent() const
{
  return NewRenderContentBinding(m_rc->Parent());
}

BND_File3dmRenderContent* BND_File3dmRenderContent::FirstChild() const
{
  return NewRenderContentBinding(m_rc->FirstChild());
}

BND_File3dmRenderContent* BND_File3dmRenderContent::NextSibling() const
{
  return NewRenderContentBinding(m_rc->NextSibling());
}

BND_File3dmRenderContent* BND_File3dmRenderContent::TopLevel() const
{
  return NewRenderContentBinding(&m_rc->TopLevel());
}

bool BND_File3dmRenderContent::IsTopLevel() const
{
  return m_rc->IsTopLevel();
}

bool BND_File3dmRenderContent::IsChild() const
{
  return m_rc->IsChild();
}

bool BND_File3dmRenderContent::SetChild(const ON_RenderContent& child, const std::wstring& csn)
{
  return m_rc->SetChild(child, csn.c_str());
}

std::wstring BND_File3dmRenderContent::ChildSlotName() const
{
  return std::wstring(static_cast<const wchar_t*>(m_rc->ChildSlotName()));
}

void BND_File3dmRenderContent::SetChildSlotName(const std::wstring& csn)
{
  m_rc->SetChildSlotName(csn.c_str());
}

bool BND_File3dmRenderContent::ChildSlotOn(const std::wstring& csn) const
{
  return m_rc->ChildSlotOn(csn.c_str());
}

bool BND_File3dmRenderContent::SetChildSlotOn(bool on, const std::wstring& csn)
{
  return m_rc->SetChildSlotOn(on, csn.c_str());
}

double BND_File3dmRenderContent::ChildSlotAmount(const wchar_t* child_slot_name) const
{
  return m_rc->ChildSlotAmount(child_slot_name, 100.0);
}

bool BND_File3dmRenderContent::SetChildSlotAmount(double amount, const wchar_t* child_slot_name)
{
  return m_rc->SetChildSlotAmount(amount, child_slot_name);
}

bool BND_File3dmRenderContent::DeleteChild(const std::wstring& csn)
{
  return m_rc->DeleteChild(csn.c_str());
}

BND_File3dmRenderContent* BND_File3dmRenderContent::FindChild(const std::wstring& csn) const
{
  ON_RenderContent* rc = const_cast<ON_RenderContent*>(m_rc->FindChild(csn.c_str()));
  return NewRenderContentBinding(rc);
}

std::wstring BND_File3dmRenderContent::XML(bool recursive) const
{
  return std::wstring(static_cast<const wchar_t*>(m_rc->XML(recursive)));
}

bool BND_File3dmRenderContent::SetXML(const std::wstring& xml)
{
  return m_rc->SetXML(xml.c_str());
}

std::wstring BND_File3dmRenderContent::GetParameter(const std::wstring& name) const
{
  return static_cast<const wchar_t*>(m_rc->GetParameter(name.c_str()).AsString());
}

bool BND_File3dmRenderContent::SetParameter(const std::wstring& name, const std::wstring& val)
{
  return m_rc->SetParameter(name.c_str(), val.c_str());
}


BND_File3dmRenderMaterial::BND_File3dmRenderMaterial()
  :
  BND_File3dmRenderContent(new ON_RenderMaterial)
{
}

BND_File3dmRenderMaterial::BND_File3dmRenderMaterial(const BND_File3dmRenderMaterial& other)
  :
  BND_File3dmRenderContent(other)
{
}

BND_File3dmRenderMaterial::BND_File3dmRenderMaterial(ON_RenderContent* rm, const ON_ModelComponentReference* compref)
  :
  BND_File3dmRenderContent(rm, compref)
{
}

BND_Material* BND_File3dmRenderMaterial::ToMaterial() const
{
  const auto* mat = dynamic_cast<const ON_RenderMaterial*>(m_rc);
  if (nullptr == mat)
    return nullptr;

  auto* m = new BND_Material;
  *m->m_material = mat->ToOnMaterial();

  return m;
}

BND_File3dmRenderEnvironment::BND_File3dmRenderEnvironment()
  :
  BND_File3dmRenderContent(new ON_RenderEnvironment)
{
}

BND_File3dmRenderEnvironment::BND_File3dmRenderEnvironment(const BND_File3dmRenderEnvironment& other)
  :
  BND_File3dmRenderContent(other)
{
}

BND_File3dmRenderEnvironment::BND_File3dmRenderEnvironment(ON_RenderContent* re, const ON_ModelComponentReference* compref)
  :
  BND_File3dmRenderContent(re, compref)
{
}

BND_Environment* BND_File3dmRenderEnvironment::ToEnvironment() const
{
  const auto* env = dynamic_cast<const ON_RenderEnvironment*>(m_rc);
  if (nullptr == env)
    return nullptr;

  auto* e = new BND_Environment;
  *e->m_env = env->ToOnEnvironment();

  return e;
}

BND_File3dmRenderTexture::BND_File3dmRenderTexture()
  :
  BND_File3dmRenderContent(new ON_RenderTexture)
{
}

BND_File3dmRenderTexture::BND_File3dmRenderTexture(const BND_File3dmRenderTexture& other)
  :
  BND_File3dmRenderContent(other)
{
}

BND_File3dmRenderTexture::BND_File3dmRenderTexture(ON_RenderContent* rt, const ON_ModelComponentReference* compref)
  :
  BND_File3dmRenderContent(rt, compref)
{
}

BND_Texture* BND_File3dmRenderTexture::ToTexture() const
{
  const auto* tex = dynamic_cast<const ON_RenderTexture*>(m_rc);
  if (nullptr == tex)
    return nullptr;

  auto* t = new BND_Texture;
  *t->m_texture = tex->ToOnTexture();

  return t;
}

std::wstring BND_File3dmRenderTexture::Filename() const
{
  std::wstring s;

  const auto* tex = dynamic_cast<const ON_RenderTexture*>(m_rc);
  if (nullptr != tex)
  {
    s = static_cast<const wchar_t*>(tex->Filename());
  }

  return s;
}

void BND_File3dmRenderTexture::SetFilename(const std::wstring& f)
{
  auto* tex = dynamic_cast<ON_RenderTexture*>(m_rc);
  if (nullptr != tex)
  {
    tex->SetFilename(f.c_str());
  }
}

void BND_File3dmRenderContentTable::Add(const BND_File3dmRenderContent& rc)
{
  const ON_RenderContent* r = rc.m_rc;
  m_model->AddModelComponent(*r);
}

BND_File3dmRenderContent* BND_File3dmRenderContentTable::FindIndex(int index)
{
  ON_ModelComponentReference compref = m_model->ComponentFromIndex(ON_ModelComponent::Type::RenderContent, index);
  const ON_ModelComponent* model_component = compref.ModelComponent();
  ON_RenderContent* model_rc = const_cast<ON_RenderContent*>(ON_RenderContent::Cast(model_component));
  if (nullptr != model_rc)
    return NewRenderContentBinding(model_rc);

  return nullptr;
}

BND_File3dmRenderContent* BND_File3dmRenderContentTable::IterIndex(int index)
{
  return FindIndex(index);
}

BND_File3dmRenderContent* BND_File3dmRenderContentTable::FindId(BND_UUID id)
{
  const ON_UUID _id = Binding_to_ON_UUID(id);
  ON_ModelComponentReference compref = m_model->ComponentFromId(ON_ModelComponent::Type::RenderContent, _id);
  const ON_ModelComponent* model_component = compref.ModelComponent();
  ON_RenderContent* model_rc = const_cast<ON_RenderContent*>(ON_RenderContent::Cast(model_component));
  if (nullptr != model_rc)
    return NewRenderContentBinding(model_rc);

  return nullptr;
}

//////////////////////////////////////////////////////////////////////////////

#if defined(ON_PYTHON_COMPILE)

void initRenderContentBindings(rh3dmpymodule& m)
{
  py::class_<BND_File3dmRenderContent>(m, "RenderContent")
    .def(py::init<>())
    .def(py::init<const BND_File3dmRenderContent&>(), py::arg("other"))
    .def_property_readonly("Kind", &BND_File3dmRenderContent::Kind)
    .def_property_readonly("Parent", &BND_File3dmRenderContent::Parent) //TODO: ALIGN WITH JS
    .def_property_readonly("IsChild", &BND_File3dmRenderContent::IsChild)
    .def_property_readonly("FirstChild", &BND_File3dmRenderContent::FirstChild)
    .def_property_readonly("NextSibling", &BND_File3dmRenderContent::NextSibling)
    .def_property_readonly("TopLevel", &BND_File3dmRenderContent::TopLevel)
    .def_property_readonly("IsTopLevel", &BND_File3dmRenderContent::IsTopLevel)
    .def_property_readonly("Id", &BND_File3dmRenderContent::Id)
    .def_property("Name", &BND_File3dmRenderContent::Name, &BND_File3dmRenderContent::SetName)
    .def_property("TypeName", &BND_File3dmRenderContent::TypeName, &BND_File3dmRenderContent::SetTypeName)
    .def_property("TypeId", &BND_File3dmRenderContent::TypeId, &BND_File3dmRenderContent::SetTypeId)
    .def_property("RenderEngineId", &BND_File3dmRenderContent::RenderEngineId, &BND_File3dmRenderContent::SetRenderEngineId)
    .def_property("PlugInId", &BND_File3dmRenderContent::PlugInId, &BND_File3dmRenderContent::SetPlugInId)
    .def_property("Notes", &BND_File3dmRenderContent::Notes, &BND_File3dmRenderContent::SetNotes)
    .def_property("Tags", &BND_File3dmRenderContent::Tags, &BND_File3dmRenderContent::SetTags)
    .def_property("GroupId", &BND_File3dmRenderContent::GroupId, &BND_File3dmRenderContent::SetGroupId)
    .def_property("Hidden", &BND_File3dmRenderContent::Hidden, &BND_File3dmRenderContent::SetHidden)
    .def_property("Reference", &BND_File3dmRenderContent::Reference, &BND_File3dmRenderContent::SetReference)
    .def_property("AutoDelete", &BND_File3dmRenderContent::AutoDelete, &BND_File3dmRenderContent::SetAutoDelete)
    .def_property("ChildSlotName", &BND_File3dmRenderContent::ChildSlotName, &BND_File3dmRenderContent::SetChildSlotName)
    .def("XML", &BND_File3dmRenderContent::XML, py::arg("recursive"))
    .def("SetXML", &BND_File3dmRenderContent::SetXML, py::arg("xml"))
    .def("ChildSlotOn", &BND_File3dmRenderContent::ChildSlotOn, py::arg("child_slot_name"))
    .def("SetChildSlotOn", &BND_File3dmRenderContent::SetChildSlotOn, py::arg("on"), py::arg("child_slot_name"))
    .def("ChildSlotAmount", &BND_File3dmRenderContent::ChildSlotAmount, py::arg("child_slot_name"))
    .def("SetChildSlotAmount", &BND_File3dmRenderContent::SetChildSlotAmount, py::arg("amount"), py::arg("child_slot_name"))
    .def("SetChild", &BND_File3dmRenderContent::SetChild, py::arg("child"), py::arg("child_slot_name"))
    .def("FindChild", &BND_File3dmRenderContent::FindChild, py::arg("child_slot_name"))
    .def("DeleteChild", &BND_File3dmRenderContent::DeleteChild, py::arg("child_slot_name"))
    .def("GetParameter", &BND_File3dmRenderContent::GetParameter, py::arg("param_name"))
    .def("SetParameter", &BND_File3dmRenderContent::SetParameter, py::arg("param_name"), py::arg("param_value"))
    ;

  py::class_<BND_File3dmRenderMaterial, BND_File3dmRenderContent>(m, "RenderMaterial")
    .def(py::init<>())
    .def(py::init<const BND_File3dmRenderMaterial&>(), py::arg("other"))
    .def("ToMaterial", &BND_File3dmRenderMaterial::ToMaterial)
    ;

  py::class_<BND_File3dmRenderEnvironment, BND_File3dmRenderContent>(m, "RenderEnvironment")
    .def(py::init<>())
    .def(py::init<const BND_File3dmRenderEnvironment&>(), py::arg("other"))
    .def("ToEnvironment", &BND_File3dmRenderEnvironment::ToEnvironment)
    ;

  py::class_<BND_File3dmRenderTexture, BND_File3dmRenderContent>(m, "RenderTexture")
    .def(py::init<>())
    .def(py::init<const BND_File3dmRenderTexture&>(), py::arg("other"))
    .def("ToTexture", &BND_File3dmRenderTexture::ToTexture)
    .def_property("FileName", &BND_File3dmRenderTexture::Filename, &BND_File3dmRenderTexture::SetFilename)
    ;
}

#endif

#if defined(ON_WASM_COMPILE)
using namespace emscripten;

void initRenderContentBindings(void*)
{
  class_<BND_File3dmRenderContent, base<BND_ModelComponent>>("RenderContent")
    .constructor<>()
    .constructor<const BND_File3dmRenderContent&>()
    .property("kind", &BND_File3dmRenderContent::Kind)
    .property("isChild", &BND_File3dmRenderContent::IsChild)
    .property("isTopLevel", &BND_File3dmRenderContent::IsTopLevel)
    .property("id", &BND_File3dmRenderContent::Id)
    .property("typeName", &BND_File3dmRenderContent::TypeName) 

    .function("getParent", &BND_File3dmRenderContent::Parent, allow_raw_pointers())
    .function("getFirstChild", &BND_File3dmRenderContent::FirstChild, allow_raw_pointers())
    .function("getNextSibling", &BND_File3dmRenderContent::NextSibling, allow_raw_pointers())
    .function("getTopLevel", &BND_File3dmRenderContent::TopLevel, allow_raw_pointers())
    .function("setTypeName", &BND_File3dmRenderContent::SetTypeName, allow_raw_pointers())
    .function("childSlotOn", &BND_File3dmRenderContent::ChildSlotOn, allow_raw_pointers())
    .function("setChildSlotOn", &BND_File3dmRenderContent::SetChildSlotOn, allow_raw_pointers())
    .function("childSlotAmount", &BND_File3dmRenderContent::ChildSlotAmount, allow_raw_pointers())
    .function("setChildSlotAmount", &BND_File3dmRenderContent::SetChildSlotAmount, allow_raw_pointers())
    .function("getXML", &BND_File3dmRenderContent::XML)
    .function("setXML",&BND_File3dmRenderContent::SetXML, allow_raw_pointers())
    .function("setChild", &BND_File3dmRenderContent::SetChild, allow_raw_pointers())       // I'm not sure about this. allow_raw_pointers())
    .function("findChild", &BND_File3dmRenderContent::FindChild, allow_raw_pointers())     // I'm not sure about this. allow_raw_pointers())
    .function("deleteChild", &BND_File3dmRenderContent::DeleteChild, allow_raw_pointers()) // I'm not sure about this. allow_raw_pointers())
    .function("getParameter", &BND_File3dmRenderContent::GetParameter, allow_raw_pointers())
    .function("setParameter", &BND_File3dmRenderContent::SetParameter, allow_raw_pointers())
    
    .property("name", &BND_File3dmRenderContent::Name, &BND_File3dmRenderContent::SetName)
    .property("typeId", &BND_File3dmRenderContent::TypeId, &BND_File3dmRenderContent::SetTypeId)
    .property("renderEngineId", &BND_File3dmRenderContent::RenderEngineId, &BND_File3dmRenderContent::SetRenderEngineId)
    .property("plugInId", &BND_File3dmRenderContent::PlugInId, &BND_File3dmRenderContent::SetPlugInId)
    .property("notes", &BND_File3dmRenderContent::Notes, &BND_File3dmRenderContent::SetNotes)
    .property("tags", &BND_File3dmRenderContent::Tags, &BND_File3dmRenderContent::SetTags)
    .property("groupId", &BND_File3dmRenderContent::GroupId, &BND_File3dmRenderContent::SetGroupId)
    .property("hidden", &BND_File3dmRenderContent::Hidden, &BND_File3dmRenderContent::SetHidden)
    .property("reference", &BND_File3dmRenderContent::Reference, &BND_File3dmRenderContent::SetReference)
    .property("autoDelete", &BND_File3dmRenderContent::AutoDelete, &BND_File3dmRenderContent::SetAutoDelete)
    .property("childSlotName", &BND_File3dmRenderContent::ChildSlotName, &BND_File3dmRenderContent::SetChildSlotName)
    
    ;

  class_<BND_File3dmRenderMaterial, base<BND_File3dmRenderContent>>("RenderMaterial")
    .constructor<>()
    .constructor<const BND_File3dmRenderMaterial&>()
    .function("toMaterial", &BND_File3dmRenderMaterial::ToMaterial, allow_raw_pointers())
    ;

  class_<BND_File3dmRenderEnvironment, base<BND_File3dmRenderContent>>("RenderEnvironment")
    .constructor<>()
    .constructor<const BND_File3dmRenderEnvironment&>()
    .function("toEnvironment", &BND_File3dmRenderEnvironment::ToEnvironment, allow_raw_pointers())
    ;

  class_<BND_File3dmRenderTexture, base<BND_File3dmRenderContent>>("RenderTexture")
    .constructor<>()
    .constructor<const BND_File3dmRenderTexture&>()
    .function("toTexture", &BND_File3dmRenderTexture::ToTexture, allow_raw_pointers())
    .property("fileName", &BND_File3dmRenderTexture::Filename)
    .function("setFilename", &BND_File3dmRenderTexture::SetFilename, allow_raw_pointers())
    ;

    
    
}
#endif
