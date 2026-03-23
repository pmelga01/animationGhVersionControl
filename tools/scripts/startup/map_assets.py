import bpy
import os
import addon_utils
from bpy.app.handlers import persistent

# --- 1. DEFINE UTILITIES FIRST ---

def update_bookmarks(bookmark_name, target_path):
    """Adds or updates a sidebar bookmark and forces a UI refresh."""
    if not os.path.exists(target_path):
        os.makedirs(target_path, exist_ok=True)
        
    bookmarks = bpy.context.preferences.filepaths.bookmarks
    
    found = False
    for bm in bookmarks:
        if bm.name == bookmark_name:
            bm.path = target_path
            found = True
            break
    
    if not found:
        new_bm = bookmarks.add()
        new_bm.name = bookmark_name
        new_bm.path = target_path
        print(f"DEBUG: Created Bookmark: {bookmark_name}")

    # --- ADD THESE TWO LINES TO FORCE THE SIDEBAR TO UPDATE ---
    bpy.ops.wm.save_userpref() # Saves the change to your tools/config folder
    for area in bpy.context.screen.areas:
        area.tag_redraw() # Tells Blender to visually refresh the UI


# --- 2. STARTUP SYNC ---

def sync_project_paths():
    startup_dir = os.path.dirname(__file__)
    scripts_dir = os.path.dirname(startup_dir)
    tools_dir = os.path.dirname(scripts_dir)
    repo_root = os.path.dirname(tools_dir)
    project_root = os.path.dirname(repo_root)
    
    shared_dir = os.path.join(project_root, "shared")
    shared_assets_root = os.path.join(shared_dir, "assets")
    local_dir = os.path.join(project_root, "local")

    # WIP Render dir
    wip_render_dir = os.path.join(shared_dir, "renders", "work_in_progress")

    prefs = bpy.context.preferences.filepaths
    
    # Set Global Directories
    prefs.texture_directory = os.path.join(shared_dir, "textures")
    prefs.sound_directory = os.path.join(shared_dir, "audio")
    prefs.font_directory = os.path.join(shared_dir, "fonts") 
    
    temp_path = os.path.join(local_dir, "temp")
    if not os.path.exists(temp_path):
        os.makedirs(temp_path, exist_ok=True)
    prefs.temporary_directory = temp_path

    # INITIAL BOOKMARK SYNC
    update_bookmarks("PROJECT_WIP_RENDERS", wip_render_dir)

    # Sync Asset Libraries
    if os.path.exists(shared_assets_root):
        asset_folders = [f for f in os.listdir(shared_assets_root) if os.path.isdir(os.path.join(shared_assets_root, f))]
        for folder_name in asset_folders:
            full_path = os.path.join(shared_assets_root, folder_name)
            found = False
            for lib in prefs.asset_libraries:
                if lib.name == folder_name:
                    lib.path = full_path
                    lib.import_method = 'LINK' 
                    found = True
                    break
            if not found:
                bpy.ops.preferences.asset_library_add(directory=full_path)
                new_lib = prefs.asset_libraries[-1]
                new_lib.name = folder_name
                new_lib.import_method = 'LINK'

    print(f"DEBUG: Startup sync complete for {project_root}")

# --- 3. PER-SHOT SYNC ---

@persistent
def auto_set_render_path(dummy):
    blend_file = bpy.data.filepath
    if not blend_file or "shots" not in blend_file:
        return

    # Resolve Paths
    current_dir = os.path.dirname(blend_file)
    shots_root = os.path.dirname(current_dir)
    repo_root = os.path.dirname(shots_root)
    project_root = os.path.dirname(repo_root)

    shared_shots_root = os.path.join(project_root, "shared", "shots")
    rel_path_from_shots = os.path.relpath(blend_file, shots_root)
    shot_folder_name = os.path.splitext(rel_path_from_shots)[0]

    target_render_dir = os.path.join(shared_shots_root, shot_folder_name, "renders")

    if not os.path.exists(target_render_dir):
        os.makedirs(target_render_dir, exist_ok=True)

    # 1. Set the Render Output (Printer Tab)
    bpy.context.scene.render.filepath = target_render_dir + os.sep
    
    # 2. Update the dynamic Shot Bookmark
    update_bookmarks("CURRENT_SHOT_RENDERS", target_render_dir)
    
    print(f"TD DEBUG: Shot Renders linked to: {target_render_dir}")

# --- 4. REGISTRATION ---

def enable_standard_addons():
    must_have = ["node_wrangler", "rigify"]
    for addon in must_have:
        is_enabled, _ = addon_utils.check(addon)
        if not is_enabled:
            try:
                addon_utils.enable(addon, default_visibility=True)
                print(f"DEBUG: Enabled {addon}")
            except:
                pass

# Clear old handlers to avoid duplicates
bpy.app.handlers.load_post.clear()
bpy.app.handlers.load_post.append(auto_set_render_path)

# Execute
sync_project_paths()
enable_standard_addons()
