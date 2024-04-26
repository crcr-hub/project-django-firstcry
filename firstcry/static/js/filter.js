$(document).ready(function(){
    $(".filter-checkbox").on('click',function(){
        var _filterObj={};
        $(".filter-checkbox").each(function(index,ele){
            var _filterval = $(this).val();
            var _filterkey = $(this).data('filter');
            console.log(_filterkey,_filterval);
            _filterObj[_filterkey]=Array.from(document.querySelectorAll('input[data-filter='+_filterkey+']:checked')).map(function(e1){
                return e1.value;
            });

        });
        console.log("thishs",_filterObj)
        // ajax starts
        $.ajax({
            type:'POST',
            url:'/filter-data',
            
            data : _filterObj,
            headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
            datatype:'json',
            beforeSend: function(){
               // $("#filterprodu").html('Loading......');
            },
            success: function(res){
                $("#filterproduct").html(res.data);
                var executeScript = function() {
                    const buttons = document.querySelectorAll('.color-button');
                    console.log(buttons);
                    buttons.forEach(button => {
                        const color = button.dataset.id;
                        console.log(color);
                        button.style.backgroundColor = color;
                    });
                };
                
                // Check if the DOM is already loaded
                if (document.readyState === 'loading') {
                    // If DOM is still loading, wait for it to be loaded
                    document.addEventListener('DOMContentLoaded', executeScript);
                } else {
                    // If DOM is already loaded, execute the script immediately
                    executeScript();
                }
            }
            
            

        });


    });



// filter from menu items based on size


    // $(".filter-checkbox").on('click',function(){
    //     var _filterObj={};
    //     $(".filter-checkbox").each(function(index,ele){
    //         var _filterval = $(this).val();
    //         var _filterkey = $(this).data('filter');
    //         console.log(_filterkey,_filterval);
    //         _filterObj[_filterkey]=Array.from(document.querySelectorAll('input[data-filter='+_filterkey+']:checked')).map(function(e1){
    //             return e1.value;
    //         });

    //     });
    //     console.log("thishs",_filterObj)
    //     // ajax starts
    //     $.ajax({
    //         type:'POST',
    //         url:'/filter-data',
            
    //         data : _filterObj,
    //         headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
    //         datatype:'json',
    //         beforeSend: function(){
    //            // $("#filterprodu").html('Loading......');
    //         },
    //         success: function(res){
    //             $("#filterproduct").html(res.data);
    //             var executeScript = function() {
    //                 const buttons = document.querySelectorAll('.color-button');
    //                 console.log(buttons);
    //                 buttons.forEach(button => {
    //                     const color = button.dataset.id;
    //                     console.log(color);
    //                     button.style.backgroundColor = color;
    //                 });
    //             };
                
    //             // Check if the DOM is already loaded
    //             if (document.readyState === 'loading') {
    //                 // If DOM is still loading, wait for it to be loaded
    //                 document.addEventListener('DOMContentLoaded', executeScript);
    //             } else {
    //                 // If DOM is already loaded, execute the script immediately
    //                 executeScript();
    //             }
    //         }
            
            

    //     });


    // });

  
});



