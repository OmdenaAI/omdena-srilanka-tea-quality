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
            url: '/withered_model/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').text('Result: ' + data);
                
                // $('#solution-div').text("SOLUTION:\n")
                if(data === 'Low Withered - Below Best'){
                  //  alert('Disease is Sigatoka');
                     $('#solution-div').append("HOW TO KEEP TEA LEAVES FRESH?:\n");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("\nTo explore the relationship between the moisture content of withered tea leaves and their physical properties (i.e., elasticity, plasticity, flexibility, and texture) during withering, texture analyzer was employed to test the elasticity and flexibility of withered tea leaves with different moisture contents.<br/> The texture was evaluated by computer vision technology. The withered tea leaves with different moisture contents were used to process congou black tea, which was then subjected to sensory evaluation.<br/> Results showed that good elasticity, optimal flexibility, and plasticity were achieved when the moisture content of the withered tea leaves of Fudingdabai comprising two leaves and one bud varied arranging from 65.51 to 61.48%. The sensory evaluation of congou black tea revealed that moderate withering was better than long-term withering and that both moderate and long-term withering were better than no withering during processing. The moisture content was significantly correlated with the flexibility and plasticity of the withered tea leaves. Fresh tea leaves undergoing moderate withering with moisture content of 65.51-61.48% to process congou black tea, good tea shape and liquor color were achieved. This study provided new evidence that the moisture content of withered tea leaves significantly affected the quality of black tea.<br/>");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("REFERENCE LINK: https://bit.ly/3kByh8k");
                     //$('#solution-div').attr('style','color:red;');
                }else if(data === 'Low Withered - Best'){
                     $('#solution-div').append("HOW TO KEEP TEA LEAVES FRESH?:\n");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("\nWITHERING is the first and fore most steps involved in tea manufacture. The evaporation of moisture in the green leaf is brought about by blowing or moving air over the leaf in the withering trough. The current of air performs a two functions viz., conveying heat from the leaf as well as carrying away the water vapor through a bed of green leaves to achieve physical withering. Whenever the hygrometric difference is below 3°C, hot air is mixed in suitable proportion or heat energy is supplied to increase the hygrometric difference with the concomitant rise in the dry bulb temperature of air. But the dry bulb temperature of air after mixing should not exceed 35°C.<br/><br/>The following two conditions are essential for good withering: storage of fresh leaf for a minimum period of nine hours is absolutely essential to allow chemical changes to take place whether a physical wither is desired or not, to make a product with required characteristics, this is referred to as chemical wither. Physical wither is necessary for good fermentation.<br/>");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("REFERENCE LINK: https://bit.ly/38uevWG");
                     //$('#solution-div').attr('style','color:green;');
                }else if(data === 'Low Withered - Poor'){
                     $('#solution-div').append("WHAT HAPPENS DURING WITHERING?\n");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("\nThe tea leaves go limp.<br/>Moisture loss in tea leaves.<br/> Oxygen absorption begins.<br/> Biochemical changes.<br/>For the most part, two main factors contribute most to an effective wither. These two are temperature and humidity. They’re important to consider because they both affect the rate of moisture loss, while also affecting the physiology of the leaves and their internal biochemical changes. Big words there.<br/>");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("HOW TO KEEP TEA LEAVES FRESH?:\n");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("\nIt’s a crucial step in the crafting and manufacturing of black and oolong teas. It serves multiple purposes including preparing the leaves for more effective machining, and prepping their physical status for general rolling and fermentation. Withering kickstarts the internal biochemical machinery that will transform the complex chemical-soup of the raw tea leaf into an equally complex but different chemical-soup of a black tea.<br/>");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("REFERENCE LINK: https://bit.ly/3Dq8mc6");
                     $('#solution-div').append("<br/>");
                     $('#solution-div').append("<br/>");
                     //$('#solution-div').attr('style','color:yellow;');
                }
                
                
                
                
                console.log('Success!');
            },
        });
    });

});
