from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import ClienteForm, MaquinaForm, ReparacionForm, DetalleReparacionFormSet
from .models import Cliente, Maquina, Reparacion


def inicio(request):
    return render(request, "maquinas/inicio.html")

def lista_maquinas(request):
    maquinas = Maquina.objects.all()
    return render(request, 'maquinas/lista_maquinas.html', {'maquinas': maquinas})

def registrar_cliente(request):
    if request.method == "POST":
        cliente_form = ClienteForm(request.POST)
        maquina_form = MaquinaForm(request.POST)
        if cliente_form.is_valid() and maquina_form.is_valid():
            cliente, _ = Cliente.objects.get_or_create(
                telefono=cliente_form.cleaned_data["telefono"],
                defaults={
                    "nombre": cliente_form.cleaned_data["nombre"],
                    "apellido": cliente_form.cleaned_data["apellido"],
                },
            )
            maquina = maquina_form.save(commit=False)
            maquina.cliente = cliente
            maquina.save()
            messages.success(request, "Cliente y máquina registrados correctamente.")
            return redirect("inicio")
    else:
        cliente_form = ClienteForm()
        maquina_form = MaquinaForm()

    return render(
        request, "maquinas/registro_cliente.html",
        {"cliente_form": cliente_form, "maquina_form": maquina_form}
    )

def lista_clientes(request):
    clientes = Cliente.objects.prefetch_related('maquinas').all()
    return render(request, "maquinas/lista_clientes.html", {"clientes": clientes})

def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    messages.success(request, "Cliente eliminado correctamente.")
    return redirect("lista_clientes")

def buscar_cliente(request):
    query = request.GET.get("q", "")
    clientes = Cliente.objects.filter(
        Q(apellido__icontains=query) | Q(nombre__icontains=query) | Q(telefono__icontains=query)
    ) if query else []
    return render(request, "maquinas/buscar_cliente.html", {"clientes": clientes})

def registrar_reparacion(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    maquinas = Maquina.objects.filter(cliente=cliente)

    if request.method == "POST":
        reparacion_form = ReparacionForm(request.POST)
        formset = DetalleReparacionFormSet(request.POST)

        if reparacion_form.is_valid() and formset.is_valid():
            reparacion = reparacion_form.save(commit=False)
            reparacion.maquina = maquinas.first()  # Puedes ajustar esto si es necesario.
            reparacion.save()

            for form in formset:
                detalle = form.save(commit=False)
                detalle.reparacion = reparacion
                detalle.save()

            messages.success(request, "Reparación registrada correctamente.")
            return redirect("lista_reparaciones")
    else:
        reparacion_form = ReparacionForm()
        formset = DetalleReparacionFormSet()

    return render(
        request,
        "registro_reparacion.html",
        {"reparacion_form": reparacion_form, "formset": formset, "cliente": cliente},
    )
    
def lista_reparaciones(request):
    reparaciones = Reparacion.objects.select_related('maquina').all()
    return render(request, "maquinas/lista_reparaciones.html", {"reparaciones": reparaciones})
