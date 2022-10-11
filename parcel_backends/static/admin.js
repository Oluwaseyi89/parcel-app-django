const useFetch = async (url, meth, bod) => {
    function getCookie(name) {
        let cookieValue = null;
        if(document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i=0; i<cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1)) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    const csrftoken = getCookie('csrftoken');

    const res = await fetch(url, {
        method: meth,
        mode: "same-origin",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-CSRFToken": csrftoken,
            "X-Requested-With": "XMLHttpRequest"
        },
        body: JSON.stringify(bod)
    });

    const data = await res.json();

    return data;
}

let getVendor = document.getElementById('getPVend');
let getProd = document.getElementById('getProd');
let getCourier = document.getElementById('getCourier');
let apiContent = document.getElementById('apiContent');
let apiDetail = document.getElementById('apiDetail');
let couriers = document.getElementById('couriers');
let vendors = document.getElementById('vendors');
let products = document.getElementById('products');
const alt_msg = document.getElementById('alert-messages');


if (!apiDetail.innerHTML) {
    apiContent.style.width = '100%';
    apiDetail.style.width = '0%';
    apiDetail.style.marginRight = '-10px';
}

apiDetail.addEventListener('change', ()=>{
    // if (apiDetail.innerHTML) {
    //     apiContent.style.width = '70%';
    //     apiDetail.style.width = '30%';
    // }

    // if (window.innerWidth <= 414) {
    //     if (!apiDetail.innerHTML) {
    //         apiContent.style.width = '100%';
    //         apiDetail.style.width = '0%';
    //     } else {
    //         apiContent.style.width = '0%';
    //         apiDetail.style.width = '100%';
    //     }
    // }
    console.log('A change occured');
});

/**
*This function handles the actions on the potential vendor
*It is called the tempVendorManager
*tempVendorManager function starts here:
**/

