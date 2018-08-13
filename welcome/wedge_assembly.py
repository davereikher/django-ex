from .common import wedge_page_render
from .wedge_selection import wedge_selection

def assembly(request):
    if 'wedge_id' not in request.session:
        return wedge_selection(request)

    WedgeAssemblyFormSet = get_wedge_assembly_form_set_factory()
    formset = WedgeAssemblyFormSet()

    return wedge_page_render(request, "assembly", "assembly", {'formset': formset})


