#include "bindings.h"

#pragma once

#if defined(ON_PYTHON_COMPILE)
void initLinearWorkflowBindings(rh3dmpymodule& m);
#else
void initLinearWorkflowBindings(void* m);
#endif

class BND_File3dmLinearWorkflow
{
private:
  ON_LinearWorkflow* _lw = nullptr;
  bool _owned = false;

public:
  BND_File3dmLinearWorkflow();
  BND_File3dmLinearWorkflow(ON_LinearWorkflow* lw);
  BND_File3dmLinearWorkflow(const BND_File3dmLinearWorkflow& lw);
  ~BND_File3dmLinearWorkflow() { if (_owned) delete _lw; }
 
  bool GetPreProcessTexturesOn(void) const { return _lw->PreProcessTexturesOn(); }
  void SetPreProcessTexturesOn(bool v) { _lw->SetPreProcessTexturesOn(v); }

  bool GetPreProcessColorsOn(void) const { return _lw->PreProcessColorsOn(); }
  void SetPreProcessColorsOn(bool v) { _lw->SetPreProcessColorsOn(v); }

  float GetPreProcessGamma(void) const { return _lw->PreProcessGamma(); }
  void SetPreProcessGamma(float v) { _lw->SetPreProcessGamma(v); }

  bool GetPreProcessGammaOn(void) const { return _lw->PreProcessGammaOn(); }
  void SetPreProcessGammaOn(bool v) { _lw->SetPreProcessGammaOn(v); }

  float GetPostProcessGamma(void) const { return _lw->PostProcessGamma(); }
  void SetPostProcessGamma(float v) { _lw->SetPostProcessGamma(v); }

  bool GetPostProcessGammaOn(void) const { return _lw->PostProcessGammaOn(); }
  void SetPostProcessGammaOn(bool v) { _lw->SetPostProcessGammaOn(v); }
};
