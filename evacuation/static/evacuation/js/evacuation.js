
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

