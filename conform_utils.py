import bpy
from bpy.types import Operator


bl_info = {
    "name": "Conform utils",
    "author": "Roman Volodin",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "Sequence Editor -> F shortcut",
    "description": "Набор скриптов для удобного конформа материалов в видеоредакторе Блендера",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Sequencer",
}


def filter_selected_strips(context, types=("MOVIE",)):
    selected_strips = [strip for strip in context.selected_sequences if strip.type in types]
    if selected_strips:
        return selected_strips


class SearchStrip(Operator):
    bl_idname = "sequence.search_strip"
    bl_label = "Search strip"
    bl_options = {"REGISTER", "UNDO"}

    name: bpy.props.StringProperty()

    def execute(self, context):
        if not self.name:
            return {"FINISHED"}

        bpy.ops.sequencer.select_all(action="DESELECT")

        scene = context.scene
        for strip in scene.sequence_editor.sequences_all:
            if self.name in strip.name:
                scene.frame_current = strip.frame_final_start
                strip.select = True
                bpy.ops.sequencer.view_selected()

        return {"FINISHED"}


addon_keymaps = []


def register():
    bpy.utils.register_class(SearchStrip)

    window_manager = bpy.context.window_manager
    keyconfig = window_manager.keyconfigs.addon
    if keyconfig:
        keymap = keyconfig.keymaps.new(name="SequencerCommon", space_type="SEQUENCE_EDITOR")
        keymap_item = keymap.keymap_items.new("sequence.search_strip", type="F", value="PRESS")
        addon_keymaps.append((keymap, keymap_item))


def unregister():
    bpy.utils.unregister_class(SearchStrip)

    for keymap, keymap_item in addon_keymaps:
        keymap.keymap_items.remove(keymap_item)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
