from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models
from django.db.models import Manager as GeoManager

# Create your models here.


class Facility(models.Model):

    id = models.AutoField(primary_key=True)
    facilities_eq_id = models.CharField(max_length=255, help_text=_(
        "facilities_eq_id"), verbose_name=_("facilities_eq_id"), null=True)
    facilities_name = models.CharField(max_length=255, help_text=_(
        "facilities_name"), verbose_name=_("facilities_name"), null=True)
    facilities_country = models.CharField(max_length=500, help_text=_(
        "facilities_country"), verbose_name=_("facilities_country"), null=True)
    facilities_address = models.CharField(max_length=500, help_text=_(
        "facilities_address"), verbose_name=_("facilities_address"), null=True)
    facilities_type = models.CharField(max_length=255, help_text=_(
        "facilities_type"), verbose_name=_("facilities_type"), null=True)
    facilities_lat = models.DecimalField(
        max_digits=9, decimal_places=6,
        help_text="facilities_lat", verbose_name="facilities_lat",
        null=True
    )
    facilities_long = models.DecimalField(
        max_digits=9, decimal_places=6,
        help_text="facilities_long", verbose_name="facilities_long",
        null=True
    )
    facilites_rspo = models.CharField(max_length=255, help_text=_(
        "facilites_rspo"), verbose_name=_("facilites_rspo"), null=True)
    facilites_date_update = models.CharField(max_length=255, help_text=_(
        "facilites_date_update"), verbose_name=_("facilites_date_update"), null=True)
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))
    geom = models.PointField(srid=4326, dim=2, null=True)
    is_display = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    objects = GeoManager()

    class Meta:
        verbose_name = _("Facility")
        verbose_name_plural = _("Facilities")

    def __str__(self):
        return str(self.facilities_address)


class Refinery(models.Model):

    id = models.AutoField(primary_key=True)
    refinery_eq_id = models.CharField(max_length=255, help_text=_(
        "refinery_eq_id"), verbose_name=_("refinery_eq_id"), null=True)
    refinery_name = models.CharField(max_length=255, help_text=_(
        "refinery_name"), verbose_name=_("refinery_name"), null=True)
    refinery_address = models.CharField(max_length=500, help_text=_(
        "refinery_address"), verbose_name=_("refinery_address"), null=True)
    refinery_country = models.CharField(max_length=500, help_text=_(
        "refinery_country"), verbose_name=_("refinery_country"), null=True)
    refinery_type = models.CharField(max_length=255, help_text=_(
        "refinery_type"), verbose_name=_("refinery_type"), null=True)
    refinery_lat = models.DecimalField(
        max_digits=9, decimal_places=6,
        help_text="refinery_lat", verbose_name="refinery_lat",
        null=True
    )
    refinery_long = models.DecimalField(
        max_digits=9, decimal_places=6,
        help_text="refinery_long", verbose_name="refinery_long",
        null=True
    )
    refinery_rspo = models.CharField(max_length=255, help_text=_(
        "refinery_rspo"), verbose_name=_("refinery_rspo"), null=True)
    refinery_date_update = models.CharField(max_length=255, help_text=_(
        "refinery_date_update"), verbose_name=_("refinery_date_update"), null=True)
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))
    geom = models.PointField(srid=4326, dim=2, null=True)
    is_display = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    objects = GeoManager()

    class Meta:
        verbose_name = _("Refinery")
        verbose_name_plural = _("Refineries")

    def __str__(self):
        return str(self.refinery_address)


