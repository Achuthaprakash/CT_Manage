from django.db import models
import datetime
from django.db.models.query import QuerySet
from django.contrib.auth.models import User


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    portfolio = models.URLField(blank=True)
    #picture = models.ImageField(upload_to='profile_pics')
    def __str__(self):
        return self.user.username

def transform_lot(x):
    my_str = x[:3]+ str(int(x[3:])+1)
    return my_str

def get_int_lot(x):
    return str(int(x[3:]))
# Create your models here.

class country(models.Model):
    country_id = models.IntegerField(primary_key=True)
    country_origin =models.CharField(max_length=255,null=False,unique=True)
    country_iso = models.CharField(max_length=2,null=False)
    # def __unicode__(self):
    #     return self.country_origin

    def __str__(self):
        return str(self.country_origin)
    class Meta:
        app_label ='kaju'
        ordering = (['country_origin'])



class region(models.Model):
    region_id = models.IntegerField(primary_key=True)
    region_name = models.CharField(max_length=255,null=False,unique=True)
    country = models.ForeignKey(country,on_delete=models.CASCADE)
    # def __unicode__(self):
    #     return self.country
    def __str__(self):
        return str(self.region_name)

class bucket(models.Model):
    bucket_id = models.IntegerField(primary_key=True)
    bucket_name = models.CharField(max_length=6,null=True)
    region = models.ForeignKey(region,on_delete=models.CASCADE)
    quantity = models.FloatField()
    crop_time = models.CharField(max_length=120,null=True)
    price_kg = models.FloatField()
    purchase_out_turn = models.FloatField(null=False)
    nut_count = models.IntegerField(null=False)
    number_bag = models.FloatField(null=True)
    production_out_turn = models.FloatField(null=False)
    moisture = models.FloatField(null=True)
    drying_req = models.BooleanField(null=False)
    date = models.DateField(null=True)
    def save(self,force_insert=True, force_update=True):
        number = bucket.objects.count()+1
        self.bucket_name= "B"+ str(self.region)[:2].upper()+str(number)
        self.number_bag = self.quantity/80
        self.date = datetime.date.today()
        super(bucket,self).save()
    def __str__(self):
        return str(self.bucket_name)
    class Meta:
        app_label ='kaju'
        ordering = (['-quantity'])



class RCN_drying(models.Model):
    bin_number = models.ForeignKey(bucket,on_delete=models.CASCADE)
    no_of_days = models.IntegerField()
    moisture_after_drying = models.FloatField()
    quantity_after = models.FloatField()
    weight_loss = models.FloatField()
    production_out_turn = models.FloatField()
    nut_count_after = models.IntegerField()

    def quantity_dry(self):
        return self.bin_number.quantity

    def save(self, force_insert=True, force_update=True):
        self.weight_loss = self.quantity_dry() - self.quantity_after
        super(RCN_drying,self).save()


class day_type(models.Model):
    day_id = models.IntegerField(primary_key=True)
    day_type = models.CharField(max_length=250)
    def __str__(self):
        return str(self.day_type)
    class Meta:
        app_label = 'kaju'
        ordering = (['day_type'])

class climate_params(models.Model):
    clim_id = models.IntegerField(primary_key=True)
    date_climate = models.DateField()
    temperature_min = models.FloatField()
    temperature_max = models.FloatField()
    humidity = models.FloatField(null=True)
    day_type = models.ForeignKey(day_type, on_delete=models.CASCADE)

    def save(self, force_insert= True, force_update= True):
        self.date_climate = datetime.date.today()
        super(climate_params,self).save()
    def __str__(self):
        return str(self.date_climate)
    class Meta:
        ordering = (['-date_climate'])

class processes (models.Model):
    pro_id = models.IntegerField(primary_key=True)
    process = models.CharField(max_length=250, null=False)


