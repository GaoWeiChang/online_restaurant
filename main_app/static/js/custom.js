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
            $('#id_latitude').val(latitude)
            $('#id_longtitude').val(longtitude)
        }
    })    
}
