
import idaapi

class Hooks(idaapi.UI_Hooks):

    def __init__(self, act_id_list):
        idaapi.UI_Hooks.__init__(self)
        self._act_id_list = act_id_list
        
    def populating_tform_popup(self, form, popup):
        # You can attach here.
        pass

    def finish_populating_tform_popup(self, form, popup):
        # Or here, after the popup is done being populated by its owner.

        # We will attach our action to the context menu
        # for the 'Diassembler and Hex Dump views' widget.
        # The action will be be inserted in a submenu of
        # the context menu, named 'Others'.
        if idaapi.get_tform_type(form) == idaapi.BWN_DISASM or \
           idaapi.get_tform_type(form) == idaapi.BWN_DUMP:
            for act_id in self._act_id_list:
                idaapi.attach_action_to_popup(form, popup, act_id, "Fentanyl/")
