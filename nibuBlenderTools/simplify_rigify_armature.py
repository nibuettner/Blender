#================ TODOs ================
#================ TODOs ================

simplified_armature_obj_name = 'root'
simplified_armature_name = 'UE_Armature'

new_mesh_obj_name = "PlayerCharacter.base.m"
new_mesh_name = "PlayerCharacter.base.m.mesh"

tgt_collection_name = "Final"

newRigName = 'root'
newRigNameArmatureName = 'UE_Armature'
newActionNamePrefix = 'UE_'
newActionNameSuffix = ''

#======================================================================

import bpy, math

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

#======================================================================
def PrintDeformBoneNames(rig):
    for bone in rig.data.bones:
        if bone.use_deform:
            print('  DEFORM: ' + bone.name)
#        else:
#            print('NODEFORM: ' + bone.name)

#======================================================================
def DeselectAll():
    for obj in bpy.context.selected_objects:
        obj.select_set(False)

#======================================================================
def SimplifyRigifyArmature(rigify_armature_obj):
    print('#######################################################')
    print('# Simplify Rigify Armature                            #')
    
    
#    bpy.context.area.type = 'VIEW_3D'
#    print('Current Context: %s' % (bpy.context.area.type))
    
    
    simplified_armature_obj = None
    
    DeselectAll()
    
    if rigify_armature_obj:
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        # --- copy artmature object -----------------
        bpy.context.view_layer.objects.active = rigify_armature_obj
        rigify_armature_obj.select_set(True)
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked" : False})
        
        simplified_armature_obj = bpy.context.object
        simplified_armature_obj.name = simplified_armature_obj_name
        simplified_armature_obj.animation_data.action = None
        simplified_armature_obj.pose.bones['root'].custom_shape = None
        
        simplified_armature = simplified_armature_obj.data
        simplified_armature.layers =  [True for i in range(32)] # activate all layers
        simplified_armature.name = simplified_armature_name
        
        bone_hierarchy = GetBoneHierarchy()
        
        # --- delete constraints --------------------
        for bone in simplified_armature_obj.pose.bones:
            bone.bone.driver_remove('hide')
            bone.bone.driver_remove('bbone_easein')
            bone.bone.driver_remove('bbone_easeout')
            
            for constraint in bone.constraints:
                cStr = constraint.type
                bone.constraints.remove(constraint)
                #print('REMOVED CONSTRAINT: %s -> %s' % (bone.name, cStr))
                
            bone.lock_location = [False, False, False]
            bone.lock_rotation = [False, False, False]
            bone.lock_rotation_w = False
            bone.lock_rotations_4d = False
            bone.lock_scale = [False, False, False]
            
        # --- delete drivers ------------------------
        for driver in rigify_armature_obj.animation_data.drivers:
            success = simplified_armature_obj.driver_remove(driver.data_path, -1)
            
        # --- delete unneeded bones -----------------
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        delete_bones = []
        for arm_bone in simplified_armature.edit_bones:
            #print('arm_bone.name: ' + arm_bone.name)
            b_found = False
            for bone_entry in bone_hierarchy:
                if arm_bone.name == bone_entry[0]:
                    b_found = True
                    break
                
            if not b_found:
                #print('DELETE: ' + arm_bone.name)
                delete_bones.append(arm_bone)

        for delete_bone in delete_bones:
            simplified_armature.edit_bones.remove(delete_bone)
        
        # --- update bone hierarchy -----------------
        for edit_bone in simplified_armature.edit_bones:
            for bone_entry in bone_hierarchy:
                if edit_bone.name == bone_entry[0] and bone_entry[1] != None:
                    edit_bone.parent = simplified_armature.edit_bones[bone_entry[1]]
                    edit_bone.use_connect = bone_entry[2]
                    edit_bone.use_inherit_rotation = False  # works fine w/o these. 
                    edit_bone.use_inherit_scale = False     # otherwise, I don't know why work w/o these.
                    
                    if not bone_entry[2]:
                        edit_bone.use_local_location = False
                        
                    break

        # --- rename bones --------------------------
        for edit_bone in simplified_armature.edit_bones:
            for bone_entry in bone_hierarchy:
                if edit_bone.name == bone_entry[0]:
                    edit_bone.name = bone_entry[3]
                    break
        
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
    else: print("ERROR: Rigify armture invalid")
    
    print('# Simplify Rigify Armature : Done!                    #')
    print('#######################################################')
    
#    bpy.context.area.type = 'TEXT_EDITOR'

    return simplified_armature_obj

#======================================================================
def DeletePoseLib(simplified_armature_obj):
#    bpy.context.area.type = '?'
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    if simplified_armature_obj.pose_library:
#        print(simplified_armature_obj.pose_library.name)        
#        for i in range(0, len(simplified_armature_obj.pose_library.pose_markers)):
#            print(simplified_armature_obj.pose_library.pose_markers[i].name)

        original_context = bpy.context.area.type
        bpy.context.area.type = 'PROPERTIES'
    
        simplified_armature_obj.select_set(True)
        simplified_armature_obj.pose_library = simplified_armature_obj.pose_library.copy()
        bpy.ops.poselib.unlink()

        bpy.context.area.type = original_context

