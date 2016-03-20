def logical_loc(camera, position):
    """
    assumption: camw == cawmh
    """
    rw = 2.0 / camera.img_w
    rh = 2.0 / camera.img_h
    camw = camera.img_w
    camh = camera.img_h
    rw2 = rw / 2.0
    rh2 = rh / 2.0
    if camw == camh:
        if position.x == 0:
            x = rw2 - 1
        else:
            x = (-1) + (position.x * rw) + rw2

        if position.y == 0:
            y = 1 - rh2
        else:
            y = 1 - (position.y * rh) - rh2
    else:
        raise 
        
    if camw > camh:
        if position.x == 0:
            x = rw2 - 1
        else:
            x = (-1) + (position.x * rw) + rw2

        if position.y == 0:
            y = (camh / float(camw)) - rw2
        else:
            y = (camh / float(camw)) - (position.y * rw) - rw2
    
    if camw < camh:
        if position.x == 0:
            x = rh2 - (camw / float(camh))
        else:
            x = (position.x * rh) - (camw / float(camh)) + rh2
    
        if position.y == 0:
            y = 1 - rh2
        else:
            y = 1 - (position.y * rh) - rh2

    return Vec3(x,y,0)

def intersect(ray, sphere):
    A = vector_sub(ray.origin, sphere.center)
    B = vector_dot(A, ray.direction)
    C = vector_dot(A,A) - sphere.radius**2
    D = max(0, B**2 - C)
    t = (-B) - D**0.5
    if (D > 0) and (t > 0):
        normal = vector_sub(position(ray, t), sphere.center).to_unit()
        return Hit(t, sphere.color, normal)
    else:
        return None

def shadowed(vector, light, sphere):
    lightv = light.direction
    nudge = vector_add(vector, lightv.scale(0.0001))
    new_ray = Ray(nudge, lightv)
    return intersect(new_ray, sphere) != None

def lighting(scene, ray, hit):
    sa = scene.amb 
    sl = scene.light
    if hit == None:
        return scene.bgcolor
    elif shadowed(position(ray, hit.dist), sl, sphere):
        return rgb_modulate(hit.surf_color, sa)
    else:
        scale = max(0, vector_dot(hit.surf_normal, sl.direction))
        product = rgb_add(sl.color.scale(scale), sa)
        return rgb_modulate(hit.surf_color, product)

sphere = Sphere(Vec3(0,0,3), 1, rgb(0.8, 0.8, 0.8))
light = Light(Vec3(-1,1,-1).to_unit(), rgb(1,1,1))
scene = Scene(rgb(0.3, 0.6, 1.0), sphere, light, rgb(0.2, 0.2, 0.2))
camera = Camera(-5, 180, 180)

im = Image.new("RGB", (camera.img_w, camera.img_h), "white")

for x in range(camera.img_w):
    for y in range(camera.img_h):
        origin = Vec3(0,0,camera.z)
        p = Posn(x,y)
        logical = logical_loc(camera,p)
        vector = vector_sub(logical, origin).to_unit()
        test_ray = Ray(origin, vector)
        hit = intersect(test_ray, sphere)
        color = lighting(scene,test_ray, hit)
        truecolor = color.to_color()
        im.putpixel((x,y),truecolor)

im.save("sphere" + str(int(time())) + ".png", "PNG")