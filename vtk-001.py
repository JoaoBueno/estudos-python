# Biblioteca vtk para python
# from vtk import *
import vtk

# ENTRADA DE DADOS
# Pontos
points = vtk.vtkPoints()
points.SetNumberOfPoints(3)
points.InsertPoint(0, 76.3221, 77.55, 6.51956)
points.InsertPoint(1, 76.61, 77.2565, 6.48612)
points.InsertPoint(2, 77.2707, 76.61, 6.44554)
# Tensores
dbar = vtk.vtkDoubleArray()
dbar.SetNumberOfTuples(3)
dbar.SetNumberOfComponents(9)
dbar.InsertTuple9(0, -1.15233, 0.0831558, 0.0469417, 0.0831558, -1.25721, 0.10167, 0.0469417, 0.10167, -1.10715)
dbar.InsertTuple9(1, -1.18056, 0.0817272, 0.016076, 0.0817272, -1.32675, 0.125833, 0.016076, 0.125833, -1.15438)
dbar.InsertTuple9(2, -1.18056, 0.0817272, 0.016076, 0.0817272, -1.32675, 0.125833, 0.016076, 0.125833, -1.15438)

# PROCESSAMENTO PARA GERAR OS GLIFOS
# Polydata
indata = vtk.vtkPolyData()
indata.SetPoints(points)
indata.GetPointData().SetTensors(dbar)
# Codigo para uma esfera
src = vtk.vtkSphereSource()
src.SetThetaResolution(16)
src.SetPhiResolution(16)
# glifos
epp = vtk.vtkTensorGlyph()
epp.SetInput(indata)
epp.SetSourceConnection(src.GetOutputPort())
epp.SetScaleFactor(1)
epp.ClampScalingOn()
# epp.SymmetricOn()
epp.ColorGlyphsOff()
epp.ThreeGlyphsOff()
epp.ExtractEigenvaluesOn()
epp.SetColorModeToEigenvalues()
# Mapeador para os dados
map = vtk.vtkPolyDataMapper()
map.SetInputConnection(epp.GetOutputPort())

# VISUALIZACAO
# Ator
elactor = vtk.vtkActor()
elactor.SetMapper(map)
# Renderizador
renderer = vtk.vtkRenderer()
renderer.AddActor(elactor)
# Janela
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
# Interador
interactor = ctk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderWindow)
interactor.Initialize()
interactor.Start()
