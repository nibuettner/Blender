newRigName = 'root'
newRigNameArmatureName = 'UE_Armature'
newActionNamePrefix = 'UE_'
newActionNameSuffix = ''

import bpy, math

def getBoneHierarchy():
    # [subject, parent, connected, rename-to]
    boneNames = [
                #['root', None, False, 'root'],
                #['torso', 'root', False],
                #['hips', 'torso', False],
                #['chest', 'torso', False],

                ['DEF-spine', None, False, 'spine'],
                ['DEF-spine.001', 'DEF-spine', True, 'spine-001'],
                ['DEF-spine.002', 'DEF-spine.001', True, 'spine-002'],
                ['DEF-spine.003', 'DEF-spine.002', True, 'spine-003'],
                ['DEF-spine.004', 'DEF-spine.003', True, 'spine-004'],
                ['DEF-spine.005', 'DEF-spine.004', True, 'spine-005'],
                ['DEF-spine.006', 'DEF-spine.005', True, 'head'], # head

                ['DEF-breast.L', 'DEF-spine.003', False, 'breast-l'],
                ['DEF-breast.R', 'DEF-spine.003', False, 'breast-r'],

                # --- left arm ------------------------------
                ['DEF-shoulder.L', 'DEF-spine.003', False, 'shoulder-l'],

                ['DEF-upper_arm.L', 'DEF-shoulder.L', False, 'upperarm-l'],
                ['DEF-upper_arm.L.001', 'DEF-upper_arm.L', True, 'upperarm-l-001'],
                ['DEF-forearm.L', 'DEF-upper_arm.L.001', True, 'forearm-l'],
                ['DEF-forearm.L.001', 'DEF-forearm.L', True, 'forearm-l-001'],
                ['DEF-hand.L', 'DEF-forearm.L.001', True, 'hand-l'],

                # --- right arm -----------------------------
                ['DEF-shoulder.R', 'DEF-spine.003', False, 'shoulder-r'],

                ['DEF-upper_arm.R', 'DEF-shoulder.R', False, 'upperarm-r'],
                ['DEF-upper_arm.R.001', 'DEF-upper_arm.R', True, 'upperarm-r-001'],
                ['DEF-forearm.R', 'DEF-upper_arm.R.001', True, 'forearm-r'],
                ['DEF-forearm.R.001', 'DEF-forearm.R', True, 'forearm-r-001'],
                ['DEF-hand.R', 'DEF-forearm.R.001', True, 'hand-r'],

                # --- left leg ------------------------------
                ['DEF-pelvis.L', 'DEF-spine', False, 'pelvis-l'],

                ['DEF-thigh.L', 'DEF-spine', False, 'thigh-l'],
                ['DEF-thigh.L.001', 'DEF-thigh.L', True, 'thigh-l-001'],
                ['DEF-shin.L', 'DEF-thigh.L.001', True, 'shin-l'],
                ['DEF-shin.L.001', 'DEF-shin.L', True, 'shin-l-001'],
                ['DEF-foot.L', 'DEF-shin.L.001', True, 'foot-l'],
                ['DEF-toe.L', 'DEF-foot.L', True, 'toe-l'],

                # --- right leg -----------------------------
                ['DEF-pelvis.R', 'DEF-spine', False, 'pelvis-r'],

                ['DEF-thigh.R', 'DEF-spine', False, 'thigh-r'],
                ['DEF-thigh.R.001', 'DEF-thigh.R', True, 'thigh-r-001'],
                ['DEF-shin.R', 'DEF-thigh.R.001', True, 'shin-r'],
                ['DEF-shin.R.001', 'DEF-shin.R', True, 'shin-r-001'],
                ['DEF-foot.R', 'DEF-shin.R.001', True, 'foot-r'],
                ['DEF-toe.R', 'DEF-foot.R', True, 'toe-r']]
                
    return boneNames

def printDeformBoneNames(rig):
    for bone in rig.data.bones:
        if bone.use_deform:
            print('  DEFORM: ' + bone.name)
        else:
            print('NODEFORM: ' + bone.name)

def printBoneMappings(boneNames):
    for b in boneNames:
        if b[1] != None:
            print('BONE mapping: ' + b[0] + ' -> ' + b[1])
        else:
            print('BONE mapping: ' + b[0] + ' -> None')