const tempVendorManager = (id, data) => {
    let curVend = document.getElementById(id);
    curVend.addEventListener('click', () => {
        apiContent.style.width = "50%";
        apiDetail.style.width = "50%";
        if(window.innerWidth <= 414) {
            apiContent.style.width = "0%";
            apiDetail.style.width = "100%";
        }

        let apprId = `${data.id}` + '1';
        let susId = `${data.id}` + '2';
        let disId = `${data.id}` + '3';
        // let img_path = data.vend_photo;
        // let img_path = `http://localhost:7000/${data.vend_photo}`;

        apiDetail.innerHTML = "<div class='tempVenChild' >" 
                                + "<p>" + data.last_name + "  " + data.first_name + "</p>" 
                                +`<img class='img-thumbnail img-size' src=${data.vend_photo} />`
                                + "<table>" 
                                + "<tr>" + "<th>" + "Business Category:   " + "</th>" + "<td>" + data.bus_category + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "Business Address:   " + "</th>" + "<td>" + data.bus_street + " " + data.bus_state + " " + data.bus_country + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "Phone No.:   " + "</th>" + "<td>" + data.phone_no + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "E-mail:   " + "</th>" + "<td>" + data.email + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "CAC Reg No.:   " + "</th>" + "<td>" + data.cac_reg_no + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "NIN:   " + "</th>" + "<td>" + data.nin + "</td>" +"</tr>" 
                                + "</table>" + "<hr/>" 
                                + "<div class='venAction' >"  
                                + `<button id=${apprId} class='btn' >` + "Approve" + "</button>"
                                + `<button id=${susId}  class='btn' >` + "Suspend" + "</button>"
                                + `<button id=${disId}  class='btn' >` + "Discard" + "</button>"
                                +  "</div>" +
                                "</div>";
                let suspen = document.getElementById(susId);
                suspen.addEventListener('click', () => {
                    apiDetail.innerHTML = "";
                    apiDetail.style.width = "0%";
                    apiContent.style.width = "100%";
                });

                let approv = document.getElementById(apprId);
                approv.addEventListener('click', () => {
                    let welcome = document.getElementById('admin-welcome');
                    let staff_f_name = welcome.innerHTML.split(" ").pop();
                    let staff_l_name = welcome.innerHTML.split(" ").slice(1, -1)[0];
                    let appr_officer = staff_l_name + " " + staff_f_name;
                    let photo_url = "http://localhost:7000" + data.vend_photo;
                    const appr_date = new Date().toISOString();
                    const vendToDel = data.id;

                    const vendBody =  {
                        "first_name": data.first_name,
                        "last_name": data.last_name,
                        "bus_country": data.bus_country,
                        "bus_state": data.bus_state,
                        "bus_street": data.bus_street,
                        "bus_category": data.bus_category,
                        "cac_reg_no": data.cac_reg_no,
                        "nin": data.nin,
                        "phone_no": data.phone_no,
                        "email": data.email,
                        "vend_photo": photo_url,
                        "ven_policy": data.ven_policy,
                        "password": data.password,
                        "appr_officer": appr_officer,
                        "appr_date": appr_date,
                        "is_email_verified": data.is_email_verified
                    }


                    let apprVendor = useFetch('/parcel_backends/appr_vendor/', 'POST', vendBody);
                    apprVendor.then((res)=> {
                        if (res.status === "error") {
                            alt_msg.innerHTML =  '<div  class="alert alert-danger alert-dismissible" role="alert">'
                    + '<p id="error-alert-messages">' + res.data + '</p>' +
                        '<button class="close" role="alert" data-dismiss="alert">' + '<span>' + '&times;' + '</span>' + '</button>'
                    + '</div>';
            } else if (res.status === "success") {
                alt_msg.innerHTML =  '<div  class="alert alert-success alert-dismissible" role="alert">'
                + '<p id="error-alert-messages">' + res.data + '</p>' +
                    '<button class="close" role="alert" data-dismiss="alert">' + '<span>' + '&times;' + '</span>' + '</button>'
                + '</div>';
                useFetch(`/parcel_backends/del_temp_vendor/${data.id}/`, 'DELETE').then((res) => console.log(res.data)).
                catch((err) => console.log(err));
                console.log(data.email);

                } else {
                    alt_msg.innerHTML =  '<div  class="alert alert-danger alert-dismissible" role="alert">'
                    + '<p id="error-alert-messages">' + "An error occured, clear cookies to resolve" + '</p>' +
                        '<button class="close" role="alert" data-dismiss="alert">' + '<span>' + '&times;' + '</span>' + '</button>'
                    + '</div>';
                }
            }).catch((err)=>console.log(err));
                    // console.log(data.nin);
        });


                let discar = document.getElementById(disId);
                discar.addEventListener('click', () => {
                    alert('discarded' + `${disId}`);
                });
    });

}

// tempVendorManager function ends here.

/**
*This function handles the actions on the potential courier
*It is called the tempCourierManager
*courierManager function starts here:
**/