class Mill(models.Model):
    id = models.AutoField(primary_key=True)
    mill_eq_id = models.CharField(max_length=255, help_text=_(
        "mill_eq_id"), verbose_name=_("mill_eq_id"), null=True)
    mill_name = models.CharField(max_length=255, help_text=_(
        "mill_name"), verbose_name=_("mill_name"), null=True)
    mill_uml_id = models.CharField(max_length=255, help_text=_(
        "mill_uml_id"), verbose_name=_("mill_uml_id"), null=True)
    mill_company_name = models.CharField(max_length=255, help_text=_(
        "mill_company_name"), verbose_name=_("mill_company_name"), null=True)
    mill_company_group_id = models.CharField(max_length=255, help_text=_(
        "mill_company_group_id"), verbose_name=_("mill_company_group_id"), null=True)
    mill_company_group = models.CharField(max_length=255, help_text=_(
        "mill_company_group"), verbose_name=_("mill_company_group"), null=True)
    mill_country = models.CharField(max_length=255, help_text=_(
        "mill_country"), verbose_name=_("mill_country"), null=True)
    mill_province = models.CharField(max_length=255, help_text=_(
        "mill_province"), verbose_name=_("mill_province"), null=True)
    mill_district = models.CharField(max_length=255, help_text=_(
        "mill_district"), verbose_name=_("mill_district"), null=True)
    mill_address = models.CharField(max_length=500, help_text=_(
        "mill_address"), verbose_name=_("mill_address"), null=True)
    mill_type = models.CharField(max_length=255, help_text=_(
        "mill_type"), verbose_name=_("mill_type"), null=True)
    mill_lat = models.DecimalField(
        max_digits=9, decimal_places=6,
        help_text="mill_lat", verbose_name="mill_lat",
        null=True
    )
    mill_long = models.DecimalField(
        max_digits=9, decimal_places=6,
        help_text="mill_long", verbose_name="mill_long",
        null=True
    )
    mill_rspo = models.CharField(max_length=255, help_text=_(
        "mill_rspo"), verbose_name=_("mill_rspo"), null=True)
    mill_mspo = models.CharField(max_length=255, help_text=_(
        "mill_mspo"), verbose_name=_("mill_mspo"), null=True)
    mill_capacity = models.CharField(max_length=255, help_text=_(
        "mill_capacity"), verbose_name=_("mill_capacity"), null=True)
    mill_methane_capture = models.CharField(max_length=255, help_text=_(
        "mill_methane_capture"), verbose_name=_("mill_methane_capture"), null=True)
    mill_deforestation_risk = models.CharField(max_length=255, help_text=_(
        "mill_deforestation_risk"), verbose_name=_("mill_deforestation_risk"), null=True)
    mill_legal_prf_risk = models.CharField(max_length=255, help_text=_(
        "mill_legal_prf_risk"), verbose_name=_("mill_legal_prf_risk"), null=True)
    mill_legal_production_forest = models.CharField(max_length=255, help_text=_(
        "mill_legal_production_forest"), verbose_name=_("mill_legal_production_forest"), null=True)
    mill_legal_conservation_area = models.CharField(max_length=255, help_text=_(
        "mill_legal_conservation_area"), verbose_name=_("mill_legal_conservation_area"), null=True)
    mill_legal_landuse_risk = models.CharField(max_length=255, help_text=_(
        "mill_legal_landuse_risk"), verbose_name=_("mill_legal_landuse_risk"), null=True)
    mill_complex_supplybase_risk = models.CharField(max_length=255, help_text=_(
        "mill_complex_supplybase_risk"), verbose_name=_("mill_complex_supplybase_risk"), null=True)
    mill_date_update = models.CharField(max_length=255, help_text=_(
        "mill_date_update"), verbose_name=_("mill_date_update"), null=True)
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))
    geom = models.PointField(srid=4326, dim=2, null=True)
    is_planted = models.BooleanField(default=False)
    is_display = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    objects = GeoManager()

    class Meta:
        verbose_name = _("Mill")
        verbose_name_plural = _("Mills")

    def __str__(self):
        return str(self.mill_address)