def main():
    print('#######################################################')
    print('# RigifyToUnreal                                      #')
    
    initialSelection = bpy.context.selected_objects
    
    # --- get selected armature -----------------
    for obj in initialSelection:
        #print('OBJ: ' + obj.name)
        if obj.type == 'ARMATURE':
            #bpy.context.scene.objects.active = obj
            bpy.context.view_layer.objects.active = obj
            rigifyObj = obj
        else:
            obj.select_set(False)
    
    #printDeformBoneNames(rigifyObj)
    
    # --- create copy of armature ---------------
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False})

    newRigObj = bpy.context.object
    newRigObj.name = newRigName
    newRigObj.animation_data.action = None
    newRigObj.pose.bones['root'].custom_shape = None
    
    armature = newRigObj.data
    armature.layers =  [True for i in range(32)] # all
    armature.name = newRigNameArmatureName
    
    boneNames = getBoneHierarchy()
    #printBoneMappings(boneNames)
    
    # --- delete constraints --------------------
    for bone in newRigObj.pose.bones:
        bone.bone.driver_remove('hide')
        bone.bone.driver_remove('bbone_easein')
        bone.bone.driver_remove('bbone_easeout')
        for constraint in bone.constraints:
            cStr = constraint.type
            bone.constraints.remove(constraint)
            #print('REMOVED CONSTRAINT: %s -> %s' % (bone.name, cStr))

    # --- delete driver -------------------------
    for d in rigifyObj.animation_data.drivers:
        dStr = d.data_path
        success = newRigObj.driver_remove(d.data_path, -1)
        
    # --- delete unneeded bones -----------------
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    deleteBones = []
    for armBone in armature.edit_bones:
        #print('armBone.name: ' + armBone.name)
        isFound = False
        for boneName in boneNames:
            if armBone.name == boneName[0]:
                isFound = True
                break
            
        if not isFound:
            #print('DELETE: ' + armBone.name)
            deleteBones.append(armBone)

    for deleteBone in deleteBones:
        armature.edit_bones.remove(deleteBone)
    
    # --- update bone hierarchy -----------------
    for editBone in armature.edit_bones:
        for boneName in boneNames:
            if editBone.name == boneName[0] and boneName[1] != None:
                #isFound = True
                
                editBone.parent = armature.edit_bones[boneName[1]]
                editBone.use_connect = boneName[2]
                editBone.use_inherit_rotation = False  #works fine w/o these. 
                editBone.use_inherit_scale = False     #otherwise, I don't know why work w/o these.
                
                if not boneName[2]:
                    editBone.use_local_location = False
                break
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    # --- rename bones --------------------------
    #boneRename = {}
    #for boneName in boneNames:
    #    boneRename[boneName[0]] = boneName[3]
    #    
    #for bone in newRigObj.pose.bones:
    #    print('from: %s - to: %s' % (bone.name, boneRename[bone.name]))
    #    bone.name = boneRename[bone.name]
    
    # --- update constraints --------------------
    for bone in newRigObj.pose.bones:
        cnst = bone.constraints.new('COPY_LOCATION')
        cnst.name = 'Copy Location'
        cnst.target = rigifyObj
        cnst.subtarget = bone.name
        
        cnst = bone.constraints.new('COPY_ROTATION')
        cnst.name = 'Copy Rotation'
        cnst.target = rigifyObj
        cnst.subtarget = bone.name    

        cnst = bone.constraints.new('COPY_SCALE')
        cnst.name = 'Copy Scale'
        cnst.target = rigifyObj
        cnst.subtarget = bone.name
        
        cnst.target_space = 'WORLD' #seems better than 'POSE'
        cnst.owner_space = 'POSE'
        
        bone.lock_location = [False, False, False]
        bone.lock_rotation = [False, False, False]
        bone.lock_rotation_w = False
        bone.lock_rotations_4d = False
        bone.lock_scale = [False, False, False]
    
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    rigArmature = rigifyObj.data
    
    # CLEAR PARENT
    # REPARENT
    
    bpy.ops.object.mode_set(mode = 'OBJECT')

    print('# RigifyToUnreal : Done!                              #')
    print('#######################################################')

def validate():
    if len(bpy.context.selected_objects) == 0:
        print("Warning: Nothing selected")
        return False
    
    selectObjs = bpy.context.selected_objects
    armatureCount = 0
    rigifyObj = None
    for obj in selectObjs:
        if obj.type == 'ARMATURE':
            rigifyObj = obj
            armatureCount += 1
    
    if armatureCount == 0:
        print("Warning: No armature is selected.")
        return False
    elif armatureCount >= 2:
        print("Warning: Multiple armatures are selected")
        return False

    return True

################################################
if validate():
    main()