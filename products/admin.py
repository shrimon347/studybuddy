from django.contrib import admin

from .models import Price, Product, ProductTag,PaymentHistory

class PriceAdmin(admin.StackedInline):
    model = Price

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (PriceAdmin,)
    list_display = ('name','desc','thumbnail','url','created_at','updated_at')
    class Meta:
        model = Product
class PaymenthistoryAdmin(admin.ModelAdmin):
    list_display = ('email','product','payment_status','created_at','updated_at')
admin.site.register(ProductTag)
admin.site.register(Price)
admin.site.register(PaymentHistory,PaymenthistoryAdmin)