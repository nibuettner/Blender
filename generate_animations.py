import bpy

src_obj = None
tgt_obj = None

def main():
    print('#######################################################')
    print('# Generate Animations                                 #')
    
#    print('src: %s' % src_obj)
#    print('tgt: %s' % tgt_obj)
    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')
    
    src_ed_armature = src_obj.data
    tgt_ed_armature = tgt_obj.data
    
    bpy.ops.object.mode_set(mode='POSE')
    
    # --- remove existing constraints ------------------------------------
    for tgt_bone in tgt_obj.pose.bones:
        for constraint in tgt_bone.constraints:
            cStr = constraint.type
            tgt_bone.constraints.remove(constraint)
            print('REMOVED CONSTRAINT: %s -> %s' % (tgt_bone.name, cStr))
    
    # --- add constraints ------------------------------------------------
    for tgt_bone in tgt_obj.pose.bones:
        print('tgt pose bone: %s' % tgt_bone.name)
        src_bone = src_obj.pose.bones.get(tgt_bone.name)
        print('src pose bone: %s' % src_bone.name)
        
        cnst = tgt_bone.constraints.new('COPY_LOCATION')
        cnst.name = 'Copy Location'
        cnst.target = src_obj
        cnst.subtarget = src_bone.name
        
        cnst = tgt_bone.constraints.new('COPY_ROTATION')
        cnst.name = 'Copy Rotation'
        cnst.target = src_obj
        cnst.subtarget = src_bone.name    

        cnst = tgt_bone.constraints.new('COPY_SCALE')
        cnst.name = 'Copy Scale'
        cnst.target = src_obj
        cnst.subtarget = src_bone.name
        
        cnst.target_space = 'WORLD' #seems better than 'POSE'
        cnst.owner_space = 'POSE'
        
        tgt_bone.lock_location = [False, False, False]
        tgt_bone.lock_rotation = [False, False, False]
        tgt_bone.lock_rotation_w = False
        tgt_bone.lock_rotations_4d = False
        tgt_bone.lock_scale = [False, False, False]

    # --- select all bones in pose mode ----------------------------------
    for tgt_bone in tgt_obj.pose.bones:
        tgt_bone.bone.select = True
        bpy.context.object.data.bones.active = tgt_bone.bone
            
    bpy.context.view_layer.objects.active = tgt_obj
    scene = bpy.context.scene
    
    if bpy.data.actions:
        for action in bpy.data.actions:
            src_obj.animation_data.action = action
            tgt_obj.animation_data.action = action
            print('src active action: %s' % (src_obj.animation_data.action))
            print('tgt active action: %s' % (tgt_obj.animation_data.action))
            print('action: %s - frame range: %s' % (action.name, action.frame_range))
            
            frame_from = (int)(action.frame_range[0])
            frame_to = (int)(action.frame_range[1])
            
            for frame in range(frame_from, frame_to + 1):
                scene.frame_current = frame
                scene.frame_set(scene.frame_current)
                bpy.ops.pose.visual_transform_apply()
                
                for tgt_bone in tgt_obj.pose.bones:
                    tgt_bone.keyframe_insert(data_path = 'location')
                    if tgt_bone.rotation_mode == "QUATERNION":
                        tgt_bone.keyframe_insert(data_path = 'rotation_quaternion')
                    else:
                        tgt_bone.keyframe_insert(data_path = 'rotation_euler')
                    tgt_bone.keyframe_insert(data_path = 'scale')
            
    # --- remove existing constraints ------------------------------------
    for tgt_bone in tgt_obj.pose.bones:
        for constraint in tgt_bone.constraints:
            cStr = constraint.type
            tgt_bone.constraints.remove(constraint)
            print('REMOVED CONSTRAINT: %s -> %s' % (tgt_bone.name, cStr))
    
    print('# Generate Animations: Done!                          #')
    print('#######################################################')

def validate():
    global src_obj, tgt_obj
    
    if len(bpy.context.selected_objects) == 0:
        print("Warning: Nothing selected")
        return False
    
    selectObjs = bpy.context.selected_objects
    
    arm_cnt = 0
    sel_arm = []
    
    if len(selectObjs) == 0:
        print("Warning: Nothing selected.")
        return False
    elif len(selectObjs) > 2:
        print("Warning: More than two objects selected.")
        return False
    
    for obj in selectObjs:
        if obj.type == 'ARMATURE':
            sel_arm.append(obj)
            arm_cnt += 1
            
    if arm_cnt == 0:
        print("Warning: No armature selected. Two expected.")
        return False
    if arm_cnt < 2:
        print("Warning: Not enough armatures selected. Two expected.")
        return False
    
    src_obj = sel_arm[0]
    tgt_obj = sel_arm[1]
    
    return True

################################################
if validate():
    main()