from .common import wedge_page_render

def wiring(request):
    return wedge_page_render(request, 'wiring_1', 'wiring')

