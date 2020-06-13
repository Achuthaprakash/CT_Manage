from django.shortcuts import render
from .forms import *
from .models import *
from django.db.models import Q
import ast
# import matploblib.pyplot as plt
import seaborn as sns
import pandas as pd
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.db.models import Subquery as sqr
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
# Create your views here.


# def base(request):
#     return render(request, 'base')
#
# def register(request):
#     registered = False
#     user_form = UserForm()
#     if request.method == "POST":
#         user_form = UserForm(data = request.POST)
#         if user_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#             registered = True
#         else:
#             print(user_form.errors)
#     context = {'user_form':user_form,
#                'registered':registered}
#     return render(request, 'kaju/registration.html',context=context)


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

    context = {'process':form}
    return render(request,'kaju/add_country.html',context=context)


def add_region(request):
    form = region_form()
    if request.method =="POST" :
        form = region_form(request.POST)
        if form.is_valid():
            form.save(commit=True)



    context = {'process': form}
    return render(request, 'kaju/add_region.html', context=context)


def bucket_vw(request):
    form = bucket_form()
    if request.method =="POST" :
        form = bucket_form(request.POST)
        if form.is_valid():
            form.save(commit=True)


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
    my_data = processing_lot.objects.all()[2:7]
    my_data_frame = pd.DataFrame(my_data.values())
    # my_data_frame.to_excel('my_data.xlsx')
    piece_per = my_data_frame.pieces*100/(my_data_frame.wholes+my_data_frame.pieces)
    plot = sns.lineplot(x=my_data_frame.lot_name,y=piece_per).get_figure()
    plot.savefig("D:\Production\Production\production_kaju\kaju\static\img\plots\pieces_per.png")
    print(my_data_frame)

    context = {'data': my_data}

    return render(request,'kaju/processing.html',context=context)


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
            lot_qty =lot_qty - float(pro_qty)+lot_pro_qty
            pro_qty_up = float(pro_qty)
            # print('\n\n\n\n qty:', lot_qty)
            lot_qry.update(quantity = pro_qty_up)
            lot_qry.update(processed = lot_qty)

            #SHELLS
            lot_shell_qry = processing_lot.objects.filter(lot_id=lot).values('shells')
            lot_shell_qty = lot_shell_qry[0]['shells']
            # print('\n\n\n\n\ qty',lot_pro_qty)
            shell_qty = request.POST.get('shells_output')
            shell_qty_up = float(shell_qty) + lot_shell_qty
            # print('\n\n\n\n qty:', lot_qty)
            lot_shell_qry.update(shells=float(shell_qty_up))

            #WHOLES
            lot_wholes_qry = processing_lot.objects.filter(lot_id=lot).values('wholes')
            lot_wholes_qty = lot_wholes_qry[0]['wholes']
            wholes_qty = request.POST.get('wholes')
            wholes_qty_up = float(wholes_qty) + lot_wholes_qty
            lot_wholes_qry.update(wholes = wholes_qty_up)

            # PIECES
            lot_pieces_qry = processing_lot.objects.filter(lot_id=lot).values('pieces')
            lot_pieces_qty = lot_pieces_qry[0]['pieces']
            # print('\n\n\n\n Pieces:',lot_pieces_qty)
            pieces_qty = request.POST.get('pieces')
            pieces_qty_up = float(pieces_qty) + lot_pieces_qty
            # print('\n\n\n\n Pieces:', pieces_qty_up)
            lot_pieces_qry.update(pieces=pieces_qty_up)

            # REJECTION
            lot_rejection_qry = processing_lot.objects.filter(lot_id=lot).values('rejection')
            lot_rejection_qty = lot_rejection_qry[0]['rejection']
            rejection_qty = request.POST.get('rejections')
            rejection_qty_up = float(rejection_qty) + lot_rejection_qty
            lot_rejection_qry.update(rejection=rejection_qty_up)


            # FOREIGN
            lot_foreign_particles_qry = processing_lot.objects.filter(lot_id=lot).values('foreign_particles')
            # print('\n\n\n fp:',lot_foreign_particles_qry)
            lot_foreign_particles_qty = lot_foreign_particles_qry[0]['foreign_particles']
            # print('\n\n\n\n lfp;',lot_foreign_particles_qty)
            foreign_particles_qty = request.POST.get('foreign_particles')
            foreign_particles_qty_up = float(foreign_particles_qty) + lot_foreign_particles_qty
            lot_foreign_particles_qry.update(foreign_particles=foreign_particles_qty_up)

            # PROCESS TOTAL
            lot_process_total_qry = processing_lot.objects.filter(lot_id=lot).values('process_total')
            lot_process_total_qty = lot_process_total_qry[0]['process_total']
            process_qty = lot_process_total_qty + foreign_particles_qty_up + rejection_qty_up + pieces_qty_up + wholes_qty_up + shell_qty_up
            lot_process_total_qry.update(process_total = process_qty)

            # LOT OUT TURN
            lot_out_turn_qry = processing_lot.objects.filter(lot_id =lot).values('out_turn')
            qty_for_ot = wholes_qty_up + pieces_qty_up
            # print('\n\n\n\n qty:',qty_for_ot)
            qty_for_ot = qty_for_ot*80*2.23/lot_qty
            # print('\n\n\n\n ot:',qty_for_ot)
            lot_out_turn_qry.update(out_turn = qty_for_ot)

            #LOT ADJ
            lot_adj_qry = processing_lot.objects.filter(lot_id=lot).values('adj_cutting')
            # print('\n\n\n process_qty:',lot_qty)
            # print('\n\n\n process_qty_aft:', process_qty)
            adj_qty = lot_qty - process_qty
            lot_adj_qry.update(adj_cutting = adj_qty)

            form.save(commit=True)

    context = {'process':form}

    return render(request, 'kaju/cutting.html', context=context)

