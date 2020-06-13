 def cooking(request):
#     form_2 = check_bin()
#     form = cooking_form()
#     td_buck = 0
#     # if request.method == "POST":
#     if 'check_qty' in request.POST:
#         form_2 = check_bin(request.POST,prefix='check')
#
#         if form_2.is_valid():
#             print('\n\n\n\nposted\n\n\n\n')
#             bucket_number = form_2.cleaned_data['bucket']
#             print('/n/n/n/n/n bucket name', bucket_number)
#             td_buck = bucket.objects.filter(bucket_name=bucket_number).values('quantity')
#             td_buck = list(td_buck)[0]['quantity']
#             print('/n/n/n/n/n td_buck', td_buck)
#             print('\n\n\n', type(td_buck))
#     elif 'submit_form' in request.POST:
#         form = cooking_form(request.POST, prefix='s_form')
#         if form.is_valid():
#             form.save(commit=True)
#             qty = form.cleaned_data['Quantity']
#             new_qty = qty - td_buck
#
#             print('\n\n\n\n new_qty',new_qty)
#
#
#
#
#     context = {'quantity':td_buck,
#                'buck_info':form_2,
#                'process':form}
#     return render(request,'kaju/cooking.html',context = context)


 # bucket_number = form.cleaned_data['bucket']
 # print('/n/n/n/n/n bucket name', bucket_number)
 # td_buck = bucket.objects.filter(bucket_name=bucket_number).values('quantity')
 # td_buck = list(td_buck)[0]['quantity']
 # print('/n/n/n/n/n td_buck', td_buck)
 # print('\n\n\n', type(td_buck))
 # if request.method == "POST":
 #     form=cooking_form(request.POST)
 # if form.is_valid():


 # form.save(commit=True)
 # buck = bucket.objects.all()
 #



# class check_bin(forms.ModelForm):
#     class Meta:
#         model = processing_lot
#         # fields =('bucket', 'quantity')
#         fields =('bucket',)



# form.fields['processing_lot'].queryset = cutting_section.objects.exclude(processing_lot= 4)
    # form.fields.lot_name.queryset = cutting_section.objects.exclude(lot_name__processed=0)
    # # form.lot_name.queryset = cutting_section.objects.exclude(lot_name__processed=0)


<!--            {% if user.is_authenticated %}-->
<!--            <li><a class="navbar-link" href="{% url 'logout' %}">log_out</a></li>-->
<!--            {% else %}-->
<!--            <li><a class="navbar-link" href="{% url 'user_login' %}">Login</a></li>-->
<!--            {% endif %}-->