from django.contrib import admin
from .models import *

admin.site.register((MainCat,
                     SubCat,
                     Brand,
                     Seller,
                     Product,
                     Buyer,
                     Wishlist,
                     Checkout,
                     ContactUs,
                     Subscribe))

