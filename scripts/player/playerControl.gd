extends KinematicBody

var pos = Vector3(0, 0, 0)
var velX = 0
var velY = 0
var velZ = 0
var timePassed = 0


func _ready():
	set_process(true)
	
	pass

func _fixed_process(delta):
	
	pass

func _process(delta):
	set_translation(get_translation() + Vector3(velX, velY, velZ) * delta)
	timePassed += delta;
	if (!is_colliding() and get_translation().y >= 0):
		velY -= 0.2
	else:
		velY = 0
		set_translation(Vector3(get_translation().x, 0, get_translation().z))
		pass
	
	
	pass