#======================================================================
def DeleteBoneGroups(simplified_armature_obj):
    bpy.ops.object.mode_set(mode = 'POSE')

    bone_groups = []
    if simplified_armature_obj.pose.bone_groups:
        for i in range(0, len(simplified_armature_obj.pose.bone_groups)):
            bone_groups.append(simplified_armature_obj.pose.bone_groups.values()[i])

        for i in range(0, len(bone_groups)):
            simplified_armature_obj.pose.bone_groups.remove(bone_groups[i])
        
    bpy.ops.object.mode_set(mode = 'OBJECT')

#======================================================================    
def MoveToCollection(obj, collection_name):
    if obj and collection_name:
        old_colls = obj.users_collection
        for coll in old_colls:
            bpy.data.collections[coll.name].objects.unlink(obj)
            
        bpy.data.collections[collection_name].objects.link(obj)
        
        DeselectAll()
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

#======================================================================
def CopyMesh(mesh_obj):
    DeselectAll()
    new_mesh_obj = None
    
    if mesh_obj:
#        bpy.context.area.type = 'VIEW_3D'
#        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        bpy.context.view_layer.objects.active = mesh_obj
        mesh_obj.select_set(True)
        bpy.ops.object.duplicate({"linked" : False})
        new_mesh_obj = bpy.context.selected_objects[0]
#        print(new_mesh_obj.name)
        
        new_mesh_obj.name = new_mesh_obj_name
        new_mesh_obj.data.name = new_mesh_name
        
    return new_mesh_obj

#======================================================================
def RenameVertexGroups(mesh_obj):
    if mesh_obj:
        bone_hierarchy = GetBoneHierarchy()
        for bone_entry in bone_hierarchy:
            if bone_entry[0] in mesh_obj.vertex_groups:
                mesh_obj.vertex_groups[bone_entry[0]].name = bone_entry[3]
    

#======================================================================
def ReparentMesh(mesh_obj, armature_obj):
    if mesh_obj and armature_obj:
        mesh_obj.parent = armature_obj
        mesh_obj.modifiers["Armature"].object = armature_obj

#======================================================================
def main():
    print('#######################################################')

    # --- purge all objects without users -------
    bpy.ops.outliner.orphans_purge()
    
#    rigify_armature_obj = bpy.context.scene.objects.get(rigify_armature_obj_name)
    rigify_armature_obj = selected_armature_obj
    
    if not(rigify_armature_obj):
        print("ERROR: Rigify armature does not exist")
        return
    else:
        simplified_armature_obj = bpy.context.scene.objects.get(simplified_armature_obj_name)

        if simplified_armature_obj:
            print("ERROR: Simplified armature already exists")
            return
        else: 
            simplified_armature_obj = SimplifyRigifyArmature(rigify_armature_obj)
            DeletePoseLib(simplified_armature_obj)
            DeleteBoneGroups(simplified_armature_obj)
            MoveToCollection(simplified_armature_obj, tgt_collection_name)
        
    mesh_obj = selected_mesh_obj
    new_mesh_obj = CopyMesh(mesh_obj)
    
    if new_mesh_obj:
        RenameVertexGroups(new_mesh_obj)
        ReparentMesh(new_mesh_obj, simplified_armature_obj)
        MoveToCollection(new_mesh_obj, tgt_collection_name)

    # --- purge all objects without users -------
    bpy.ops.outliner.orphans_purge()
    
    DeselectAll()
#    print(bpy.context.mode)
#    print(bpy.context.area.type)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    DeselectAll()
#    rigify_armature_obj.select_set(True)
#    simplified_armature_obj.select_set(True)
#    bpy.context.view_layer.objects.active = simplified_armature_obj
    
#    simplified_armature_obj = bpy.data.objects[simplified_armature_obj_name]
    
    
    print('#######################################################')

#======================================================================
def validate():
    global selected_armature_obj, selected_mesh_obj

    sel_cnt = len(bpy.context.selected_objects)
    
    if sel_cnt == 0:
        print("Warning: Nothing selected. Please select an armature and a mesh")
        return False
    
    if sel_cnt != 2:
        print("Warning: Invalid selection count. Please select an armature and a mesh")
        return False
    
    selectObjs = bpy.context.selected_objects
    
    arm_cnt = 0
    mesh_cnt = 0

    for obj in selectObjs:
        print(obj.type)
        if obj.type == 'ARMATURE':
            selected_armature_obj = obj
            arm_cnt += 1
        if obj.type == 'MESH':
            selected_mesh_obj = obj
            mesh_cnt += 1

    if arm_cnt != 1:
        print("Warning: Invalid selected armature count. One expected.")
        return False
    if mesh_cnt != 1:
        print("Warning: Invalid selected mesh count. One expected.")
        return False
    
    return True

#======================================================================
if validate():
    main()





