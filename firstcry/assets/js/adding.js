$(document).ready(function() {
    $('.add-to-wishlist').on('click', function() {
        event.preventDefault();
        var productId = $(this).closest('.product').data('product-id');
        let this_val = $(this)
        console.log(this_val)
        var csrftoken = getCookie('csrftoken');
        console.log("this",productId);
        $.ajax({
          type: 'POST',
          url: '/add_to_wishlist/',
          data: {'product_id': productId},
          dataType: 'json',
          headers: {'X-CSRFToken': csrftoken},
          success: function(response) {
            this_val.html("WISHLISTED")
            
              if (response.bool == true) {
                this_val.html("WISHLISTED")
                console.log("after",this_val);
                console.log("hiiiiii")
                console.log("Success! Data:");
                
           
                alert('Product added to wishlist!');
              } else {
                  alert('Product already in wishlist.');
              }
          }
      });
      
    });

                    // Function to get CSRF token from cookies
                    function getCookie(name) {
                      var cookieValue = null;
                      if (document.cookie && document.cookie !== '') {
                          var cookies = document.cookie.split(';');
                          for (var i = 0; i < cookies.length; i++) {
                              var cookie = cookies[i].trim();
                              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                  break;
                              }
                          }
                      }
                      return cookieValue;
                    }





});



$(document).ready(function() {
$('.remove-from-wishlist').on('click', function() {
    event.preventDefault();
    var productId = $(this).closest('.product').data('product-id');
    let this_val = $(this)
    console.log(productId)
    var csrftoken = getCookie('csrftoken');
    console.log("this",productId);
    $.ajax({
      type: 'POST',
      url: '/remove_from_wishlist',
      data: {'product_id': productId},
      dataType: 'json',
      headers: {'X-CSRFToken': csrftoken},
      success: function(response) {

        
          if (response.bool == true) {
            console.log("after",this_val);
            console.log("hiiiiii")
            console.log("Success! Data:");
            
       
           
            $(" .remove").load(location.href + " .remove")
            $(" #divid ").load(" # divid");
          } else {
              alert('Product already in wishlist.');
          }
      }
  });
  
});




  // Function to get CSRF token from cookies
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

});
  



$(document).ready(function() {
    $('.add-to-cart').on('click', function() {
        event.preventDefault();
        var productId = $(this).closest('.product').data('product-id');
        let this_val = $(this)
        console.log(productId)
        var csrftoken = getCookie('csrftoken');
        console.log("this",productId);
        $.ajax({
          type: 'POST',
          url: '/add_to_cart',
          data: {'product_id': productId},
          dataType: 'json',
          headers: {'X-CSRFToken': csrftoken},
          success: function(response) {
    
            this_val.html("ADDED TO CART")
              if (response.bool == true) {
                alert('Product added to cart!');
            
              } else {
                  alert('Product already in Cart.');
              }
          }
      });
      
    });
    
    
    
    
      // Function to get CSRF token from cookies
      function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
      }
    
    });
      
      