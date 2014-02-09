# Load the Chrono::Engine unit and the postprocessing unit!!!
import ChronoEngine_PYTHON_core as chrono
import ChronoEngine_PYTHON_postprocess as postprocess
import ChronoEngine_PYTHON_irrlicht as chronoirr


# We will create two directories for saving some files, we need this:
import os
import math



# ---------------------------------------------------------------------
#
#  Create the simulation system and add items
#

my_system = chrono.ChSystem()


# Set the default outward/inward shape margins for collision detection,
# this is epecially important for very large or very small objects.
chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.001)
chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.001)

# Maybe you want to change some settings for the solver. For example you
# might want to use SetIterLCPmaxItersSpeed to set the number of iterations
# per timestep, etc.

#my_system.SetLcpSolverType(chrono.ChSystem.LCP_ITERATIVE_BARZILAIBORWEIN) # precise, more slow
my_system.SetIterLCPmaxItersSpeed(70)



# Create a contact material (surface property)to share between all objects.
# The rolling and spinning parameters are optional - if enabled they double
# the computational time.
brick_material = chrono.ChMaterialSurfaceShared()
brick_material.SetFriction(0.5)
brick_material.SetDampingF(0.2)
brick_material.SetCompliance (0.0000001)
brick_material.SetComplianceT(0.0000001)
# brick_material.SetRollingFriction(rollfrict_param)
# brick_material.SetSpinningFriction(0)
# brick_material.SetComplianceRolling(0.0000001)
# brick_material.SetComplianceSpinning(0.0000001)


# Create the room floor: a simple fixed rigid body with a collision shape
# and a visualization shape

body_floor = chrono.ChBodyShared()
body_floor.SetBodyFixed(True)
body_floor.SetPos(chrono.ChVectorD(0, -2, 0))
body_floor.SetMaterialSurface(brick_material)

# Collision shape
body_floor.GetCollisionModel().ClearModel()
body_floor.GetCollisionModel().AddBox(10, 1, 10) # hemi sizes
body_floor.GetCollisionModel().BuildModel()
body_floor.SetCollide(True)

# Visualization shape
body_floor_shape = chrono.ChBoxShapeShared()
body_floor_shape.GetBoxGeometry().Size = chrono.ChVectorD(10, 1, 10)
body_floor.GetAssets().push_back(body_floor_shape)

body_floor_texture = chrono.ChTextureShared()
body_floor_texture.SetTextureFilename('../bin/data/concrete.jpg')
body_floor.GetAssets().push_back(body_floor_texture)

my_system.Add(body_floor)



def create_application():
    # ---------------------------------------------------------------------
    #
    #  Create an Irrlicht application to visualize the system
    #

    myapplication = chronoirr.ChIrrApp(my_system)

    myapplication.AddTypicalSky('../bin/data/skybox/')
    myapplication.AddTypicalCamera(chronoirr.vector3df(0.5,0.5,1.0))
    myapplication.AddLightWithShadow(chronoirr.vector3df(2,4,2),    # point
                                     chronoirr.vector3df(0,0,0),    # aimpoint
                                     9,                 # radius (power)
                                     1,9,               # near, far
                                     30)                # angle of FOV

                # ==IMPORTANT!== Use this function for adding a ChIrrNodeAsset to all items
                # in the system. These ChIrrNodeAsset assets are 'proxies' to the Irrlicht meshes.
                # If you need a finer control on which item really needs a visualization proxy in
                # Irrlicht, just use application.AssetBind(myitem); on a per-item basis.

    myapplication.AssetBindAll();

                # ==IMPORTANT!== Use this function for 'converting' into Irrlicht meshes the assets
                # that you added to the bodies into 3D shapes, they can be visualized by Irrlicht!

    myapplication.AssetUpdateAll();

                # If you want to show shadows because you used "AddLightWithShadow()'
                # you must remember this:
    myapplication.AddShadowAll();



    myapplication.SetStepManage(True)
    myapplication.SetTimestep(0.001)
    myapplication.SetTryRealtime(True)
    return myapplication


# Create the set of bricks in a vertical stack, along Y axis

def create_block(center_x, center_y, center_z, size_x, size_y, size_z, weight):
    body_brick = chrono.ChBodyShared()

    body_brick.SetPos(chrono.ChVectorD(center_x, center_y, center_z))
    body_brick.SetMass(weight)
    body_brick.SetMaterialSurface(brick_material)

    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddBox(size_x/2, size_y/2, size_z/2)
    body_brick.GetCollisionModel().BuildModel()
    body_brick.SetCollide(True)

    body_brick_shape = chrono.ChBoxShapeShared()
    body_brick_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_x/2, size_y/2, size_z/2)
    if center_y%2==0:
        body_brick_shape.SetColor(chrono.ChColor(0.65, 0.65, 0.6)) # set gray color only for odd bricks
    body_brick.GetAssets().push_back(body_brick_shape)

    return body_brick



def check_stable_stack(boxs, draw=True):
    bricks = []
    for x, y, z, x_size, y_size, z_size, w in boxs:
        bricks.append(create_block(x - x_size/2, y - y_size/2, z - z_size/2, x_size, y_size, z_size, w))


    # bricks = [create_block(*k) for k in boxs]
    [my_system.Add(k) for k in bricks]

    Pos0 = [k.GetPos() for k in bricks]

    myapplication = create_application()    

    index = 0 
    while(myapplication.GetDevice().run()):
        index += 1
        
        if draw:
            myapplication.BeginScene()
            myapplication.DrawAll()
        
        for substep in range(0,5):
            myapplication.DoStep()

        if draw:
            myapplication.EndScene()

        if index == 100:
            break

    #import pdb; pdb.set_trace()
    Pos1 = [k.GetPos() for k in bricks]
    Rot1 = [k.GetRotAngle() for k in bricks]

    if any([abs(k) > 0.001 for k in Rot1]):
        # if the blocks rotate, it is not a stable stack
        return False

    return True
    # print([str(k) for k in Pos0])
    # print([str(k) for k in Pos1])



if __name__ == '__main__':
    import sys

    if len(sys.argv) > 2:
        boxs = eval(sys.argv[1])
        draw = eval(sys.argv[2])

        print(check_stable_stack(boxs, draw))


#bricks = [create_block(0, 0, 0, 1, 1, 1, 1), create_block(1, 0, 1, 3, 1, 1, 1), create_block(1, 1, 1, 1, 1, 2, 1)]
#assert check_stable_stack([ (1, 0, 1, 3, 1, 1, 1), (1, 1, 1, 1, 1, 2, 1)], True) == True
#assert check_stable_stack([ (1, 0, 1, 3, 1, 1, 1), (1, 1, 1, 1, 1, 3, 1)], True) == False
