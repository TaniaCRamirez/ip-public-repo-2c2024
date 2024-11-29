# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request):
    images = services.getAllImages() #Trae un lista con todos los personajes al cargar la galeria
    favourite_list = [services.getAllFavourites(request)]
    

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })


def search(request):
    # Obtiene el texto ingresado en el campo de búsqueda del formulario
    search_msg = request.POST.get('query', '')

    if not search_msg:  # Verifica si el término de búsqueda está vacío
        # Si no se ingresó nada, redirige a la página de inicio
        return redirect('home')
    else:
        # Busca imágenes relacionadas con el término ingresado llamando a una función en services.py
        images = services.getAllImages(search_msg)

        # Muestra la página de inicio con las imágenes encontradas
        return render(request, 'home.html', {'images': images})



# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services.getAllFavourites(request)

    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    save = services.saveFavourite(request)
    favourite_list = services.getAllFavourites(request)
    return render(request, 'favourites.html', { 'favourite_list': favourite_list  })

@login_required
def deleteFavourite(request):
    delete = services.deleteFavourite(request)
    favourite_list = services.getAllFavourites(request)
    return render(request, 'favourites.html', { 'favourite_list': favourite_list  })


# función encargada del logout

@login_required
def exit(request):
   logout(request) # se encarga de cerrar la sesión
   return redirect ('home') # Regresa al usuario a la página de bienvenida