const tempCourierManager = (id, data) => {
    let curCour = document.getElementById(id);
    curCour.addEventListener('click', () => {
        apiContent.style.width = "50%";
        apiDetail.style.width = "50%";
        if(window.innerWidth <= 414) {
            apiContent.style.width = "0%";
            apiDetail.style.width = "100%";
        }

        let apprId = `${data.id}` + '1';
        let susId = `${data.id}` + '2';
        let disId = `${data.id}` + '3';
        // let img_path = data.vend_photo;
        // let img_path = `http://localhost:7000/${data._photo}`;

        apiDetail.innerHTML = "<div class='tempVenChild' >" 
                                + "<p>" + data.last_name + "  " + data.first_name + "</p>" 
                                +`<img class='img-thumbnail img-size' src=${data.cour_photo} />`
                                + "<table>" 
                                + "<tr>" + "<th>" + "Business Category:   " + "</th>" + "<td>" + "Courier" + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "Business Address:   " + "</th>" + "<td>" + data.bus_street + " " + data.bus_state + " " + data.bus_country + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "Phone No.:   " + "</th>" + "<td>" + data.phone_no + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "E-mail:   " + "</th>" + "<td>" + data.email + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "CAC Reg No.:   " + "</th>" + "<td>" + data.cac_reg_no + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "NIN:   " + "</th>" + "<td>" + data.nin + "</td>" +"</tr>" 
                                + "</table>" + "<hr/>" 
                                + "<div class='venAction' >"  
                                + `<button id=${apprId} class='btn' >` + "Approve" + "</button>"
                                + `<button id=${susId}  class='btn' >` + "Suspend" + "</button>"
                                + `<button id=${disId}  class='btn' >` + "Discard" + "</button>"
                                +  "</div>" +
                                "</div>";
                let suspen = document.getElementById(susId);
                suspen.addEventListener('click', () => {
                    apiDetail.innerHTML = "";
                    apiDetail.style.width = "0%";
                    apiContent.style.width = "100%";
                });

                let approv = document.getElementById(apprId);
                approv.addEventListener('click', () => {
                    let welcome = document.getElementById('admin-welcome');
                    let staff_f_name = welcome.innerHTML.split(" ").pop();
                    let staff_l_name = welcome.innerHTML.split(" ").slice(1, -1)[0];
                    let appr_officer = staff_l_name + " " + staff_f_name;
                    let photo_url = "http://localhost:7000" + data.cour_photo;
                    const appr_date = new Date().toISOString();
                    const vendToDel = data.id;

                    const courBody =  {
                        "first_name": data.first_name,
                        "last_name": data.last_name,
                        "bus_country": data.bus_country,
                        "bus_state": data.bus_state,
                        "bus_street": data.bus_street,
                        "cac_reg_no": data.cac_reg_no,
                        "nin": data.nin,
                        "phone_no": data.phone_no,
                        "email": data.email,
                        "cour_photo": photo_url,
                        "cour_policy": data.cour_policy,
                        "password": data.password,
                        "appr_officer": appr_officer,
                        "appr_date": appr_date,
                        "is_email_verified": data.is_email_verified
                    }


                    let apprCourier = useFetch('/parcel_backends/appr_courier/', 'POST', courBody);
                    apprCourier.then((res)=> {
                        if (res.status === "error") {
                            alt_msg.innerHTML =  '<div  class="alert alert-danger alert-dismissible" role="alert">'
                    + '<p id="error-alert-messages">' + res.data + '</p>' +
                        '<button class="close" role="alert" data-dismiss="alert">' + '<span>' + '&times;' + '</span>' + '</button>'
                    + '</div>';
            } else if (res.status === "success") {
                alt_msg.innerHTML =  '<div  class="alert alert-success alert-dismissible" role="alert">'
                + '<p id="error-alert-messages">' + res.data + '</p>' +
                    '<button class="close" role="alert" data-dismiss="alert">' + '<span>' + '&times;' + '</span>' + '</button>'
                + '</div>';
                useFetch(`/parcel_backends/del_temp_courier/${data.id}/`, 'DELETE').then((res) => console.log(res.data)).
                catch((err) => console.log(err));
                console.log(data.email);

                }
            }).catch((err)=>console.log(err));
                    
                });


                let discar = document.getElementById(disId);
                discar.addEventListener('click', () => {
                    alert('discarded' + `${disId}`);
                });
    });

}

// tempCourierManager function ends here.




