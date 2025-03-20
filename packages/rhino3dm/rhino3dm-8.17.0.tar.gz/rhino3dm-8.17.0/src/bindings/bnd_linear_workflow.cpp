
#include "bindings.h"

BND_File3dmLinearWorkflow::BND_File3dmLinearWorkflow()
{
  _lw = new ON_LinearWorkflow;
  _owned = true;
}

BND_File3dmLinearWorkflow::BND_File3dmLinearWorkflow(const BND_File3dmLinearWorkflow& lw)
{
   // see bnd_ground_plane.cpp for justification
  _lw = lw._lw;

  if (lw._owned)
  {
    // Tell the original owner that it no longer owns it.
    const_cast<BND_File3dmLinearWorkflow&>(lw)._owned = false;

    // This object now owns it instead.
    _owned = true;
  }

  // Old code makes an actual copy of the native object -- which means changes don't stick.
  //_lw = new ON_LinearWorkflow(*lw._lw); 
  //_owned = true; 
}

BND_File3dmLinearWorkflow::BND_File3dmLinearWorkflow(ON_LinearWorkflow* lw)
: _lw(lw)
{
}

#if defined(ON_PYTHON_COMPILE)

void initLinearWorkflowBindings(rh3dmpymodule& m)
{
  py::class_<BND_File3dmLinearWorkflow>(m, "LinearWorkflow")
    .def(py::init<>())
    .def(py::init<const BND_File3dmLinearWorkflow&>(), py::arg("other"))
    .def_property("PreProcessTexturesOn", &BND_File3dmLinearWorkflow::GetPreProcessTexturesOn, &BND_File3dmLinearWorkflow::SetPreProcessTexturesOn)
    .def_property("PreProcessColorsOn", &BND_File3dmLinearWorkflow::GetPreProcessColorsOn, &BND_File3dmLinearWorkflow::SetPreProcessColorsOn)
    .def_property("PreProcessGamma", &BND_File3dmLinearWorkflow::GetPreProcessGamma, &BND_File3dmLinearWorkflow::SetPreProcessGamma)
    .def_property("PreProcessGammaOn", &BND_File3dmLinearWorkflow::GetPreProcessGammaOn, &BND_File3dmLinearWorkflow::SetPreProcessGammaOn)
    .def_property("PostProcessGamma", &BND_File3dmLinearWorkflow::GetPostProcessGamma, &BND_File3dmLinearWorkflow::SetPostProcessGamma)
    .def_property("PostProcessGammaOn", &BND_File3dmLinearWorkflow::GetPostProcessGammaOn, &BND_File3dmLinearWorkflow::SetPostProcessGammaOn)
   ;
}

#endif

#if defined(ON_WASM_COMPILE)
using namespace emscripten;

void initLinearWorkflowBindings(void*)
{
  class_<BND_File3dmLinearWorkflow>("LinearWorkflow")
    //.constructor<>()
    //.constructor<const BND_File3dmLinearWorkflow&>()
    .property("preProcessTexturesOn", &BND_File3dmLinearWorkflow::GetPreProcessTexturesOn, &BND_File3dmLinearWorkflow::SetPreProcessTexturesOn)
    .property("preProcessColorsOn", &BND_File3dmLinearWorkflow::GetPreProcessColorsOn, &BND_File3dmLinearWorkflow::SetPreProcessColorsOn)
    .property("preProcessGamma", &BND_File3dmLinearWorkflow::GetPreProcessGamma, &BND_File3dmLinearWorkflow::SetPreProcessGamma)
    .property("preProcessGammaOn", &BND_File3dmLinearWorkflow::GetPreProcessGammaOn, &BND_File3dmLinearWorkflow::SetPreProcessGammaOn)
    .property("postProcessGamma", &BND_File3dmLinearWorkflow::GetPostProcessGamma, &BND_File3dmLinearWorkflow::SetPostProcessGamma)
    .property("postProcessGammaOn", &BND_File3dmLinearWorkflow::GetPostProcessGammaOn, &BND_File3dmLinearWorkflow::SetPostProcessGammaOn)
    ;
}
#endif
