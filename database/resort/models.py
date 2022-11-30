# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Bedinfo(models.Model):
    bed_typeid = models.OneToOneField('Roomtype', models.DO_NOTHING, db_column='BED_TYPEID', primary_key=True)  # Field name made lowercase.
    size = models.FloatField(db_column='SIZE')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='QUANTITY')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BEDINFO'
        unique_together = (('bed_typeid', 'size'),)


class Bill(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    billid = models.CharField(db_column='BILLID', max_length=16, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    bill_checkin = models.TimeField(db_column='BILL_CHECKIN')  # Field name made lowercase.
    bill_checkout = models.TimeField(db_column='BILL_CHECKOUT')  # Field name made lowercase.
    bill_bookingid = models.ForeignKey('Receipt', models.DO_NOTHING, db_column='BILL_BOOKINGID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BILL'


class BillService(models.Model):
    bill_customerid = models.OneToOneField('Customer', models.DO_NOTHING, db_column='BILL_CUSTOMERID', primary_key=True)  # Field name made lowercase.
    bill_package_name = models.ForeignKey('Package', models.DO_NOTHING, db_column='BILL_PACKAGE_NAME')  # Field name made lowercase.
    date_buy = models.DateTimeField(db_column='DATE_BUY')  # Field name made lowercase.
    used_date = models.IntegerField(db_column='USED_DATE', blank=True, null=True)  # Field name made lowercase.
    start_day = models.DateTimeField(db_column='START_DAY')  # Field name made lowercase.
    total_cost_kvnd_field = models.IntegerField(db_column='TOTAL_COST (kVND)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'BILL_SERVICE'
        unique_together = (('bill_customerid', 'bill_package_name', 'start_day'),)


class Branch(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    branchid = models.CharField(db_column='BRANCHID', unique=True, max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    province = models.CharField(db_column='PROVINCE', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    addr = models.CharField(db_column='ADDR', unique=True, max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    phone = models.CharField(db_column='PHONE', unique=True, max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    mail = models.CharField(db_column='MAIL', unique=True, max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BRANCH'


class BranchHaveRoomtype(models.Model):
    bhr_branchid = models.OneToOneField(Branch, models.DO_NOTHING, db_column='BHR_BRANCHID', primary_key=True)  # Field name made lowercase.
    bhr_typeid = models.ForeignKey('Roomtype', models.DO_NOTHING, db_column='BHR_TYPEID')  # Field name made lowercase.
    price_kvnd_field = models.IntegerField(db_column='PRICE (kVND)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'BRANCH_HAVE_ROOMTYPE'
        unique_together = (('bhr_branchid', 'bhr_typeid'),)


class BranchImg(models.Model):
    img_branchid = models.OneToOneField(Branch, models.DO_NOTHING, db_column='IMG_BRANCHID', primary_key=True)  # Field name made lowercase.
    img = models.CharField(db_column='IMG', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BRANCH_IMG'
        unique_together = (('img_branchid', 'img'),)


class Company(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    companyid = models.CharField(db_column='COMPANYID', unique=True, max_length=6, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    company_name = models.CharField(db_column='COMPANY_NAME', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'COMPANY'


class Customer(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    customerid = models.CharField(db_column='CUSTOMERID', unique=True, max_length=8, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cccd = models.CharField(db_column='CCCD', unique=True, max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    fullname = models.CharField(db_column='FULLNAME', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PHONENUMBER', unique=True, max_length=12, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', unique=True, max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', unique=True, max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    points = models.IntegerField(db_column='POINTS')  # Field name made lowercase.
    ctype = models.IntegerField(db_column='CTYPE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CUSTOMER'


class Estate(models.Model):
    estate_branchid = models.OneToOneField(Branch, models.DO_NOTHING, db_column='ESTATE_BRANCHID', primary_key=True)  # Field name made lowercase.
    estateid = models.IntegerField(db_column='ESTATEID')  # Field name made lowercase.
    height = models.FloatField(db_column='HEIGHT')  # Field name made lowercase.
    width = models.FloatField(db_column='WIDTH')  # Field name made lowercase.
    cost = models.IntegerField(db_column='COST')  # Field name made lowercase.
    info = models.CharField(db_column='INFO', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    estate_serviceid = models.ForeignKey('Services', models.DO_NOTHING, db_column='ESTATE_SERVICEID')  # Field name made lowercase.
    link = models.CharField(db_column='LINK', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    storename = models.CharField(db_column='STORENAME', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ESTATE'
        unique_together = (('estate_branchid', 'estateid'),)


class HiringRoom(models.Model):
    hr_bookingid = models.ForeignKey('Receipt', models.DO_NOTHING, db_column='HR_BOOKINGID')  # Field name made lowercase.
    hr_branchid = models.OneToOneField('Room', models.DO_NOTHING, db_column='HR_BRANCHID', primary_key=True, related_name='hr_branchid')  # Field name made lowercase.
    hr_roomid = models.ForeignKey('Room', models.DO_NOTHING, db_column='HR_ROOMID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HIRING_ROOM'
        unique_together = (('hr_branchid', 'hr_bookingid', 'hr_roomid'),)


class Package(models.Model):
    package_name = models.CharField(db_column='PACKAGE_NAME', primary_key=True, max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    num_days = models.IntegerField(db_column='NUM_DAYS')  # Field name made lowercase.
    package_capacity = models.IntegerField(db_column='PACKAGE_CAPACITY')  # Field name made lowercase.
    package_cost = models.IntegerField(db_column='PACKAGE_COST')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PACKAGE'


class ProvideSupply(models.Model):
    provide_supplier = models.ForeignKey('Supplier', models.DO_NOTHING, db_column='PROVIDE_SUPPLIER_ID')  # Field name made lowercase.
    provide_supply_branchid = models.ForeignKey(Branch, models.DO_NOTHING, db_column='PROVIDE_SUPPLY_BRANCHID')  # Field name made lowercase.
    provide_supplyid = models.OneToOneField('SupplyType', models.DO_NOTHING, db_column='PROVIDE_SUPPLYID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PROVIDE_SUPPLY'
        unique_together = (('provide_supplyid', 'provide_supply_branchid'),)


class Receipt(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    receipt_bookingid = models.CharField(db_column='RECEIPT_BOOKINGID', max_length=16, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    booking_time = models.DateTimeField(db_column='BOOKING_TIME')  # Field name made lowercase.
    checkin = models.DateTimeField(db_column='CHECKIN')  # Field name made lowercase.
    checkout = models.DateTimeField(db_column='CHECKOUT')  # Field name made lowercase.
    stat = models.IntegerField(db_column='STAT')  # Field name made lowercase.
    receipt_capacity = models.IntegerField(db_column='RECEIPT_CAPACITY')  # Field name made lowercase.
    receipt_total_cost = models.IntegerField(db_column='RECEIPT_TOTAL_COST')  # Field name made lowercase.
    receipt_customerid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='RECEIPT_CUSTOMERID')  # Field name made lowercase.
    receipt_package_name = models.ForeignKey(Package, models.DO_NOTHING, db_column='RECEIPT_PACKAGE_NAME')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RECEIPT'


class Room(models.Model):
    room_branchid = models.OneToOneField('Zones', models.DO_NOTHING, db_column='ROOM_BRANCHID', primary_key=True, related_name='room_branchid')  # Field name made lowercase.
    roomid = models.CharField(db_column='ROOMID', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    room_typeid = models.ForeignKey('Roomtype', models.DO_NOTHING, db_column='ROOM_TYPEID')  # Field name made lowercase.
    room_zname = models.ForeignKey('Zones', models.DO_NOTHING, db_column='ROOM_ZNAME')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ROOM'
        unique_together = (('room_branchid', 'room_branchid', 'roomid'),)


class Roomtype(models.Model):
    typeid = models.AutoField(db_column='TYPEID', primary_key=True)  # Field name made lowercase.
    typename = models.CharField(db_column='TYPENAME', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    area = models.FloatField(db_column='AREA')  # Field name made lowercase.
    capacity = models.IntegerField(db_column='CAPACITY')  # Field name made lowercase.
    descriptions = models.CharField(db_column='DESCRIPTIONS', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ROOMTYPE'


class Services(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    service_type = models.CharField(db_column='SERVICE_TYPE', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    serviceid = models.CharField(db_column='SERVICEID', unique=True, max_length=8, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    service_capacity = models.IntegerField(db_column='SERVICE_CAPACITY')  # Field name made lowercase.
    style = models.CharField(db_column='STYLE', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    companyid = models.ForeignKey(Company, models.DO_NOTHING, db_column='COMPANYID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SERVICES'


class Souvenir(models.Model):
    serviceid = models.CharField(db_column='SERVICEID', max_length=8, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    souvenir_name = models.CharField(db_column='SOUVENIR_NAME', unique=True, max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SOUVENIR'


class SouvenirBrand(models.Model):
    sbrand_serviceid = models.OneToOneField(Services, models.DO_NOTHING, db_column='SBRAND_SERVICEID', primary_key=True)  # Field name made lowercase.
    brand = models.CharField(db_column='BRAND', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SOUVENIR_BRAND'
        unique_together = (('sbrand_serviceid', 'brand'),)


class Spa(models.Model):
    spa_serviceid = models.OneToOneField(Services, models.DO_NOTHING, db_column='SPA_SERVICEID', primary_key=True)  # Field name made lowercase.
    spa_name = models.CharField(db_column='SPA_NAME', unique=True, max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SPA'
        unique_together = (('spa_serviceid', 'spa_name'),)


class StorePic(models.Model):
    spic_branchid = models.OneToOneField(Estate, models.DO_NOTHING, db_column='SPIC_BRANCHID', primary_key=True, related_name='spic_branchid')  # Field name made lowercase.
    spic = models.ForeignKey(Estate, models.DO_NOTHING, db_column='SPIC_ID')  # Field name made lowercase.
    spic_link = models.CharField(db_column='SPIC_LINK', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'STORE_PIC'
        unique_together = (('spic_branchid', 'spic', 'spic_link'),)


class Supplier(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    supplier_id = models.CharField(db_column='SUPPLIER_ID', unique=True, max_length=7, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    supplier_name = models.CharField(db_column='SUPPLIER_NAME', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    supplier_email = models.CharField(db_column='SUPPLIER_EMAIL', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    supplier_addres = models.CharField(db_column='SUPPLIER_ADDRES', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SUPPLIER'


class Supply(models.Model):
    supply_branchid = models.OneToOneField(Room, models.DO_NOTHING, db_column='SUPPLY_BRANCHID', related_name='supply_branchid')  # Field name made lowercase.
    supplyid = models.ForeignKey('SupplyType', models.DO_NOTHING, db_column='SUPPLYID')  # Field name made lowercase.
    stt_id = models.AutoField(db_column='STT_ID', primary_key=True)  # Field name made lowercase.
    supply_roomid = models.ForeignKey(Room, models.DO_NOTHING, db_column='SUPPLY_ROOMID')  # Field name made lowercase.
    statuss = models.CharField(db_column='STATUSS', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SUPPLY'
        unique_together = (('supply_branchid', 'supply_branchid', 'supplyid', 'stt_id'),)


class SupplyInRoom(models.Model):
    sir_supplyid = models.OneToOneField('SupplyType', models.DO_NOTHING, db_column='SIR_SUPPLYID', primary_key=True)  # Field name made lowercase.
    sir_typeid = models.ForeignKey(Roomtype, models.DO_NOTHING, db_column='SIR_TYPEID')  # Field name made lowercase.
    num_supply = models.IntegerField(db_column='NUM_SUPPLY')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SUPPLY_IN_ROOM'
        unique_together = (('sir_supplyid', 'sir_typeid'),)


class SupplyType(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    supplyid = models.CharField(db_column='SUPPLYID', unique=True, max_length=6, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sname = models.CharField(db_column='SNAME', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SUPPLY_TYPE'


class TimeActivity(models.Model):
    at_branchid = models.OneToOneField(Estate, models.DO_NOTHING, db_column='AT_BRANCHID', primary_key=True, related_name='at_branchid')  # Field name made lowercase.
    at = models.ForeignKey(Estate, models.DO_NOTHING, db_column='AT_ID')  # Field name made lowercase.
    at_start_time = models.TimeField(db_column='AT_START_TIME')  # Field name made lowercase.
    at_end_time = models.TimeField(db_column='AT_END_TIME')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TIME_ACTIVITY'
        unique_together = (('at_branchid', 'at', 'at_start_time'),)


class Zones(models.Model):
    zone_branchid = models.OneToOneField(Branch, models.DO_NOTHING, db_column='ZONE_BRANCHID', primary_key=True)  # Field name made lowercase.
    zname = models.CharField(db_column='ZNAME', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ZONES'
        unique_together = (('zone_branchid', 'zname'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    object_repr = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')
    action_flag = models.SmallIntegerField()
    change_message = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('UsrCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    model = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS')
    session_data = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class UsrCustomuser(models.Model):
    password = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
    last_login = models.DateTimeField(blank=True, null=True)
    fullname = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    email = models.CharField(max_length=254, db_collation='SQL_Latin1_General_CP1_CI_AS')
    username = models.CharField(primary_key=True, max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    date_joined = models.DateTimeField()
    is_active = models.BooleanField()
    is_staff = models.BooleanField()
    is_superuser = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'usr_customuser'


class UsrCustomuserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(UsrCustomuser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'usr_customuser_groups'
        unique_together = (('customuser', 'group'),)


class UsrCustomuserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(UsrCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'usr_customuser_user_permissions'
        unique_together = (('customuser', 'permission'),)
