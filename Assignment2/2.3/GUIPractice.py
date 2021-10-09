
# We create a dictionary with the mapping: True -> 3D, False -> 2D.
def is2DOr3D(toggleValue):
	toggle_to_viewer = {
		True: "3D",
		False: "2D"
	} 
	return toggle_to_viewer[toggleValue]

# If the button is pressed, we call this function. The function reads the current boolean value of the field "persistentToggle" and then flips this value.
def buttonPressed():
	current_value = not ctx.field("persistentToggle").value
	ctx.field("persistentToggle").value = current_value
	print(f"Current viewer is: {is2DOr3D(current_value)}")
	
	if current_value:
		touchField(ctx.field("SphereDrawer.update"))
	else:
		touchField(ctx.field("CircleDrawer.update"))
	toggleViewer()
	
def touchField(Field):
	print(f"Touched field: {Field}")
	Field.touch()

def toggleViewer():
	switchField = ctx.field("Switch2D3D.currentInput")
	current_value = switchField.value
	if current_value == 1:
		switchField.value = 0
	else:
		switchField.value = 1
	print(f"Switching from {is2DOr3D(current_value == 1)} to {is2DOr3D(switchField.value == 1)}!")