/**
*This function handles the actions on the potential courier
*It is called the tempProductManager
*courierManager function starts here:
**/
const tempProductManager = (id, data) => {
    let curCour = document.getElementById(id);
    curCour.addEventListener('click', () => {
        apiContent.style.width = "50%";
        apiDetail.style.width = "50%";
        if(window.innerWidth <= 414) {
            apiContent.style.width = "0%";
            apiDetail.style.width = "100%";
        }

        let apprId = `${data.id}` + '1';
        let susId = `${data.id}` + '2';
        let disId = `${data.id}` + '3';
        // let img_path = data.vend_photo;
        // let img_path = `http://localhost:7000/${data._photo}`;

        apiDetail.innerHTML = "<div class='tempVenChild' >" 
                                + "<p>" + data.vendor_name + "</p>" 
                                +`<img class='img-thumbnail img-size' src=${data.prod_photo} />`
                                + "<table>" 
                                + "<tr>" + "<th>" + "Product Category:   " + "</th>" + "<td>" + data.prod_cat + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "Product Name and Model:   " + "</th>" + "<td>" + data.prod_name + " " + data.prod_model + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "Vendor Phone.:   " + "</th>" + "<td>" + data.vendor_phone + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "Vendor E-Mail:   " + "</th>" + "<td>" + data.vendor_email + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "Product Price.:   " + "</th>" + "<td>" + data.prod_price + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "Product Qty.:   " + "</th>" + "<td>" + data.prod_qty + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "Discount Allowed:   " + "</th>" + "<td>" + data.prod_disc + "</td>" +"</tr>" 
                                + "</table>" + "<hr/>" 
                                + "<div class='venAction' >"  
                                + `<button id=${apprId} class='btn' >` + "Approve" + "</button>"
                                + `<button id=${susId}  class='btn' >` + "Suspend" + "</button>"
                                + `<button id=${disId}  class='btn' >` + "Discard" + "</button>"
                                +  "</div>" +
                                "</div>";
                let suspen = document.getElementById(susId);
                suspen.addEventListener('click', () => {
                    apiDetail.innerHTML = "";
                    apiDetail.style.width = "0%";
                    apiContent.style.width = "100%";
                });

                let approv = document.getElementById(apprId);
                approv.addEventListener('click', () => {
                    let welcome = document.getElementById('admin-welcome');
                    let staff_f_name = welcome.innerHTML.split(" ").pop();
                    let staff_l_name = welcome.innerHTML.split(" ").slice(1, -1)[0];
                    let appr_officer = staff_l_name + " " + staff_f_name;
                    let photo_url = "http://localhost:7000" + data.prod_photo;
                    const appr_date = new Date().toISOString();
                    const prodToDel = data.id;

                    console.log(photo_url);

                    const prodBody =  {
                        "vendor_name": data.vendor_name,
                        "vendor_phone": data.vendor_phone,
                        "vendor_email": data.vendor_email,
                        "vend_photo": data.vend_photo,
                        "prod_cat": data.prod_cat,
                        "prod_name": data.prod_name,
                        "prod_model": data.prod_model,
                        "prod_photo": photo_url,
                        "prod_price": data.prod_price,
                        "prod_qty": data.prod_qty,
                        "prod_disc": data.prod_disc,
                        "prod_desc": data.prod_desc,
                        "img_base": data.img_base,
                        "appr_officer": appr_officer,
                        "appr_date": appr_date,
                        "updated_at": appr_date,
                    }


                    let apprProduct = useFetch('/parcel_product/appr_product/', 'POST', prodBody);
                    apprProduct.then((res)=> {
                        if (res.status === "error") {
                            alt_msg.innerHTML =  '<div  class="alert alert-danger alert-dismissible" role="alert">'
                    + '<p id="error-alert-messages">' + res.data + '</p>' +
                        '<button class="close" role="alert" data-dismiss="alert">' + '<span>' + '&times;' + '</span>' + '</button>'
                    + '</div>';
            } else if (res.status === "success") {
                alt_msg.innerHTML =  '<div  class="alert alert-success alert-dismissible" role="alert">'
                + '<p id="error-alert-messages">' + res.data + '</p>' +
                    '<button class="close" role="alert" data-dismiss="alert">' + '<span>' + '&times;' + '</span>' + '</button>'
                + '</div>';
                useFetch(`/parcel_product/del_temp_product/${data.id}/`, 'DELETE').then((res) => console.log(res.data)).
                catch((err) => console.log(err));
                console.log(data.email);

                } else {
                    alt_msg.innerHTML =  '<div  class="alert alert-danger alert-dismissible" role="alert">'
                    + '<p id="error-alert-messages">' + "An error occured! Clear cookies to resolve" + '</p>' +
                        '<button class="close" role="alert" data-dismiss="alert">' + '<span>' + '&times;' + '</span>' + '</button>'
                    + '</div>';   
                }
            }).catch((err)=>console.log(err));
                    
                });


                let discar = document.getElementById(disId);
                discar.addEventListener('click', () => {
                    alert('discarded' + `${disId}`);
                });
    });

}

