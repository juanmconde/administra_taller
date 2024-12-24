from django.shortcuts import get_object_or_404, redirect, render
from .models import Cliente, Reparacion, DetalleReparacion, Maquina
from .forms import ReparacionForm, ClienteForm, MaquinaForm, DetalleReparacionFormSet
from django.contrib import messages


def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect("lista_clientes")
    else:
        form = ClienteForm(instance=cliente)
    return render(request, "maquinas/editar_cliente.html", {"form": form})

def registrar_maquina(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == "POST":
        form = MaquinaForm(request.POST)
        if form.is_valid():
            maquina = form.save(commit=False)
            maquina.cliente = cliente
            maquina.save()
            return redirect('lista_clientes')  # Cambia esto si necesitas redirigir a otro lugar
    else:
        form = MaquinaForm()

    return render(request, 'maquinas/registrar_maquina.html', {'form': form, 'cliente': cliente})

def agregar_maquina_cliente(request):
    if request.method == "POST":
        maquina_form = MaquinaForm(request.POST)

        if maquina_form.is_valid():
            cliente_id = request.POST.get("cliente_id")
            cliente = get_object_or_404(Cliente, id=cliente_id)

            maquina = maquina_form.save(commit=False)
            maquina.cliente = cliente
            maquina.save()

            messages.success(request, "Máquina agregada al cliente.")
            return redirect("inicio")  # Cambia esto por la URL adecuada
    else:
        maquina_form = MaquinaForm()
        clientes = Cliente.objects.all()

    return render(
        request,
        "agregar_maquina_cliente.html",
        {"maquina_form": maquina_form, "clientes": clientes},
    )


def registrar_cliente_maquina(request):
    if request.method == "POST":
        cliente_form = ClienteForm(request.POST)
        maquina_form = MaquinaForm(request.POST)

        if cliente_form.is_valid() and maquina_form.is_valid():
            cliente = cliente_form.save()
            maquina = maquina_form.save(commit=False)
            maquina.cliente = cliente  # Asocia la máquina al cliente recién creado
            maquina.save()

            messages.success(request, "Cliente y máquina registrados correctamente.")
            return redirect("inicio")  # Cambia esto por la URL a la que quieras redirigir
    else:
        cliente_form = ClienteForm()
        maquina_form = MaquinaForm()

    return render(
        request,
        "registrar_cliente_maquina.html",
        {"cliente_form": cliente_form, "maquina_form": maquina_form},
    )

def registrar_reparacion(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == "POST":
        reparacion_form = ReparacionForm(request.POST, cliente=cliente)
        detalle_formset = DetalleReparacionFormSet(request.POST)
        if reparacion_form.is_valid() and detalle_formset.is_valid():
            reparacion = reparacion_form.save(commit=False)
            reparacion.cliente = cliente
            reparacion.save()
            detalle_formset.instance = reparacion
            detalle_formset.save()
            return redirect('lista_reparaciones')
    else:
        reparacion_form = ReparacionForm(cliente=cliente)
        detalle_formset = DetalleReparacionFormSet()

    return render(request, "maquinas/registrar_reparacion.html", {
        "cliente": cliente,
        "reparacion_form": reparacion_form,
        "detalle_formset": detalle_formset,
    })
    
# def registrar_reparacion(request, cliente_id):
#     cliente = get_object_or_404(Cliente, id=cliente_id)
#     if request.method == "POST":
#         reparacion_form = ReparacionForm(request.POST, cliente=cliente)
#         detalle_formset = DetalleReparacionFormSet(request.POST)
#         if reparacion_form.is_valid() and detalle_formset.is_valid():
#             reparacion = reparacion_form.save(commit=False)
#             reparacion.cliente = cliente
#             reparacion.save()
#             detalles = detalle_formset.save(commit=False)
#             for detalle in detalles:
#                 detalle.reparacion = reparacion
#                 detalle.save()
#             return redirect("inicio")  # Ajusta esta URL según tu configuración
#     else:
#         reparacion_form = ReparacionForm(cliente=cliente)
#         detalle_formset = DetalleReparacionFormSet()

#     return render(request, "registrar_reparacion.html", {
#         "reparacion_form": reparacion_form,
#         "detalle_formset": detalle_formset,
#         "cliente": cliente
#     })



def inicio(request):
    return render(request, "maquinas/inicio.html")


def lista_maquinas(request):
    maquinas = Maquina.objects.all()
    return render(request, "maquinas/lista_maquinas.html", {"maquinas": maquinas})


def registrar_cliente(request):
    if request.method == "POST":
        cliente_form = ClienteForm(request.POST)
        maquina_form = MaquinaForm(request.POST)

        # Verificar si ya existe un cliente con el mismo teléfono
        if cliente_form.is_valid() and maquina_form.is_valid():
            telefono = cliente_form.cleaned_data["telefono"]
            cliente = Cliente.objects.filter(telefono=telefono).first()

            if not cliente:  # Si no existe, creamos el cliente
                cliente = cliente_form.save()

            # Asociar la máquina al cliente existente o recién creado
            maquina = maquina_form.save(commit=False)
            maquina.cliente = cliente
            maquina.save()

            messages.success(request, "Cliente y máquina registrados correctamente.")
            return redirect("inicio")  # Cambia esto por tu URL de inicio o lista de clientes
    else:
        cliente_form = ClienteForm()
        maquina_form = MaquinaForm()

    return render(
        request,
        "registrar_cliente.html",
        {"cliente_form": cliente_form, "maquina_form": maquina_form},
    )


def lista_clientes(request):
    clientes = Cliente.objects.prefetch_related("maquinas").all()
    return render(request, "maquinas/lista_clientes.html", {"clientes": clientes})


def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    messages.success(request, "Cliente eliminado correctamente.")
    return redirect("lista_clientes")


def buscar_cliente(request):
    query = request.GET.get("q", "")
    clientes = (
        Cliente.objects.filter(
            Q(apellido__icontains=query)
            | Q(nombre__icontains=query)
            | Q(telefono__icontains=query)
        )
        if query
        else []
    )
    return render(request, "maquinas/buscar_cliente.html", {"clientes": clientes})


def lista_reparaciones(request):
    reparaciones = Reparacion.objects.select_related("maquina").all()
    return render(
        request, "maquinas/lista_reparaciones.html", {"reparaciones": reparaciones}
    )

def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    maquinas = cliente.maquinas.all()  # Relación inversa para obtener las máquinas del cliente

    if request.method == "POST":
        form = MaquinaForm(request.POST)
        if form.is_valid():
            maquina = form.save(commit=False)
            maquina.cliente = cliente  # Asociar la nueva máquina al cliente
            maquina.save()
            return redirect("detalle_cliente", cliente_id=cliente.id)
    else:
        form = MaquinaForm()

    return render(request, "detalle_cliente.html", {"cliente": cliente, "maquinas": maquinas, "form": form})