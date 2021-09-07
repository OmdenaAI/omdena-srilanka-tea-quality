$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();  
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/fresh_model/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').text(' Result:  ' + data);

                //$('#solution-div').text("SOLUTION:\n");
                if(data === 'Low Fresh - Below Best'){
                     $('#solution-div').append("HOW TO KEEP TEA LEAVES FRESH?:\n");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("\nDO<br/>Store Tea In an Airtight Container<br/>Keep Tea Dry>br/>Stay Away from Scents<br/><br/>DON'T<br/>Keep Tea Out In the Sunlight</br>Open Too Much Tea<br/>");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("REFERENCE LINK: https://bit.ly/3gMfeaf");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("<br/>");//$('#solution-div').attr('style','color:red;');
                }else if(data === 'Low Fresh - Best'){
                     $('#solution-div').append("HOW TO KEEP TEA LEAVES FRESH?:\n");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("\nAs tea leaves don’t expire easily, it’s quite possible to store them for a longer time than their expiration period. Tea leaves will stay fresh as long as you can keep them isolated. Most tea leaves are sold in paper or plastic bags. These bags can’t be sealed once they’re opened, and even if they can be sealed, that won’t be enough to keep them safe. <br/> So, it’s highly recommended to store these in tin cans with a tight sealing. If you manage to store them properly, then you’ll be able to keep them fresh for a pretty long time.A crucial thing to do is keep the tea leaves away from the mold. If they get moldy, they will lose their color, fragrance, and taste very soon. <br/>As long as you can keep them safe from these elements, they will be safe.<br/>");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("REFERENCE LINK: https://bit.ly/3t4vHvo");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("<br/>"); //$('#solution-div').attr('style','color:green;');
                }else if(data === 'Low Fresh - Poor'){
                     $('#solution-div').append("HOW TO KEEP TEA LEAVES FRESH?:\n");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("\nTea must be kept free from oxygen and heat. Tea must be kept away from light and from strong odors. Tea must be kept away from moisture and is best when stored in bulk.<br/>");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("REFERENCE LINK: https://bit.ly/2V57458");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("<br/>");
                     //$('#solution-div').attr('style','color:yellow;');
                }

                console.log('Success!');
            },
        });
    });

});
