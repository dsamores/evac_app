
function Interaction(type, description, page, element){
    this.userId = localStorage.getItem('userId');
    this.type = type;
    this.description = description;
    this.page = page;
    this.element = element;
    this.time = Date.now();

    this.save = function(){
        if(this.userId == null){
            console.log('User ID hasn\'t been set yet. Skipping this interaction.');
            return;
        }
        var interactions = localStorage.getItem("interactions");
        if(!interactions)
            interactions = new Array();
        else
            interactions = JSON.parse(interactions);
        interactions.push(this);
        localStorage.setItem("interactions", JSON.stringify(interactions));
    }
}

function flushInteractions(){
    var interactions = localStorage.getItem("interactions");
    if(interactions){
        //interactions = JSON.parse(interactions);
        $.post("/save_interactions", { interactions: interactions })
            .done(function( response ) {
                console.log(response);
                if(response['success'])
                    localStorage.removeItem("interactions");
            });
    }
}

$(document).ready(function($) {

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    (new Interaction('access', '', window.location.href, null)).save();
    var notification_ids = $.map( $('[name="notification_id"]'), function( n, i ) {
      return n.value;
    });
    if(notification_ids.length > 0){
        $.post("/read_notifications", { notification_ids: notification_ids })
            .done(function( response ) {
                console.log(response);
                (new Interaction('notification', 'Viewed ' + notification_ids.length + ' new notifications', window.location.href, null)).save();
            });
    }

    setInterval(function() {
         flushInteractions();
    }, 5000);
});

/* Save menu clicks */
$("#main-menu a").click(function(){
    (new Interaction('menu-click', $(this).attr('href'), window.location.href, null)).save();
});

document.addEventListener('touchstart', handleTouchStart, false);
document.addEventListener('touchmove', handleTouchMove, false);
document.addEventListener('touchend', handleTouchEnd, false);

var xDown = null;
var yDown = null;
var xUp = null;
var yUp = null;
var eventType;

function getTouches(evt) {
  return evt.touches ||             // browser API
         evt.originalEvent.touches; // jQuery
}

function handleTouchStart(evt) {
    xDown = getTouches(evt)[0].clientX;
    yDown = getTouches(evt)[0].clientY;
    eventType = 'tap';
};

function handleTouchMove(evt) {
    if ( ! xDown || ! yDown ) {
        return;
    }

    xUp = evt.touches[0].clientX;
    yUp = evt.touches[0].clientY;

    var xDiff = xDown - xUp;
    var yDiff = yDown - yUp;

    if ( Math.abs( xDiff ) > Math.abs( yDiff ) ) {
        if ( xDiff > 5 ) {
            /* left swipe */
            eventType = 'left-swipe';
        } else if ( xDiff < -5 ){
            /* right swipe */
            eventType = 'right-swipe';
        }
    } else {
        if ( yDiff > 5 ) {
            /* up swipe */
            eventType = 'up-swipe';
        } else if ( yDiff < -5 ) {
            /* down swipe */
            eventType = 'down-swipe';
        }
    }
};

function handleTouchEnd(evt) {
    if(eventType == 'tap'){
        (new Interaction(eventType, xDown + "," + yDown, window.location.href, null)).save();
    }
    else{
        (new Interaction(eventType, xDown + "," + yDown + "-" + xUp + "," + yUp, window.location.href, null)).save();
    }

    xDown = null;
    yDown = null;
    xUp = null;
    yUp = null;
};

$("#content a").click(function(){
    (new Interaction('link-click', $(this).attr('href'), window.location.href, null)).save();
});