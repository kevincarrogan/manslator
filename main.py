import random

from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from translations import translations

templates = Jinja2Templates(directory='templates')

def slugify(string):
    return string.lower().replace(" ", "-")

def get_context_data(request, man, woman, perm=False):
    permalink = request.url_for(
        "permalink",
        man=slugify(man),
        woman=slugify(woman),
    )

    title = "Manslator"
    if perm:
        title = f"Manslator - {man} is {woman}"

    return {
        "man": man,
        "woman": woman,
        "permalink": permalink,
        "perm": perm,
        "title": title,
        "description": "Are you confused with how to talk to and about women? Here is your helpful manslator.",
        "request": request,
    }

def permalink(request):
    man = request.path_params['man']
    woman = request.path_params['woman']

    try:
        translation = routes[(man, woman)]
    except KeyError:
        return Response('Not found', status_code=404)
    else:
        man, woman = translation

        return templates.TemplateResponse(
            'translation.html',
            get_context_data(request, man, woman),
        )

def home(request):
    man, woman = random.choice(translations)

    return templates.TemplateResponse(
        'translation.html',
        get_context_data(request, man, woman),
    )

routes = [
    Route('/', home),
    Route('/{man}-is-{woman}/', permalink),
    Mount('/static', StaticFiles(directory='static')),
]

app = Starlette(debug=True, routes=routes)