class Agriplot(models.Model):
    id = models.AutoField(primary_key=True)
    id_mill = models.CharField(max_length=255, help_text=_(
        "id_mill"), verbose_name=_("id_mill"), null=True)
    mill_name = models.CharField(max_length=255, help_text=_(
        "mill_name"), verbose_name=_("mill_name"), null=True)
    millideq = models.CharField(max_length=255, help_text=_(
        "millideq"), verbose_name=_("millideq"), null=True)
    ownership_plot = models.CharField(max_length=255, help_text=_(
        "ownership"), verbose_name=_("ownership"), null=True)
    subsidiary = models.CharField(max_length=255, help_text=_(
        "subsidiary"), verbose_name=_("subsidiary"), null=True)
    estate = models.CharField(max_length=255, help_text=_(
        "estate"), verbose_name=_("estate"), null=True)
    # ID_Estate = models.CharField(max_length=255, help_text=_(
    #     "ID_Estate"), verbose_name=_("ID_Estate"), null=True)
    id_estate = models.CharField(max_length=255, help_text=_(
        "id_estate"), verbose_name=_("id_estate"), null=True)
    agriplot_id = models.CharField(max_length=255, help_text=_(
        "agriplot_id"), verbose_name=_("agriplot_id"), null=True)
    type_of_supplier = models.CharField(max_length=255, help_text=_(
        "type_of_supplier"), verbose_name=_("type_of_supplier"), null=True)
    village = models.CharField(max_length=255, help_text=_(
        "village"), verbose_name=_("village"), null=True)
    sub_district = models.CharField(max_length=255, help_text=_(
        "sub_district"), verbose_name=_("sub_district"), null=True)
    district = models.CharField(max_length=255, help_text=_(
        "district"), verbose_name=_("district"), null=True)
    province = models.CharField(max_length=255, help_text=_(
        "province"), verbose_name=_("province"), null=True)
    country = models.CharField(max_length=255, help_text=_(
        "country"), verbose_name=_("country"), null=True)
    planted_area = models.CharField(max_length=255, help_text=_(
        "planted_area"), verbose_name=_("planted_area"), null=True)
    year_update = models.CharField(max_length=255, help_text=_(
        "year_update"), verbose_name=_("year_update"), null=True)
    risk_assess = models.CharField(max_length=255, help_text=_(
        "risk_assess"), verbose_name=_("risk_assess"), null=True)
    ghg_luc = models.CharField(max_length=255, help_text=_(
        "ghg_luc"), verbose_name=_("ghg_luc"), null=True)
    def_free = models.CharField(max_length=255, help_text=_(
        "def_free"), verbose_name=_("def_free"), null=True)
    compliance = models.CharField(max_length=255, help_text=_(
        "compliance"), verbose_name=_("compliance"), null=True)
    status_of_plot = models.CharField(max_length=255, help_text=_(
        "status_of_plot"), verbose_name=_("status_of_plot"), null=True)
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))
    geom = models.PolygonField(srid=4326, blank=True, null=True, dim=3)
    actual_supplier = models.BooleanField(default=True)
    is_display = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    objects = GeoManager()

    class Meta:
        verbose_name = _("Agriplot")
        verbose_name_plural = _("Agriplots")

    def __str__(self):
        return str(self.id)


class Tracetomill(models.Model):
    id = models.AutoField(primary_key=True)
    facility_eq_id = models.CharField(max_length=255, help_text=_(
        "facility_eq_id"), verbose_name=_("facility_eq_id"), null=True)
    mill_eq_id = models.CharField(max_length=255, help_text=_(
        "mill_eq_id"), verbose_name=_("mill_eq_id"), null=True)
    mill_uml_id = models.CharField(max_length=255, help_text=_(
        "mill_uml_id"), verbose_name=_("mill_uml_id"), null=True)
    mill_name = models.CharField(max_length=255, help_text=_(
        "mill_name"), verbose_name=_("mill_name"), null=True)
    ttm_source_type = models.CharField(max_length=255, help_text=_(
        "ttm_source_type"), verbose_name=_("ttm_source_type"), null=True)
    ttm_year_period = models.CharField(max_length=255, help_text=_(
        "ttm_year_period"), verbose_name=_("ttm_year_period"), null=True)
    ttm_date_update = models.CharField(max_length=255, help_text=_(
        "ttm_date_update"), verbose_name=_("ttm_date_update"), null=True)
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))
    is_display = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Tracetomill")
        verbose_name_plural = _("Tracetomills")

    def __str__(self):
        return str(self.mill_name)


