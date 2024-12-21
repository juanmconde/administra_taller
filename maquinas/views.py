from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Cliente, Maquina, Reparacion
from .forms import ClienteForm, MaquinaForm, ReparacionForm

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, "maquinas/lista_clientes.html", {"clientes": clientes})

def registrar_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_clientes")
    else:
        form = ClienteForm()
    return render(request, "maquinas/agregar_cliente.html", {"form": form})


def registrar_maquina(request):
    if request.method == "POST":
        form = MaquinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_maquinas")
    else:
        form = MaquinaForm()
    return render(request, "agregar_maquina.html", {"form": form})

def buscar_cliente(request):
    query = request.GET.get("q", "")
    clientes = Cliente.objects.filter(nombre__icontains=query)
    return render(request, "buscar_cliente.html", {"clientes": clientes})

def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    return redirect("lista_clientes")

def lista_maquinas(request):
    maquinas = Maquina.objects.all()
    return render(request, "lista_maquinas.html", {"maquinas": maquinas})

def lista_reparaciones(request):
    reparaciones = Reparacion.objects.all()
    return render(request, "lista_reparaciones.html", {"reparaciones": reparaciones})

def imprimir_reparacion(request, pk):
    reparacion = get_object_or_404(Reparacion, pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reparacion_{pk}.pdf"'
    p = canvas.Canvas(response)

    # Encabezado
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "Reporte de Reparación")

    # Información de la reparación
    p.setFont("Helvetica", 12)
    p.drawString(100, 770, f"Cliente: {reparacion.maquina.cliente.nombre} {reparacion.maquina.cliente.apellido}")
    p.drawString(100, 750, f"Máquina: {reparacion.maquina.tipo} - {reparacion.maquina.marca}")
    p.drawString(100, 730, f"Modelo: {reparacion.maquina.modelo}")
    p.drawString(100, 710, f"Problema reportado: {reparacion.problema_reportado}")
    p.drawString(100, 690, f"Solución: {reparacion.solucion}")
    p.drawString(100, 670, f"Fecha de ingreso: {reparacion.fecha_ingreso.strftime('%Y-%m-%d')}")
    p.drawString(100, 650, f"Costo: ${reparacion.costo:.2f}")

    # Finaliza el PDF
    p.showPage()
    p.save()
    return response