// tempProductManager function ends here.




getVendor.addEventListener('click', () =>{
    let data = useFetch('/parcel_backends/get_temp_ven/', 'GET');
    data.then((res)=> {
        apiContent.innerHTML = "";
        apiContent.innerHTML = res.data.length > 1 ? ("<p class='apiHeading' >" + res.data.length + "  " + "Potential vendors are available" + "</p>") :
        ("<p class='apiHeading' >" + res.data.length + "  " + "Potential vendor is available" + "</p>");
        res.data.forEach((vendor) => {
            apiContent.innerHTML += "<div class='alert p-vend-item'>"
                + "<p>" + vendor.first_name + "</p>" + "<p>" + vendor.bus_category 
                + "</p>" + `<button id=${vendor.id} class="btn">`  + "View Details" 
                + "</button>" + "</div>";
            })
           res.data.forEach((vendor) =>{
            tempVendorManager(`${vendor.id}`, vendor);
           }); 
        });
    // console.log('clicked');
}, false);

getCourier.addEventListener('click', () =>{
    let data = useFetch('/parcel_backends/get_temp_cour/', 'GET');
    data.then((res)=> {
        apiContent.innerHTML = "";
        apiContent.innerHTML = res.data.length > 1 ?("<p class='apiHeading' >" + res.data.length + "  " + "Potential Couriers are available" + "</p>"):
        ("<p class='apiHeading' >" + res.data.length + "  " + "Potential Courier is available" + "</p>");
        res.data.forEach((courier) => {
            apiContent.innerHTML += "<div class='alert p-vend-item'>"
                + "<p>" + courier.last_name + "  " + courier.first_name + "</p>"  + `<button id=${courier.id} class="btn">`  + "View Details" 
                + "</button>" + "</div>";
            })
           res.data.forEach((courier) =>{
            tempCourierManager(`${courier.id}`, courier);
           }); 
        });
    // console.log('clicked');
}, false);


getProd.addEventListener('click', () =>{
    let data = useFetch('/parcel_product/get_temp_prod/', 'GET');
    data.then((res)=> {
        apiContent.innerHTML = "";
        apiContent.innerHTML = res.data.length > 1 ?("<p class='apiHeading' >" + res.data.length + "  " + "Potential Products are available" + "</p>"):
        ("<p class='apiHeading' >" + res.data.length + "  " + "Potential Product is available" + "</p>");
        res.data.forEach((product) => {
            apiContent.innerHTML += "<div class='alert p-vend-item'>"
                + "<p>" + product.prod_name + "  " + product.prod_model  + "</p>" + "<p>" + product.prod_cat + "</p>"   
                + `<button id=${product.id} class="btn">`  + "View Details" 
                + "</button>" + "</div>";
            })
           res.data.forEach((product) =>{
            tempProductManager(`${product.id}`, product);
           }); 
        });
    // console.log('clicked');
}, false);


/*
 *This function handles the actions on the vendor
 *It is called the vendorManager
 *vendorManager function starts here:
 */ 
