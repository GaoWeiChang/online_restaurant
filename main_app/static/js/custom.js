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
    // add to cart
    $('.add_to_cart').on('click', function(e){
        e.preventDefault(); // ป้องกันการทำงานปกติของลิงก์ (เช่น การนำทางไปยัง URL ที่ระบุใน href) เมื่อมีการคลิก
        
        // data-* ใช้เพื่อเก็บข้อมูลส่วนตัวหรือข้อมูลเพิ่มเติมในองค์ประกอบ HTML
        food_id = $(this).attr('data-id'); // get data-id attrbute
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.status == 'login_required'){
                    //swal(title, subtitle, theme)
                    swal(response.message, '', 'info').then(function(){
                        window.location = '/login';
                    })
                }
                else if(response.status == 'Failed'){
                    swal(response.message, '', 'error')
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count']); // print to console and click inspect to see cart_counter
                    $('#qty-'+food_id).html(response.qty);
                    console.log(response)
                    // subtotal, tax and grand total
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total']
                    )
                }
            }
        })
    })

    // place the cart item quantity on load
    $('.item_qty').each(function(){
        var _id = $(this).attr('id')
        var _qty = $(this).attr('data-qty')
        /* 
            .html()) จะดึงเนื้อหา HTML ภายในองค์ประกอบที่เลือก
            .html(_qty) กำหนดให้เนื้อหาภายในองค์ประกอบมีค่าเท่ากับ _qty
        */
        $('#'+_id).html(_qty) // เปลี่ยนเนื้อหาของ element ที่มี id เดียวกัน 
        // ex. "#qty-101" เป็น CSS selector ที่เลือกองค์ประกอบที่มี id="qty-101" เเล้วกำหนดให้เนื้อหาภายในองค์ประกอบมีค่าเท่ากับ _qty
    })

    // decrease cart
    $('.decrease_cart').on('click', function(e){
        e.preventDefault(); // ป้องกันการทำงานปกติของลิงก์ (เช่น การนำทางไปยัง URL ที่ระบุใน href) เมื่อมีการคลิก
        
        // data-* ใช้เพื่อเก็บข้อมูลส่วนตัวหรือข้อมูลเพิ่มเติมในองค์ประกอบ HTML
        cart_id = $(this).attr('id'); 
        food_id = $(this).attr('data-id'); // get data-id attrbute
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.status == 'login_required'){
                    //swal(title, subtitle, theme)
                    swal(response.message, '', 'info').then(function(){
                        window.location = '/login';
                    })
                }
                else if(response.status == 'Failed'){
                    swal(response.message, '', 'error')
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count']); // print to console and click inspect to see cart_counter
                    $('#qty-'+food_id).html(response.qty);

                    // subtotal, tax and grand total
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total']
                    )

                    if(window.location.pathname == '/cart/'){
                        removeCartItem(response.qty, cart_id)
                        checkEmptyCart();
                    }
                }
            }
        })
    })

    // delete cart item
    $('.delete_cart').on('click', function(e){
        e.preventDefault(); // ป้องกันการทำงานปกติของลิงก์ (เช่น การนำทางไปยัง URL ที่ระบุใน href) เมื่อมีการคลิก
        
        cart_id = $(this).attr('data-id'); // get data-id attrbute
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.status == 'Failed'){
                    swal(response.message, '', 'error')
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count']); // print to console and click inspect to see cart_counter
                    swal(response.status, response.message, "success")
                    
                    // subtotal, tax and grand total
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total']
                    )   

                    removeCartItem(0, cart_id);
                    checkEmptyCart();
                }
            }
        })
    })

    // delete cart element if the qty is 0
    function removeCartItem(qty, cart_id){
        if(qty <= 0){
            document.getElementById("cart-item-"+cart_id).remove()
        }
    }

    // check if the cart is empty
    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if (cart_counter == 0) {
            document.getElementById('empty-cart').style.display = 'block'; // enable display in UI
        }
    }

    // apply cart amount
    function applyCartAmounts(subtotal, tax_dict, grandtotal){
        if(window.location.pathname == '/cart/'){
            $('#subtotal').html(subtotal)
            $('#total').html(grandtotal)

            for(key1 in tax_dict){
                for(key2 in tax_dict[key1]){
                    $('#tax-'+key1).html(tax_dict[key1][key2]);
                }
            }
        }
    }

    // add opening hours
    $('.add_hour').on('click', function(e){
        e.preventDefault();
        var day = document.getElementById('id_day').value // find id from inspect the UI (required_id)
        var from_hour = document.getElementById('id_from_hour').value
        var to_hour = document.getElementById('id_to_hour').value
        var is_closed = document.getElementById('id_is_closed').checked
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val() // use name inside the input tag
        var url = document.getElementById('add_hour_url').value
        // console.log(day, from_hour, to_hour, is_closed, csrf_token)

        if(is_closed){
            is_closed = 'True'
            condition = "day != ''"
        }else{
            is_closed = 'False'
            condition = "day != '' && from_hour != '' && to_hour != ''"
        }

        if(eval(condition)){
            $.ajax({ // ajax request
                type: 'POST',
                url: url,
                data: {
                    'day': day,
                    'from_hour': from_hour,
                    'to_hour': to_hour,
                    'is_closed': is_closed,
                    'csrfmiddlewaretoken': csrf_token,
                },
                success: function(response){ // response from views.py
                    if(response.status == 'success'){
                        if(response.is_closed == 'Closed'){ 
                            html = '<tr id="hour-'+response.id+'"> <td><b>'+ response.day +'</b></td> <td>Closed</td> <td><a href="#" class="remove_hour" data-url="/restaurant/opening-hours/remove/'+ response.id +'/">Remove</a></td></tr>';
                        }else{
                            html = '<tr id="hour-'+response.id+'"> <td><b>'+ response.day +'</b></td> <td>'+ response.from_hour + ' - '+ response.to_hour + '</td> <td><a href="#" class="remove_hour" data-url="/restaurant/opening-hours/remove/'+ response.id +'/">Remove</a></td></tr>';
                        }
                        $(".opening_hours").append(html);
                        document.getElementById('opening_hours').reset(); // reset the form
                    }else{
                        swal(response.message, '', 'error')
                    }
                }
            })
        }else{
            swal('Please fill all field', '', 'info')
        }
    });

    // remove opening hours
    // Event Delegation - วิธีเขียนเเบบนี้ใช้เทคนิค event delegation ซึ่งทำให้สามารถจัดการกับองค์ประกอบที่สร้างขึ้นใหม่หลังจากที่โค้ด JavaScript ทำงานแล้ว
    $(document).on('click', '.remove_hour', function(e){
        e.preventDefault();
        url = $(this).attr('data-url');
        
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.status == 'success'){
                    document.getElementById('hour-'+response.id).remove();
                }
            }
        })
    });

    // วิธีนี้จะผูกอีเวนต์โดยตรงกับองค์ประกอบที่มีคลาส .remove_hour ที่มีอยู่ในเวลาที่โค้ด JavaScript ทำงาน (เมื่อเพจโหลดครั้งแรก) เท่านั้น
    // $('.remove_hour').on('click', function(e){

    // });

    // document ready close

});