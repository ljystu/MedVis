import vtk 
from pathlib import Path

def vtkRenderVolume():
    ####################   Part 1   #############################
    # Read in our dataset.
    reader = vtk.vtkXMLImageDataReader()
    
    # Obtain the folder where this file is located and create a path to "./data/aneurysm.vti"
    current_workdirectory = Path(ctx.networkPath()) / Path("data/aneurysm.vti")
    
    # For debugging: show the given path
    print(current_workdirectory.absolute())
    
    # Convert the Path object to a string using str(...)
    reader.SetFileName(str(current_workdirectory))
    reader.Update()
    
    # Your vti file is now loaded! 
    image_data = reader.GetOutput()
   
    # If the path was correct, you can inspect the data's scalar range below.
    print(f"Image data range: {image_data.GetScalarRange()}")

    ####################   Part 2   #############################

    # Create a volume property, which will carry all optical properties of the volume (these will be set on Step 5)
    propVolume = vtk.vtkVolumeProperty()
    propVolume.ShadeOn()
    propVolume.SetInterpolationTypeToLinear()

    ####################   Part 3   #############################

    # If dataset contains negative values, we correct it by shifting upwards:
    LOWER_RANGE = image_data.GetScalarRange()[0]
    UPPER_RANGE = image_data.GetScalarRange()[1]
    
    math = vtk.vtkImageMathematics()
    
    if LOWER_RANGE < 0:
        math = vtk.vtkImageMathematics()
        math.SetInputData(reader.GetOutput())
        math.SetOperationToAddConstant()
        math.SetConstantC(-LOWER_RANGE)         # Change this line such that you map any range [a, b] to [0, N]
        math.Update()
        print(f"Data range mapped to new Range: {math.GetOutput().GetScalarRange()}")
        image_data = math.GetOutput()
        
    LOWER_RANGE = image_data.GetScalarRange()[0]
    UPPER_RANGE = image_data.GetScalarRange()[1]
    
    ####################   Part 4   #############################
    
    # NOTE: These values are specific to the `aneurysm.vti` dataset!
    
    # Create a Color TF (data values to colors), and an Opacity TF (data values to opacity)
    # ctf = vtk.vtkColorTransferFunction()
    # ctf.RemoveAllPoints() 
    # ctf.AddRGBPoint(image_data.GetScalarRange()[0], 0, 0, 0)
    # ctf.AddRGBPoint(1024, 0., 0., 0.) 
    # ctf.AddRGBPoint(1124, 0.5, 0.5, 0.2) 
    # ctf.AddRGBPoint(2000, 0.5, 0.5, 1.) 
    # ctf.AddRGBPoint(UPPER_RANGE, 1., 1., 1.)
    ctf = ctx.field("MLToVTKColorTransferFunction.outputColorTransferFunction").object()
    # otf = vtk.vtkPiecewiseFunction()
    # otf.RemoveAllPoints()
    # otf.AddPoint(LOWER_RANGE, 0) 
    # otf.AddPoint(1024, 0.0) 
    # otf.AddPoint(1124, 0.1) 
    # otf.AddPoint(2000, 0.7)
    # otf.AddPoint(UPPER_RANGE, 0)   
    otf = ctx.field("MLToVTKPiecewiseFunction.outputPiecewiseFunction").object()

    # Finally: Add the created TFs to the volume property
    propVolume.SetColor(ctf)
    propVolume.SetScalarOpacity(otf)

    ####################   Part 5   #############################
    
    # Switch between compositing methods here
    COMPOSITE = 0
    MIP = 1
    ISOSURF = 2
    compositing_method = 0
    
    mapper_volume = vtk.vtkVolumeRayCastMapper()
    
    if compositing_method == COMPOSITE:
        print("Raycasting in composite mode")
        raycast = vtk.vtkVolumeRayCastCompositeFunction()
        raycast.SetCompositeMethodToClassifyFirst()
        mapper_volume.SetVolumeRayCastFunction(raycast) 
    elif compositing_method == MIP:
        print("Raycasting in MIP mode")
        mip_raycast = vtk.vtkVolumeRayCastMIPFunction()
        mapper_volume.SetVolumeRayCastFunction(mip_raycast) 
    else:
        print("Raycasting in iso-surf mode")
        isosurf_raycast = vtk.vtkVolumeRayCastIsosurfaceFunction()
        isosurf_raycast.SetIsoValue(1400)
        mapper_volume.SetVolumeRayCastFunction(isosurf_raycast)     


    ####################   Rendering boilerplate   #############################
    
    
    # Data type of image data must be shifted to unsiged short ints or VTK will not show anything
    image_shift = vtk.vtkImageShiftScale()
    image_shift.SetInputData(image_data)
    image_shift.SetOutputScalarTypeToUnsignedShort()
    image_shift.Update()

    mapper_volume.SetInputData(image_shift.GetOutput())  

    actor_volume = vtk.vtkVolume()
    actor_volume.SetMapper(mapper_volume)
    actor_volume.SetProperty(propVolume)

    render_window = vtk.vtkRenderWindow()
    renderer = vtk.vtkRenderer()
    render_window.AddRenderer(renderer)

    renderer.AddActor(actor_volume)
    renderer.SetBackground(1,1,1)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    interactor.Initialize()
    render_window.Render()
    interactor.Start()