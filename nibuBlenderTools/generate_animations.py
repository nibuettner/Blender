#================ TODOs ================
#================ TODOs ================

src_obj = None
tgt_obj = None

import bpy

def GetBoneHierarchy():
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
                ['DEF-spine.006', 'DEF-spine.005', True, 'spine-006'], # head

                ['DEF-breast.L', 'DEF-spine.003', False, 'breast-l'],
                ['DEF-breast.R', 'DEF-spine.003', False, 'breast-r'],

                # --- left arm ------------------------------
                ['DEF-shoulder.L', 'DEF-spine.003', False, 'shoulder-l'],

                ['DEF-upper_arm.L', 'DEF-shoulder.L', False, 'upperarm-l'],
                ['DEF-upper_arm.L.001', 'DEF-upper_arm.L', True, 'upperarm-001-l'],
                ['DEF-forearm.L', 'DEF-upper_arm.L.001', True, 'forearm-l'],
                ['DEF-forearm.L.001', 'DEF-forearm.L', True, 'forearm-001-l'],
                ['DEF-hand.L', 'DEF-forearm.L.001', True, 'hand-l'],

                # --- right arm -----------------------------
                ['DEF-shoulder.R', 'DEF-spine.003', False, 'shoulder-r'],

                ['DEF-upper_arm.R', 'DEF-shoulder.R', False, 'upperarm-r'],
                ['DEF-upper_arm.R.001', 'DEF-upper_arm.R', True, 'upperarm-001-r'],
                ['DEF-forearm.R', 'DEF-upper_arm.R.001', True, 'forearm-r'],
                ['DEF-forearm.R.001', 'DEF-forearm.R', True, 'forearm-001-r'],
                ['DEF-hand.R', 'DEF-forearm.R.001', True, 'hand-r'],

                # --- left leg ------------------------------
                ['DEF-pelvis.L', 'DEF-spine', False, 'pelvis-l'],

                ['DEF-thigh.L', 'DEF-spine', False, 'thigh-l'],
                ['DEF-thigh.L.001', 'DEF-thigh.L', True, 'thigh-001-l'],
                ['DEF-shin.L', 'DEF-thigh.L.001', True, 'shin-l'],
                ['DEF-shin.L.001', 'DEF-shin.L', True, 'shin-001-l'],
                ['DEF-foot.L', 'DEF-shin.L.001', True, 'foot-l'],
                ['DEF-toe.L', 'DEF-foot.L', True, 'toe-l'],

                # --- right leg -----------------------------
                ['DEF-pelvis.R', 'DEF-spine', False, 'pelvis-r'],

                ['DEF-thigh.R', 'DEF-spine', False, 'thigh-r'],
                ['DEF-thigh.R.001', 'DEF-thigh.R', True, 'thigh-001-r'],
                ['DEF-shin.R', 'DEF-thigh.R.001', True, 'shin-r'],
                ['DEF-shin.R.001', 'DEF-shin.R', True, 'shin-001-r'],
                ['DEF-foot.R', 'DEF-shin.R.001', True, 'foot-r'],
                ['DEF-toe.R', 'DEF-foot.R', True, 'toe-r']]
                
    return boneNames

def DeselectAll():
    for obj in bpy.context.selected_objects:
        obj.select_set(False)

def main():
    print('#######################################################')
    print('# Generate Animations                                 #')
    
    # --- purge all objects without users -------
    bpy.ops.outliner.orphans_purge()
    
    bone_hierarchy = GetBoneHierarchy()
    
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

    bpy.ops.object.mode_set(mode='EDIT')
    
#    for tgt_bone in tgt_obj.data.edit_bones:
#        tgt_bone.parent = None
        
    bpy.ops.object.mode_set(mode='POSE')
    
    # --- add constraints ------------------------------------------------
    # We want the target bones to copy location, rotation and scale of
    # the source bones
    for tgt_bone in tgt_obj.pose.bones:
        for bone_entry in bone_hierarchy:
#            b_found = False
            if tgt_bone.name == bone_entry[3]:
#                b_found = True
                src_bone_name = bone_entry[0]
                
#                src_bone = src_obj.pose.bones.get(tgt_bone.name)
                print('src pose bone: %s' % src_bone_name)
                
                cnst = tgt_bone.constraints.new('COPY_LOCATION')
                cnst.name = 'Copy Location'
                cnst.target = src_obj
                cnst.subtarget = src_bone_name
                
                cnst.target_space = 'WORLD'
                cnst.owner_space = 'POSE'
                
                cnst = tgt_bone.constraints.new('COPY_ROTATION')
                cnst.name = 'Copy Rotation'
                cnst.target = src_obj
                cnst.subtarget = src_bone_name

                cnst.target_space = 'WORLD'
                cnst.owner_space = 'POSE'

                cnst = tgt_bone.constraints.new('COPY_SCALE')
                cnst.name = 'Copy Scale'
                cnst.target = src_obj
                cnst.subtarget = src_bone_name
                
                cnst.target_space = 'WORLD'
                cnst.owner_space = 'POSE'
                
                break
        
    # --- select all bones in pose mode ----------------------------------
    for tgt_bone in tgt_obj.pose.bones:
        tgt_bone.bone.select = True
        bpy.context.object.data.bones.active = tgt_bone.bone

    DeselectAll()
    tgt_obj.select_set(True)
    bpy.context.view_layer.objects.active = tgt_obj
    scene = bpy.context.scene
    
    if bpy.data.actions:
        ln = len(bpy.data.actions)
        
        actions = []
        newActions = []
        
        # selet relevant actions
        for i in range(0, ln):
            action = bpy.data.actions[i]
            
            if action.name.find("rig.") > -1 and action.name.find("PoseLib") == -1:
                print('valid source action: %s' % (action.name))
                actions.append(action)
            
        for action in actions:
                newAction = bpy.data.actions.new(action.name[4:])
                print('new action: %s' % (newAction.name))
                
                src_obj.animation_data.action = action
                tgt_obj.animation_data.action = newAction
                
                print('action: %s - frame range: %s' % (action.name, action.frame_range))

                frame_from = (int)(action.frame_range[0])
                frame_to = (int)(action.frame_range[1])
                
                frame_from = (int)(action.frame_range[0])
                frame_to = (int)(action.frame_range[1])
                print('frame_from: %s - frame_to: %s' % (frame_from, frame_to))
                
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

                newActions.append(newAction)

#    original_context = bpy.context.area.type
    
#    bpy.context.area.type = 'VIEW_3D'
#    bpy.ops.object.mode_set(mode='OBJECT')
    
#    bpy.context.area.type = 'ACTION_EDITOR'
    
    DeselectAll()
    src_obj.select_set(True)
    
#    for action in newActions:
#        bpy.context.object.animation_data.action = action
#        bpy.ops.action.unlink()
        
#    bpy.context.area.type = original_context
     
    # --- remove existing constraints ------------------------------------
    for tgt_bone in tgt_obj.pose.bones:
        for constraint in tgt_bone.constraints:
            cStr = constraint.type
            tgt_bone.constraints.remove(constraint)
            print('REMOVED CONSTRAINT: %s -> %s' % (tgt_bone.name, cStr))
            
    bpy.ops.object.mode_set(mode='OBJECT')
    DeselectAll()
    
#    tgt_obj.select_set(True)

#    for action in newActions:
#        print('New Action: %s' % (action.name))
#        
#        track = tgt_obj.animation_data.nla_tracks.new()
#        track.name = action.name
#        track.strips.new(action.name, action.frame_range[0], action)
#        
#    tgt_obj.animation_data.action = None
#    src_obj.animation_data.action = None

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