class Tracetoplantation(models.Model):
    id = models.AutoField(primary_key=True)
    mill_eq_id = models.CharField(max_length=255, help_text=_(
        "mill_eq_id"), verbose_name=_("mill_eq_id"), null=True)
    mill_uml_id = models.CharField(max_length=255, help_text=_(
        "mill_uml_id"), verbose_name=_("mill_uml_id"), null=True)
    mill_name = models.CharField(max_length=255, help_text=_(
        "mill_name"), verbose_name=_("mill_name"), null=True)
    agriplot_eq_id = models.CharField(max_length=255, help_text=_(
        "agriplot_eq_id"), verbose_name=_("agriplot_eq_id"), null=True)
    agriplot_type = models.CharField(max_length=255, help_text=_(
        "agriplot_type"), verbose_name=_("agriplot_type"), null=True)
    agriplot_estate_name_id = models.CharField(max_length=255, help_text=_(
        "agriplot_estate_name_id"), verbose_name=_("agriplot_estate_name_id"), null=True)
    agriplot_estate_name = models.CharField(max_length=255, help_text=_(
        "agriplot_estate_name"), verbose_name=_("agriplot_estate_name"), null=True)
    ttp_source_type = models.CharField(max_length=255, help_text=_(
        "ttp_source_type"), verbose_name=_("ttp_source_type"), null=True)
    ttp_year_period = models.CharField(max_length=255, help_text=_(
        "ttp_year_period"), verbose_name=_("ttp_year_period"), null=True)
    ttp_date_update = models.CharField(max_length=255, help_text=_(
        "ttp_date_update"), verbose_name=_("ttp_date_update"), null=True)
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))
    is_display = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Tracetoplantation")
        verbose_name_plural = _("Tracetoplantations")

    def __str__(self):
        return str(self.mill_name)


# class PlantedOutsideLandRegistration(models.Model):
#     id = models.AutoField(primary_key=True)
#     mukim = models.CharField(max_length=255, help_text=_(
#         "mukim"), verbose_name=_("mukim"), null=True)
#     id_mukim = models.CharField(max_length=255, help_text=_(
#         "id_mukim"), verbose_name=_("id_mukim"), null=True)
#     daerah = models.CharField(max_length=255, help_text=_(
#         "daerah"), verbose_name=_("daerah"), null=True)
#     id_daerah = models.CharField(max_length=255, help_text=_(
#         "id_daerah"), verbose_name=_("id_daerah"), null=True)
#     negeri = models.CharField(max_length=255, help_text=_(
#         "negeri"), verbose_name=_("negeri"), null=True)
#     id_negeri = models.CharField(max_length=255, help_text=_(
#         "id_negeri"), verbose_name=_("id_negeri"), null=True)
#     country = models.CharField(max_length=255, help_text=_(
#         "country"), verbose_name=_("country"), null=True)
#     note = models.CharField(max_length=255, help_text=_(
#         "note"), verbose_name=_("note"), null=True)
#     status_plot = models.CharField(max_length=255, help_text=_(
#         "status"), verbose_name=_("status"), null=True)
#     created_at = models.DateTimeField(default=timezone.now, help_text=_(
#         "Creation date"), verbose_name=_("Created at"))
#     geom = models.PolygonField(srid=4326, blank=True, null=True, dim=3)

#     is_display = models.BooleanField(default=True)
#     is_edited = models.BooleanField(default=False)
#     is_deleted = models.BooleanField(default=False)

#     class Meta:
#         verbose_name = _("PlantedOutsideLandRegistration")
#         verbose_name_plural = _("PlantedOutsideLandRegistrations")

#     def __str__(self):
#         return str(self.mukim)