const vendorManager = (id, data) => {
    let curVend = document.getElementById(id);
    curVend.addEventListener('click', () => {
        apiContent.style.width = "50%";
        apiDetail.style.width = "50%";
        if(window.innerWidth <= 414) {
            apiContent.style.width = "0%";
            apiDetail.style.width = "100%";
        }

        let apprId = `${data.id}` + '1';
        let susId = `${data.id}` + '2';
        let disId = `${data.id}` + '3';
        // let img_path = data.vend_photo;
        // let img_path = `http://localhost:7000/${data.vend_photo}`;

        apiDetail.innerHTML = "<div class='tempVenChild' >" 
                                + "<p>" + data.last_name + "  " + data.first_name + "</p>" 
                                +`<img class='img-thumbnail img-size' src=${data.vend_photo} />`
                                + "<table>" 
                                + "<tr>" + "<th>" + "Business Category:   " + "</th>" + "<td>" + data.bus_category + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "Business Address:   " + "</th>" + "<td>" + data.bus_street + " " + data.bus_state + " " + data.bus_country + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "Phone No.:   " + "</th>" + "<td>" + data.phone_no + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "E-mail:   " + "</th>" + "<td>" + data.email + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "CAC Reg No.:   " + "</th>" + "<td>" + data.cac_reg_no + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "NIN:   " + "</th>" + "<td>" + data.nin + "</td>" +"</tr>" 
                                + "</table>" + "<hr/>" 
                                + "<div class='venAction' >"  
                                + `<button id=${apprId} class='btn' >` + "Approve" + "</button>"
                                + `<button id=${susId}  class='btn' >` + "Suspend" + "</button>"
                                + `<button id=${disId}  class='btn' >` + "Discard" + "</button>"
                                +  "</div>" +
                                "</div>";
                let suspen = document.getElementById(susId);
                suspen.addEventListener('click', () => {
                    apiDetail.innerHTML = "";
                    apiDetail.style.width = "0%";
                    apiContent.style.width = "100%";
                });

                let approv = document.getElementById(apprId);
                approv.addEventListener('click', () => {
                        alert(`${apprId} is clicked`);
                });


                let discar = document.getElementById(disId);
                discar.addEventListener('click', () => {
                    alert(`${disId} is clicked`);
                });
    });

}

// vendorManager function ends here.



/**
*This function handles the actions on the courier
*It is called the courierManager
*courierManager function starts here:
**/

const courierManager = (id, data) => {
    let curCour = document.getElementById(id);
    curCour.addEventListener('click', () => {
        apiContent.style.width = "50%";
        apiDetail.style.width = "50%";
        if(window.innerWidth <= 414) {
            apiContent.style.width = "0%";
            apiDetail.style.width = "100%";
        }

        let apprId = `${data.id}` + '1';
        let susId = `${data.id}` + '2';
        let disId = `${data.id}` + '3';
        // let img_path = data.vend_photo;
        // let img_path = `http://localhost:7000/${data._photo}`;

        apiDetail.innerHTML = "<div class='tempVenChild' >" 
                                + "<p>" + data.last_name + "  " + data.first_name + "</p>" 
                                +`<img class='img-thumbnail img-size' src=${data.cour_photo} />`
                                + "<table>" 
                                + "<tr>" + "<th>" + "Business Category:   " + "</th>" + "<td>" + "Courier" + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "Business Address:   " + "</th>" + "<td>" + data.bus_street + " " + data.bus_state + " " + data.bus_country + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "Phone No.:   " + "</th>" + "<td>" + data.phone_no + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "E-mail:   " + "</th>" + "<td>" + data.email + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "CAC Reg No.:   " + "</th>" + "<td>" + data.cac_reg_no + "</td>" +"</tr>" 
                                + "<tr>" + "<th>" + "NIN:   " + "</th>" + "<td>" + data.nin + "</td>" +"</tr>" 
                                + "</table>" + "<hr/>" 
                                + "<div class='venAction' >"  
                                + `<button id=${apprId} class='btn' >` + "Approve" + "</button>"
                                + `<button id=${susId}  class='btn' >` + "Suspend" + "</button>"
                                + `<button id=${disId}  class='btn' >` + "Discard" + "</button>"
                                +  "</div>" +
                                "</div>";
                let suspen = document.getElementById(susId);
                suspen.addEventListener('click', () => {
                    apiDetail.innerHTML = "";
                    apiDetail.style.width = "0%";
                    apiContent.style.width = "100%";
                });

                let approv = document.getElementById(apprId);
                approv.addEventListener('click', () => {
                   alert(`${apprId} is clicked`)                    
                });


                let discar = document.getElementById(disId);
                discar.addEventListener('click', () => {
                    alert(`${disId} is clicked`);
                });
    });

}