def bormah(request):
    form = bormah_form()
    if request.method == "POST":
        form = bormah_form(request.POST)
        if form.is_valid():
            form.save(commit=True)
            lot = request.POST.get('bormah_lot')
            lot_wholes_qry = processing_lot.objects.filter(lot_id = lot).values('dried_wholes')
            lot_pieces_qry = processing_lot.objects.filter(lot_id=lot).values('dried_pieces')
            lot_wholes_qty = lot_wholes_qry[0]['dried_wholes']
            lot_pieces_qty = lot_pieces_qry[0]['dried_pieces']
            form_wholes = request.POST.get('dried_wholes')
            form_pieces = request.POST.get('dried_pieces')
            wholes_up = lot_wholes_qty + float(form_wholes)
            pieces_up = lot_pieces_qty + float(form_pieces)

            lot_wholes_qry.update(dried_wholes = wholes_up)
            lot_pieces_qry.update(dried_pieces = pieces_up)


    context = {'process': form}
    return render(request, 'kaju/bormah.html', context=context)



def peeling(request):
    form = peeling_form()
    if request.method == "POST":
        form = peeling_form(request.POST)
        if form.is_valid():
            lot = request.POST.get('peeling_lot')
            lot_wholes_qry = processing_lot.objects.filter(lot_id = lot).values('final_output')
            lot_rejection_qry = processing_lot.objects.filter(lot_id=lot).values('rejection')
            lot_final_qty = lot_wholes_qry[0]['final_output']
            lot_rejects_qty = lot_rejection_qry[0]['rejection']
            form_wholes = request.POST.get('peeled_wholes')
            form_pieces = request.POST.get('peeled_pieces')
            form_rejection = request.POST.get('rejections')
            final_output_up = lot_final_qty + float(form_wholes)+float(form_pieces)
            rejection_up = lot_rejects_qty + float(form_rejection)

            form_husk = request.POST.get('husk')
            lot_husk_qry = processing_lot.objects.filter(lot_id = lot).values('husk')
            lot_husk_qty = lot_husk_qry[0]['husk']
            husk_up = lot_husk_qty + float(form_husk)

            lot_wholes_qry.update(final_output = final_output_up)
            lot_rejection_qry.update(rejection = rejection_up)
            lot_husk_qry.update(husk = husk_up)

            form.save(commit=True)
    context = {'process': form}
    return render(request, 'kaju/bormah.html', context=context)


def add_grade(request):
    form = grade_name_form()

    if request.method =="POST" :
        form = grade_name_form(request.POST)
        if form.is_valid():
            form.save(commit=True)
            # return HttpResponseRedirect(reverse('index'))
    context = {'process':form}
    return render(request,'kaju/add_grade.html',context=context)

def grading(request):
    form_grade = grading_form()
    grades = grade_names.objects.all()
    grade_n_ls = []
    invalues_ls = []
    if request.method == "POST" :
        form_grade = grading_form(request.POST)
        for i in range(len(grades)):
            in_name = "grade-"+str(i+1)
            in_value = request.POST.get(in_name)
            grades_n = grades.filter(grad_id = i+1).values('grade_names')
            grades_n = grades_n[0]['grade_names']
            grade_n_ls.append(grades_n)
            invalues_ls.append(in_value)
        grade_list = dict(zip(grade_n_ls,invalues_ls))
        form_grade.save()
        grade_lot = request.POST.get('grading_lot')
        lot_qry = grading_section.objects.filter(grading_lot = grade_lot )
        lot_qry.update(grading_output = grade_list)


        lot_qry = processing_lot.objects.filter(lot_id = grade_lot).values('grading_consolidation')
        consol = lot_qry[0]['grading_consolidation']

        if consol == 'NA':
            lot_qry.update(grading_consolidation = grade_list)
            print("I am Here")

        else:
            print(consol)
            consol = ast.literal_eval(consol)
            added_qty = []
            for grade in grade_n_ls:
                print (grade)
                qty_total = int(consol[grade])+ int(grade_list[grade])
                added_qty.append(qty_total)
                print(qty_total)

            consol_qty = dict(zip(grade_n_ls,added_qty))
            lot_qry.update(grading_consolidation = consol_qty)
            print(consol_qty)
            print('I am not there')

    context = {'grades':grades,
               'process':form_grade}
    return render(request, 'kaju/grading.html',context=context)

def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('base'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'kaju/login.html', {})
    # return render(request, 'kaju/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('kaju/base.html'))