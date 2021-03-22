"'use strict';\n"
$.ajaxSetup({
    xhrFields: {
        withCredentials: true,
    },
});
var guest_form = {
    init: function () {
    if (window.location.href.indexOf("/render/") !== -1) this.form_id = window.location.href.split("/render/")[1].split("/")[0];
    this.base_url = window.location.origin
    this.app = window.location.pathname.split("/")[1];
    this.bindEvents();
    },

bindEvents: function() {
    var that = this
    $(document).on("click", "#home", function () {
        $(".home").addClass("active");
        // $("#form_list").removeClass("active");
    });
    $(document).on("click", "#form_list", function () {
        $("#form_list").addClass("active");
        $(".home").removeClass("active");
    });
    

    $(document).on("click", "#submit_btn", function () {
        that.guest_signup(that.form_id);
        return false
    });

    $(document).on("change", "#email", function () {
        that.email_validation();
    });
},
showAlertBox: function (type, msg, parent, showTime) {
    if (showTime != -1 && !showTime) showTime = 5000;
    var div = document.createElement("div");
    var style = "alert fade show mt-2 mb-2 w-100";
    if (type == "error") style += " alert-danger ";
    else if (type == "success") style += " alert-success ";
    else if (type == "warning") style += " alert-warning ";
    else style += " alert-primary ";
    if (showTime != -1) style += " alert-dismissible ";

    div.setAttribute("class", style);
    if (showTime != -1) {
        var a = document.createElement("a");
        a.setAttribute("href", "#");
        a.setAttribute("class", "close");
        a.setAttribute("data-dismiss", "alert");
        a.setAttribute("aria-label", "close");
        a.innerHTML = "&times;";
        div.appendChild(a);
    }
    var span = document.createElement("span");
    span.innerText = msg;
    div.appendChild(span);
    if (typeof parent === "string") document.getElementById(parent).appendChild(div);
    else parent.append(div);
    if (showTime != -1) {
        window.setTimeout(function () {
            // $(div).alert('close')
            $(div)
                .fadeTo(1000, 0)
                .slideUp(1000, function () {
                    $(this).remove();
                });
        }, showTime);
    }
},

    email_validation: function() {
        var that = this
        var email = $("#email").val();
        let email_regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if (email.length == 0 || !email_regex.test(email)) {
            alert("Please enter a valid email address")
            that.showAlertBox("error", "Please enter a valid email address", $("#email").parent(), 20000);
        } 

        },


    guest_signup: function(){
        var that = this
        var name = $("#name").val();
        var email = $("#email").val();
        var mobile_number = $("#mobile_number").val();
        var gender = $(document).find("input[type='radio']:checked").val();
        var array = []
        var checkboxes = document.querySelectorAll('input[type=checkbox]:checked')
        for (var i = 0; i < checkboxes.length; i++) {
        array.push(checkboxes[i].value)
        }
        let subject = array;
        let email_regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        let username_regex = /^[a-zA-Z0-9]+$/;
        let mobile_no_regex = /^\d{10}$/;
        if (!username_regex.test(name)) {
            that.showAlertBox("error", "name must contain only letters and numbers", $("#name").parent());
        } else if (name.length == 0) {
            that.showAlertBox("error", "Please enter your first name", $("#name").parent());
        } else  if (email.length == 0 || !email_regex.test(email)) {
            that.showAlertBox("error", "Please enter a valid email address", $("#email").parent(), 20000);
        } else  if (gender.length == 0) {
            that.showAlertBox("error", "Please select your gender", $("#gender").parent(), 20000);
        } else if (mobile_number.length == 0 || !mobile_no_regex.test(mobile_number)) {
            that.showAlertBox("error", "Please enter a valid mobile number", $("#mobile_number").parent());
        } else if (subject.length == 0) {
            that.showAlertBox("error", "Please select atleast one subject", $("#submit_btn").parent());
        }else {
            var data = JSON.stringify({
                name: name,
                mobile_number: mobile_number,
                email: email,
                gender: gender,
                subject: subject,
                baseurl: that.base_url,
            });
            $("#submit_btn").attr("disabled", true);
            $.ajax({
                url:"http://localhost:5000/submit/"+ that.form_id + "/",
                type: "POST",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                data: data,
                success: function (result) {
                    if (!result.isSuccess) that.showAlertBox("error", result.msg, $("#submit_btn").parent(), 20000);
                    else {
                        that.showAlertBox("success", result.msg, $("#submit_btn").parent(), 30000);
                        // $("#name, #mobile_number, #signup_last_name, #signup_email, #signup_password, #signup_cpassword").val("");
                    }
                    $("#submit_btn").attr("disabled", false);
                },
                error: function () {
                    $("#submit_btn").attr("disabled", false);
                    that.showAlertBox("error", "We were unable submit the guest details. Please refresh your page or try again later.", $("#submit_btn").parent(), 30000);
                },
            });
        }
    },

};

$(document).ready(function () {
    guest_form.init(5333333333342332);
});