/**
 * This script checks if a user has been already created for this browser.
 * If so, just load the userId into a variable or an html element.
 * If not, send an AJAX requesting the creation of a new user, retrieving the
 * userId from the server and storing it locally for future use.
 *
 * Also, do some other stuff transferred from main.js
 */

var userId = localStorage.getItem('userId');

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(function($) {

	"use strict";

	[].slice.call( document.querySelectorAll( 'select.cs-select' ) ).forEach( function(el) {
		new SelectFx(el);
	} );

	$('.selectpicker').selectpicker;


	$('#menuToggle').on('click', function(event) {
		$('body').toggleClass('open');
	});

	$('.search-trigger').on('click', function(event) {
		event.preventDefault();
		event.stopPropagation();
		$('.search-trigger').parent('.header-left').addClass('open');
	});

	$('.search-close').on('click', function(event) {
		event.preventDefault();
		event.stopPropagation();
		$('.search-trigger').parent('.header-left').removeClass('open');
	});

    // load user_id
    if(userId == null){
//        $.post( "/new_user")
//            .done(function( response ) {
//                userId = response["user_id"];
//                localStorage.setItem('userId', userId);
//                console.log("User created: " + userId);
//                console.log("Reloading...");
//                location.reload();
//            });
    }
    else{
//        console.log("User detected: " + userId + ". Logging in...");
//        var csrftoken = getCookie('csrftoken');
//        $.ajaxSetup({
//            beforeSend: function(xhr, settings) {
//                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
//                }
//            }
//        });
//        $.post("/auto_login", { user_id: userId })
//            .done(function( response ) {
//                if(userId != response["user_id"]){
//                    alert("Something fishy going on...");
//                    return;
//                }
//                console.log("Logged in user: " + userId);
//                if(response["refresh"]){
//                    console.log("Reloading...");
//                    location.reload();
//                }
//            });
    }



});