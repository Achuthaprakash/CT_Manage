from django.shortcuts import render
from .forms import *
from .models import *
from django.db.models import Q
from django.views.generic import TemplateView
from django.db.models import Subquery as sqr
from django.http import HttpResponseRedirect
# Create your views here.

def index(request):
    return render(request, 'kaju/index.html')

def add_static(request):
    return render(request,'kaju/Add_static.html')

def add_country(request):
    form = country_form()

    if request.method =="POST" :
        form = country_form(request.POST)
        if form.is_valid():
            form.save(commit=True)
            # return HttpResponseRedirect(reverse('index'))
    context = {'process':form}
    return render(request,'kaju/add_country.html',context=context)


def add_region(request):
    form = region_form()
    if request.method =="POST" :
        form = region_form(request.POST)
        if form.is_valid():
            form.save(commit=True)
        # return HttpResponseRedirect(reverse('index'))


    context = {'process': form}
    return render(request, 'kaju/add_region.html', context=context)


def bucket_vw(request):
    form = bucket_form()
    if request.method =="POST" :
        form = bucket_form(request.POST)
        if form.is_valid():
            form.save(commit=True)
        # return HttpResponseRedirect(reverse('index'))

    context = {'process': form}
    return render(request, 'kaju/bucket.html', context=context)

def dry_rcn(request):
    form = rcn_dry_form()
    if request.method =="POST":
        form = rcn_dry_form(request.POST)
        if form.is_valid():
            bkt = request.POST.get('bin_number')
            print('\n\n\n\n\n bkt',bkt)
            bkt_qry = bucket.objects.filter(bucket_id=bkt).values('quantity')
            print(bkt_qry)
            bkt_qty = bkt_qry[0]['quantity']
            print('\n\n\n\n bucket qu', bkt_qty)
            qty = request.POST.get('quantity_after')
            bkt_qry.update(quantity = float(qty))
            form.save(commit=True)
    context = {'process':form}
    return render(request,'kaju/dry_rcn.html',context=context)

def processing(request):
    return render(request,'kaju/processing.html')


def day_parameters(request):
        form = day_param()
        if request.method =="POST":
            form = day_param(request.POST)
            if form.is_valid():
                form.save(commit=True)
        context = {'process':form}
        return render(request,'kaju/climate.html',context = context)


def cooking(request):
    form = cooking_form()
    td_buck = bucket.objects.filter(~Q(quantity = 0)).order_by('-quantity')[:5]
    # print(td_buck)
    if request.method == "POST":
        form = cooking_form(request.POST)
        if form.is_valid():
            bkt = request.POST.get('bucket')
            # print('\n\n\n',bkt)
            bct_qry = bucket.objects.filter(bucket_id=bkt).values('quantity')
            # print('\n\n\n\n bquery',bct_qry)
            bct_qty = bct_qry[0]['quantity']
            qty_2 = request.POST.get('quantity')
            bct_qty = bct_qty - float(qty_2)
            bct_qry.update(quantity = bct_qty)
            form.save(commit=True)


    context = {'process': form,
               'quantity':td_buck}
    return render(request,'kaju/cooking.html',context = context)

def rcn_avail(request):
    td_buck = bucket.objects.filter(~Q(quantity = 0)).order_by('-quantity')
    context = {'quantity':td_buck}
    return render(request,'kaju/RCN_avail.html',context = context)

def cutting(request):
    form = cut_form()


    if request.method == 'POST':
        form = cut_form(request.POST)
        if form.is_valid():
            lot = request.POST.get('processing_lot')

            #PROCESSED QUANTITY
            # print('\n\n\n len:lot', len(lot),' lot: ',lot)
            lot_qry = processing_lot.objects.filter(lot_id=lot).values('quantity')
            lot_pro_qry = processing_lot.objects.filter(lot_id=lot).values('processed')
            # print('\n\n\n\n\n',lot_qry)
            # print('form is valid')
            lot_qty = lot_qry[0]['quantity']
            lot_pro_qty = lot_pro_qry[0]['processed']
            # print('\n\n\n\n\ qty',lot_pro_qty)
            pro_qty = request.POST.get('pending_quantity')
            if lot_pro_qty:
                lot_qty =lot_qty - float(pro_qty)+lot_pro_qty
            else:
                lot_qty = lot_qty - float(pro_qty)
            # print('\n\n\n\n qty:', lot_qty)
            lot_qry.update(quantity = float(pro_qty))
            lot_qry.update(processed = lot_qty)

            #SHELLS
            lot_shell_qry = processing_lot.objects.filter(lot_id=lot).values('shells')
            lot_shell_qty = lot_shell_qry[0]['shells']
            # print('\n\n\n\n\ qty',lot_pro_qty)
            shell_qty = request.POST.get('shells_output')
            if lot_shell_qty:
                shell_qty_up = float(shell_qty) + lot_shell_qty
            else:
                shell_qty_up = float(shell_qty)
            # print('\n\n\n\n qty:', lot_qty)
            lot_shell_qry.update(shells=float(shell_qty_up))

            #WHOLES
            lot_wholes_qry = processing_lot.objects.filter(lot_id=lot).values('wholes')
            lot_wholes_qty = lot_wholes_qry[0]['wholes']
            wholes_qty = request.POST.get('wholes')
            if lot_wholes_qty:
                wholes_qty_up = float(wholes_qty) + lot_wholes_qty
            else:
                wholes_qty_up = float(wholes_qty)
            lot_wholes_qry.update(wholes = wholes_qty_up)

            # PIECES
            lot_pieces_qry = processing_lot.objects.filter(lot_id=lot).values('pieces')
            lot_pieces_qty = lot_pieces_qry[0]['pieces']
            pieces_qty = request.POST.get('pieces')
            if lot_pieces_qty:
                pieces_qty_up = float(pieces_qty) + lot_pieces_qty
            else:
                pieces_qty_up = float(pieces_qty)
            lot_pieces_qry.update(pieces=pieces_qty_up)

            # REJECTION
            lot_rejection_qry = processing_lot.objects.filter(lot_id=lot).values('rejection')
            lot_rejection_qty = lot_rejection_qry[0]['rejection']
            rejection_qty = request.POST.get('rejections')
            if lot_rejection_qty:
                rejection_qty_up = float(rejection_qty) + lot_rejection_qty
            else:
                rejection_qty_up = float(rejection_qty)
            lot_rejection_qry.update(pieces=rejection_qty_up)


            # FOREIGN
            lot_foreign_particles_qry = processing_lot.objects.filter(lot_id=lot).values('foreign_particles')
            print('\n\n\n fp:',lot_foreign_particles_qry)
            lot_foreign_particles_qty = lot_foreign_particles_qry[0]['foreign_particles']
            print('\n\n\n\n lfp;',lot_foreign_particles_qty)
            foreign_particles_qty = request.POST.get('foreign_particles')
            if lot_foreign_particles_qty:
                foreign_particles_qty_up = float(foreign_particles_qty) + lot_foreign_particles_qty
            else:
                foreign_particles_qty_up = float(foreign_particles_qty)
            lot_foreign_particles_qry.update(pieces=foreign_particles_qty_up)

            form.save(commit=True)

    context = {'process':form}

    return render(request, 'kaju/cutting.html',context=context)

