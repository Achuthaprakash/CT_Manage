from django import forms
from django.contrib.auth.models import User
from .models import *

class UserForm(forms.ModelForm):
    # password = forms.CharField(widget = forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','email','password')

class UserInfo(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('user',)
class country_form(forms.ModelForm):
    class Meta:
        model = country
        fields = ('country_origin','country_iso')


class region_form(forms.ModelForm):
    class Meta:
        model = region
        fields = ('country','region_name')

class bucket_form(forms.ModelForm):

    class Meta:
        model = bucket
        fields = ('region', 'quantity', 'crop_time', 'price_kg',
                  'purchase_out_turn', 'nut_count','production_out_turn',
                  'moisture', 'drying_req')

class rcn_dry_form(forms.ModelForm):
    class Meta:
        model = RCN_drying
        fields = ('bin_number','no_of_days','moisture_after_drying','quantity_after',
                  'production_out_turn','nut_count_after')




class day_param(forms.ModelForm):
    class Meta:
        model = climate_params
        fields = ('temperature_min', 'temperature_max','humidity','day_type')



class cooking_form(forms.ModelForm):
    class Meta:
        model = processing_lot
        fields =('bucket', 'quantity', 'date_of_position', 'cook_time', 'cook_pressure','foreign_particles','bag_weight')


class cut_form(forms.ModelForm):
    # dropdown = forms.ModelChoiceField(queryset=cutting_section.objects.all())
    class Meta:
        model = cutting_section
        fields = ('date', 'processing_lot', 'rcn_moisture','wholes', 'pieces', 'rejections', 'shells_output', 'pending_quantity',
                  'foreign_particles', 'kernel_moisture')

    # def __init__(self, *args, **kwargs):
    #     super(cut_form, self).__init__(*args,**kwargs)
    #     self.fields['processing_lot'].queryset = cutting_section.objects.exclude(processing_lot__lot_name='Lot1')


class bormah_form(forms.ModelForm):
    class Meta:
        model = bormah
        fields = ('bormah_date','bormah_lot','dried_wholes','dried_pieces')

class peeling_form(forms.ModelForm):
    class Meta:
        model = peeling
        fields = ('peeling_date', 'peeling_lot', 'peeled_wholes', 'peeled_pieces', 'unpeeled_wholes', 'unpeeled_pieces', 'rejections', 'husk')



class grade_name_form(forms.ModelForm):
    class Meta:
        model = grade_names
        fields = ('grade_type','grade_names')

class grading_form(forms.ModelForm):
    class Meta:
        model = grading_section
        fields = ('grading_date','grading_lot')