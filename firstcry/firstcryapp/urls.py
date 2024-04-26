from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('user_login/', CustomLoginView.as_view(), name='user_login'),
    path('',views.first,name='first'),
    path('req_otp',views.request_otp,name='req_otp' ),
    path('resend_otp',views.resend_otp,name='resend_otp'),
    path('verify_otp',views.verify_otp,name='verify_otp'),
    path('forgotpwd',views.forgotpwd,name='forgotpwd'),
    path('pwd_verify_otp',views.pwd_verify_otp,name='pwd_verify_otp'),
    
    path('register',views.register,name='register'),
    path('registration',views.registration,name='reg'),
    path('reg',views.reg,name='reg'),
    path('insert_img',views.insert_img,name='insert_img'),
    path('submit/<pk>',views.submit,name='submit'),
    path('user_login',views.user_login,name='user_login'),
    path('userhome',views.userhome,name='userhome'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('detailedpage/<pk>',views.detailedpage,name='detailedpage'),
    path('logout/',views.user_logout,name='logout'),

    # admin urls--------------------------------------------------

    path('get_monthly_order_data/',views.get_monthly_order_data,name='get_monthly_order_data'),
    path('alluser',views.alluser,name='alluser'),
    path('edituser/<pk>',views.edituser,name='edituser'),
    path('updateuser,/<pk>',views.update_user,name='updateuser'),
    path('block_user/<pk>',views.block_user,name='block_user'),
    path('unblock_user/<pk>',views.unblock_user,name='unblock_user'),
    path('category',views.category,name='category'),
    path('add_category',views.add_category,name='add_category'),
    path('view_category',views.view_category,name='view_category'),
    path('edit_category/<pk>',views.edit_category,name='edit_category'),
    path('update_category/<pk>',views.update_category,name='update_category'),
    path('delete_category/<pk>',views.delete_category,name='delete_category'),

    path('addproduct/',views.add_product,name='addproduct'),
    path('add_vew_product',views.showproduct,name='add_vew_product'),
    path('adminproduct',views.product,name='adminproduct'),
    path('show_return',views.show_return,name='show_return'),
    path('show_returnProduct/<pk>',views.show_returnProduct,name='show_returnProduct'),
    path('addtostock/<pk>',views.addtostock,name='addtostock'),
    path('view_order/',views.view_order,name='view_order'),
    path('orderDetails/<pk>',views.orderDetails,name='orderDetails'),
    path('order_processed/<pk>',views.order_processed,name='order_processed'),
    path('order_shipping/<pk>',views.order_shipping,name='order_shipping'),
    path('order_deliver/<pk>',views.order_deliver,name='order_deliver'),
    path('admin_orderCancelPage/<pk>',views.admin_orderCancelPage,name='admin_orderCancelPage'),
    path('editproduct/<pk>',views.editproduct,name='editproduct'),
    path('productupdattion/<pk>',views.productupdation,name='productupdattion'),
    path('deleteproduct/<pk>',views.deleteproduct,name='deleteproduct'),
    path('change_for_types',views.change_for_types,name='change_for_types'),
    path('add_color_js',views.add_color_js,name='add_color_js'),
    path('view_varient/<pk>',views.view_product_varient,name='view_varient'),
    path('edit_varient/<pk>',views.edit_varient,name='edit_varient'),
    path('update_vairent/<pk>',views.update_varient,name='update_varient'),
    path('back_product',views.back_product,name='back_product'),
    path('add_brand_page/',views.add_brand_page,name='add_brand_page'),
    path('add_brand',views.add_brand,name='add_brand'),
    path('view_brand',views.view_brand,name='view_brand'),
    path('edit_brand_page/<pk>',views.edit_brand_page,name='edit_brand_page'),
    path('add_brand_js',views.add_brand_js,name='add_brand_js'),
    path('update_brand/<pk>/',views.update_brand,name='update_brand'),
    path('generate_pdf/',views.generate_pdf,name='generate_pdf'),
    path('downloading_page',views.downloading_page,name='downloading_page'),
    path('generate_excel',views.generate_excel,name='generate_excel'),
    path('listSales',views.listSales,name='listSales'),
    path('show_coupon',views.show_coupon,name='show_coupon'),
    path('add_coupon_page',views.add_coupon_page,name='add_coupon_page'),
    path('add_coupon',views.add_coupon,name='add_coupon'),
    path('show_edit_couponpage/<pk>',views.show_edit_couponpage,name='show_edit_couponpage'),
    path('update_coupon/<pk>',views.update_coupon,name='update_coupon'),
    path('delete_coupon/<pk>',views.delete_coupon,name='delete_coupon'),
    path('admin_cancelOrder',views.admin_cancelOrder,name='admin_cancelOrder'),

    # User URL-------------------------------




    path('detailed/<pk>',views.detailpage,name='detailed'),
    path('selectoneproduct/<pk>',views.selectoneproduct,name='selectoneproduct'),
    path('select_one/<pk>',views.oneproduct,name='select_one'),
    path('add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist',views.wishlistpage,name='wishlist'),
    path('remove_from_wishlist',views.remove_from_wishlist,name='remove_from_wishlist'),
    path('add_to_cart',views.add_to_cart,name='add_to_cart'),
    path('cart',views.showcart,name='cart'),
    path('update-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove-item/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('order',views.order_product,name='order'),
    path('order_product_from_orderhistory',views.order_product_from_orderhistory,name='order_product_from_orderhistory'),
   
    path('useraccount',views.useraccount,name='useraccount'),
    path('orderhistory',views.orderhistory,name='orderhistory'),
    
    path('personal',views.personal_data,name='personal'),
    path('update_user',views.updateuser,name='update_user'),
    path('show_address',views.show_address,name='show_address'),
    path('add_address',views.add_address,name='add_address'),
    path('update_address/<pk>',views.update_address,name='update_address'),
    path('delete_address/<pk>',views.delete_address,name='delete_address'),
    path('show_changepassword',views.show_changepassword,name='show_changepassword'),
    path('changepassword/',views.change_password,name='changepassword'),
    path('make_default/<pk>',views.make_default,name='make_default'),
    path('confirm_order',views.confirmorder,name='confirm_order'),
    path('coupon_check',views.coupon_check,name='coupon_check'),
    
    path('show_returnpage',views.show_returnpage,name='show_returnpage'),
    path('editreturnpage',views.editreturnpage,name='editreturnpage'),
   
    path('filter-data',views.filter_data,name='filter-data'),
    
    path('oneprod_filter',views.oneprod_filter,name='oneprod_filter'),
    path('paytoproceed',views.paytoproceed,name='paytoproceed'),
    path('menulinkSize',views.menulinkSize,name='menulinkSize'),
    
    path('orderItems/<pk>',views.orderItems,name='orderItems'),
    path('userreturnPage/<pk>',views.userreturnPage,name='userreturnPage'),
    path('returnOrder/<pk>',views.returnOrder,name='returnOrder'),
    path('showCancelledOrders',views.showCancelledOrders,name='showCancelledOrders'),
    path('showReturnedOrders',views.showReturnedOrders,name='showReturnedOrders'),
    path('show_wallet',views.show_wallet,name='show_wallet'),
    path('wallet_transaction',views.wallet_transaction,name='wallet_transaction'),
    path('invoice_pdf/<pk>',views.invoice_pdf,name='invoice_pdf'),


    # for test
    path('test',views.test,name='test'),
    path('crop-image/', views.upload_and_crop, name='upload_and_crop'),
    path('testttting',views.testttting,name='testttting'),
    

  
]