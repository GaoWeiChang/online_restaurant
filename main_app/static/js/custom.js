let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'), // id come from id inside the tag
    {
        types: ['geocode', 'establishment'],
        // add your country code
        componentRestrictions: {'country': ['tw']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();
    // console.log(place) // show all place details, print and click inspect in UI

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
    var geocoder = new google.maps.Geocoder() // แปลงที่อยู่แบบข้อความ (เช่น "กรุงเทพฯ, ประเทศไทย") ให้เป็นพิกัดทางภูมิศาสตร์ (ละติจูดและลองจิจูด) vice versa
    var address = document.getElementById('id_address').value

    geocoder.geocode({'address':address}, function(results, status){
        // console.log('results=>', results)
        // console.log('status=>', status)
        if(status == google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longtitude = results[0].geometry.location.lng();

            // console.log("lat",latitude)
            // console.log("long",longtitude)

            // ใช้ jQuery เพื่อกำหนดค่าให้กับ input field 
            $('#id_latitude').val(latitude) // $('#id').val(value)
            $('#id_longtitude').val(longtitude)
            $('#id_address').val(address)
        }
    });

    console.log(place.address_components)

    // loop through the address components and assign other address data
    // console.log(place.address_components);
    for(var i=0; i<place.address_components.length; i++){
        for(var j=0; j<place.address_components[i].types.length; j++){
            // get country
            if(place.address_components[i].types[j] == 'country'){
                $('#id_country').val(place.address_components[i].long_name);
            }
            // get state (in this case district)
            if(place.address_components[i].types[j] == 'administrative_area_level_2'){
                $('#id_state').val(place.address_components[i].long_name);
            }
            // get city
            if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_city').val(place.address_components[i].long_name);
            }
            // zipcode
            if(place.address_components[i].types[j] == 'postal_code'){
                $('#id_pin_code').val(place.address_components[i].long_name);
            }else{
                $('#id_pin_code').val("");
            }
        }
    }
}

$(document).ready(function(){
    $('.add_to_cart').on('click', function(e){
        e.preventDefault(); // ป้องกันการทำงานปกติของลิงก์ (เช่น การนำทางไปยัง URL ที่ระบุใน href) เมื่อมีการคลิก
        
        // data-* ใช้เพื่อเก็บข้อมูลส่วนตัวหรือข้อมูลเพิ่มเติมในองค์ประกอบ HTML
        food_id = $(this).attr('data-id'); // get data-id attrbute
        url = $(this).attr('data-url');
        data = {
            food_id: food_id,
        }
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response){
                console.log(response)
            }
        })
    })
})