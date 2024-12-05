$(document).ready(function(){
 
    $("a.image").on("click", function(){
        new_img = $(this).attr("id");
        bigImg = document.getElementById("bigImg");
        bigImg.src=new_img;
    });
});

$(document).ready(function(){
    
    $("a.basket").on("click", function(){
        var clicked_obj = $(this);
        product_id = clicked_obj.attr('id');
        $.ajax({
            url: '/addtobasket',
            type: 'POST',
            data: JSON.stringify({ product_id: product_id}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response){
                console.log(response);
            },
            error: function(error){
                console.log(error);
            }
        });
    });
});
