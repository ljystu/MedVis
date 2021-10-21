from mevis import *
import vtk

def print_version():
  print(vtk.vtkVersion().GetVTKVersion())

def Cylinder():
    print (vtk.vtkVersion().GetVTKVersion())
    
    # Create a cylinder source, which is just a 3D primitive
    cylinder_source = vtk.vtkCylinderSource()
    cylinder_source.SetResolution(8)
    # Recall the data -> mapper -> actor -> renderer pipeline from the lectures
    cylinder_mapper = vtk.vtkPolyDataMapper()
    cylinder_mapper.SetInputConnection(cylinder_source.GetOutputPort())    
    
    # We create an actor of the mapped data, which we want to render.
    cylinder_actor = vtk.vtkActor()
    
    # We obtain its property and set the color to red.
    cylinder_actor.GetProperty().SetColor(0.0, 0.0, 1.0)
    
    """
        Take a moment to browse to the VTK reference manual at this point:
            https://vtk.org/doc/nightly/html/classvtkActor.html
            
        Ignore the huge graph, hit ctrl-f (or command-f) to search for the phrase "GetProperty"
        You should be able to find a table with `vtkProperty *   GetProperty ()` in it. The first part, `vtkProperty` indicates a return type. This is the object you get when you call `GetProperty()`. You can click the vtkProperty text to jump to the definition of the object. It will list all the possible functions and fields that the object offers.
        
        There's no need to know it all; working from examples is more efficient. 
        But if you don't know what a particular object offers; this is how you find out.
    """

    cylinder_actor.GetProperty().SetOpacity(0.5)
    # Now, we configure the mapper that cylinder-actor should use.
    cylinder_actor.SetMapper(cylinder_mapper)
    
    # Lastly, we need a renderer:
    
    # We instantiate a window and a vtk renderer
    render_window = vtk.vtkRenderWindow()
    renderer = vtk.vtkRenderer()
        
    # We configure the window to display the result of the VTK renderer 
    render_window.AddRenderer(renderer)
    
    # Set the resolution to 400x300 pixels
    render_window.SetSize(400, 300)

    # And add the actor of our cylinder to the renderer 
    renderer.AddActor(cylinder_actor)
    
    # Add an interactor for the window, so we can interact using the mouse 
    interactor = vtk.vtkRenderWindowInteractor()
    
    # Bind it to the window we created above
    interactor.SetRenderWindow(render_window)
      
    # Initialize the interactor
    interactor.Initialize()
    
    # Tell VTK to start rendering
    render_window.Render()
    
    # And tell the interactor to start as well 
    interactor.Start()
    
    # Now go back to `Assignment-3-1.mlab` and double-click the `Cylinder` module. Click the `Cylinder` button. You should obtain a window with an interactible cylinder in it. You can zoom by holding the right mouse button and rotate the cylinder by dragging with the left mouse button. Pressing w and s toggles between wireframe and shaded rendering.