class processing_lot(models.Model):
    lot_id = models.IntegerField(primary_key=True)
    lot_name= models.CharField(max_length=6)
    quantity = models.FloatField()
    lot_quantity = models.FloatField(null=True)
    bucket = models.ForeignKey(bucket,on_delete=models.CASCADE)
    # process_position = models.ForeignKey(processes, on_delete= models.CASCADE)
    date_of_position = models.ForeignKey(climate_params,on_delete= models.CASCADE)
    cook_time = models.FloatField(null=True, default=0)
    cook_pressure = models.FloatField(null=True, default=0)
    foreign_particles = models.FloatField(null=True,default=0)
    bag_weight = models.FloatField(null=True, default=0)
    processed = models.FloatField(null=True, default=0)
    wholes = models.FloatField(null=True, default=0)
    pieces = models.FloatField(null=True, default=0)
    rejection = models.FloatField(null=True, default=0)
    shells = models.FloatField(null=True, default=0)
    out_turn = models.FloatField(null=True, default=0)
    process_total = models.FloatField(null=True, default=0)
    adj_cutting = models.FloatField(null=True, default=0)
    dried_wholes = models.FloatField(null=True, default=0)
    dried_pieces = models.FloatField(null=True, default=0)
    husk = models.FloatField(null=True, default=0)
    final_output = models.FloatField(null=True, default=0)
    grading_consolidation = models.CharField(max_length=1500,default='NF')



    def save(self, force_insert=True, force_update=True):
        self.lot_quantity = self.quantity

        #LOT NAME UPDATE
        # number = processing_lot.objects.count() + 1

        id_no = str(processing_lot.objects.latest('lot_id'))
        id_no = int(id_no[3:])+1
        self.lot_name = "LOT" + str(id_no)
        # self.lot_name = "LOT" + str(self.lot_id)
        super(processing_lot, self).save()
    def __str__(self):
        return str(self.lot_name)
    class Meta:
        ordering = (['-lot_id'])




class cutting_section(models.Model):
    date   = models.ForeignKey(climate_params,on_delete=models.CASCADE)
    processing_lot = models.ForeignKey(processing_lot,on_delete=models.CASCADE)
    rcn_moisture = models.FloatField()
    wholes = models.FloatField()
    pieces = models.FloatField()
    rejections = models.FloatField()
    shells_output = models.FloatField()
    pending_quantity = models.FloatField(null=True)
    foreign_particles = models.FloatField(null=True)
    kernel_moisture = models.FloatField(null=True)
    out_turn = models.FloatField(null=True)
    def __str__(self):
        return str(self.processing_lot)
    def save(self, force_insert=True, force_update=True):
        qty = self.processing_lot.quantity - self.pending_quantity
        op = self.wholes+self.pieces
        try:
            ot = (op*80*2.23)/(qty)
        except:
            ot = 0
        self.out_turn = ot
        super(cutting_section,self).save()

class bormah(models.Model):
    bormah_date = models.ForeignKey(climate_params,on_delete=models.CASCADE)
    bormah_lot = models.ForeignKey(processing_lot,on_delete=models.CASCADE)
    dried_wholes = models.FloatField(null=True)
    dried_pieces = models.FloatField(null=True)

    def __str__(self):
        return str(self.bormah_lot)

class peeling(models.Model):
    peeling_date = models.ForeignKey(climate_params,on_delete=models.CASCADE)
    peeling_lot = models.ForeignKey(processing_lot,on_delete=models.CASCADE)
    peeled_wholes = models.FloatField()
    peeled_pieces = models.FloatField()
    unpeeled_wholes = models.FloatField()
    unpeeled_pieces = models.FloatField()
    rejections = models.FloatField(null=True)
    husk = models.FloatField(null=True)

    def __str__(self):
        return str(self.peeling_lot)

class grade_names(models.Model):
    grad_id = models.IntegerField(primary_key=True)
    grade_type = models.CharField(max_length=10)
    grade_names = models.CharField(max_length=10)
    consolidated_qty = models.FloatField(null=True)

class grading_section(models.Model):
    grading_date = models.ForeignKey(climate_params,on_delete=models.CASCADE)
    grading_lot = models.ForeignKey(processing_lot,on_delete=models.CASCADE)
    grading_output = models.CharField(max_length=1500)






