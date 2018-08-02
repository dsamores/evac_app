/**
 * This script checks if a user has been already created for this browser.
 * If so, just load the userId into a variable or an html element.
 * If not, send an AJAX requesting the creation of a new user, retrieving the
 * userId from the server and storing it locally for future use.
 *
 * Also, do some other stuff transferred from main.js
 */

var userId = localStorage.getItem('userId');

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
        $.post( "/new_user")
            .done(function( response ) {
                userId = response["user_id"];
                localStorage.setItem('userId', userId);
                console.log("User created: " + userId);
            });
    }
    else{
        console.log("User detected: " + userId);
        // Maybe load to an HTML tag
    }



});