// courierManager function ends here.



couriers.addEventListener('click', () =>{
    let data = useFetch('/parcel_backends/get_cour/', 'GET');
    data.then((res)=> {
        apiContent.innerHTML = "";
        apiContent.innerHTML = res.data.length > 1 ?("<p class='apiHeading' >" + res.data.length + "  " + "Couriers are available" + "</p>"):
        ("<p class='apiHeading' >" + res.data.length + "  " + "Courier is available" + "</p>");
        res.data.forEach((courier) => {
            apiContent.innerHTML += "<div class='alert p-vend-item'>"
                + "<p>" + courier.last_name + "  " + courier.first_name + "</p>"  + `<button id=${courier.id} class="btn">`  + "View Details" 
                + "</button>" + "</div>";
            })
           res.data.forEach((courier) =>{
            courierManager(`${courier.id}`, courier);
           }); 
        });
    // console.log('clicked');
}, false);



vendors.addEventListener('click', () =>{
    let data = useFetch('/parcel_backends/get_ven/', 'GET');
    data.then((res)=> {
        apiContent.innerHTML = "";
        apiContent.innerHTML = res.data.length > 1 ? ("<p class='apiHeading' >" + res.data.length + "  " + "vendors are available" + "</p>") :
        ("<p class='apiHeading' >" + res.data.length + "  " + "vendor is available" + "</p>");
        res.data.forEach((vendor) => {
            apiContent.innerHTML += "<div class='alert p-vend-item'>"
                + "<p>" + vendor.first_name + "</p>" + "<p>" + vendor.bus_category 
                + "</p>" + `<button id=${vendor.id} class="btn">`  + "View Details" 
                + "</button>" + "</div>";
            })
           res.data.forEach((vendor) =>{
            vendorManager(`${vendor.id}`, vendor);
           }); 
        });
    // console.log('clicked');
}, false);

// getCourier.addEventListener('click', () => {
//     alert('clicked');
// });

let reset = document.getElementById('reset');
reset.addEventListener('click', ()=> {
    apiContent.innerHTML = "";
    apiDetail.innerHTML = "";
    apiDetail.style.width = "0%";
    apiContent.style.width = "100%";
});

// const staff_img = document.getElementById('staff-img')
// const photo_img = document.getElementsByClassName('photo-img');

// if (staff_img.attribute.src === "") {
//     photo_img.style.display = "none";
// }

// photo_img.style.display = "none";

// window.addEventListener('load', () => {
//     let data = useFetch('parcel_backends/desk_login/', 'GET');
//     data.then((res)=>console.log(res));
// });



// data.dispatch_array.forEach((customer) => {
//     ready_orders.innerHTML += "<div>" 
//         + "<p>" + `${customer.order_id}` + "</p>"
//         + "<p>" + `${customer.customer_id}` + "</p>"
//         + "<p>" + `${customer.customer_name}` + "</p>"
//         + "<p>" + `${customer.address}` + "</p>"
//         + "<p>" + `${customer.email}` + "</p>"
//         +"<div>" + `${customer.products.forEach((item) => {
//             ready_orders.innerHTML += "<p>"
//                 + `${item.product_name}` + "</p>"})}` + "</div>"
//         + "</div>"



// ready_orders.innerHTML += data.dispatch_array.map((customer) => {
//     return (
//         <div>
//             <p>{customer.customer_name}</p>
//         </div>
//     )
// });
console.log('working');
