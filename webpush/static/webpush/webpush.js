// Based On https://github.com/chrisdavidmills/push-api-demo/blob/283df97baf49a9e67705ed08354238b83ba7e9d3/main.js

var isPushEnabled = false,
  subBtn,
  messageBox,
  registration;

window.addEventListener('load', function() {
  subBtn = document.getElementById('webpush-subscribe-button');
  messageBox = document.getElementById('webpush-message');

    if ('serviceWorker' in navigator && 'PushManager' in window) {
      console.log('Service Worker and Push is supported');

        var serviceWorker = document.querySelector('meta[name="service-worker-js"]').content;
        navigator.serviceWorker.register(serviceWorker)
          .then(
            function(reg) {
              subBtn.textContent = 'Loading....';
              registration = reg;
                initializeUI();

            }
          )
      .catch(function(error) {
      messageBox.textContent = 'Service Worker Error' + error ;
      });
    } else {
      messageBox.textContent = 'Push messaging is not supported';
      subBtn.textContent = 'Push Not Supported';
    }


    function initializeUI() {

      subBtn.addEventListener('click', function() {
            subBtn.disabled = true;
            if (isSubscribed) {
              //unsubscribe();
            } else {
              //subscribeUser();
              initialiseState(registration);
            }
          });

      // Set the initial subscription value
      registration.pushManager.getSubscription()
      .then(function(subscription) {
        isSubscribed = !(subscription === null);

        if (isSubscribed) {
          console.log('User IS subscribed.');
        } else {
          console.log('User is NOT subscribed.');
        }

        updateBtn();
        //invisibleSubscription();
      });
    }

    function updateBtn() {
      if (Notification.permission === 'denied') {
        subBtn.textContent = 'Push Messaging Blocked.';
        subBtn.disabled = true;
        return;
      }

      if (isSubscribed) {
        subBtn.textContent = 'Already subscribed. Thanks!';
        subBtn.disabled = true;
      } else {
        subBtn.textContent = 'Enable Push Messaging';
        subBtn.disabled = false;
        if(window.location.href.includes("alerts")){
            subBtn.click();
        }
      }

    }

  // Once the service worker is registered set the initial state  
  function initialiseState(reg) {
    // Are Notifications supported in the service worker?  
    if (!(reg.showNotification)) {
        // Show a message and activate the button
        messageBox.textContent = 'Showing Notification is not suppoted in your browser';
        updateBtn();
        //messageBox.style.display = 'block';
        return;
    }

    // We need to subscribe for push notification and send the information to server  
    subscribe(reg);
  }

  function invisibleSubscription(){
    subBtn.style.display = 'none';
    if(subBtn.textContent == 'Enable Push Messaging'){
        subBtn.click();
    }
    else if(subBtn.textContent == 'Already subscribed. Thanks!'){
        console.log('User already registered');
    }
    else{
        console.log('Couldn\'t subscribe user:', subBtn.textContent);
    }
  }

function subscribe(reg) {
  // Get the Subscription or register one
  getSubscription(reg).then(
      function(subscription) {
        postSubscribeObj('subscribe',subscription);
      }
    )
    .catch(
      function(error) {
        console.log('Subscription error.', error);
        updateBtn();
      }
    )
}

}
);



function urlB64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (var i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

function getSubscription(reg) {
    return reg.pushManager.getSubscription().then(
        function(subscription) {
          var metaObj, applicationServerKey, options;
          // Check if Subscription is available
          if (subscription) {
            return subscription;
          }

          metaObj = document.querySelector('meta[name="django-webpush-vapid-key"]');
          applicationServerKey = metaObj.content;
          options = {
              userVisibleOnly: true
          };
          if (applicationServerKey){
              options.applicationServerKey = urlB64ToUint8Array(applicationServerKey)
          }
          // If not, register one
          return registration.pushManager.subscribe(options)
        }
      )
}

function unsubscribe() {
  // Get the Subscription to unregister
  registration.pushManager.getSubscription()
    .then(
      function(subscription) {

        // Check we have a subscription to unsubscribe
        if (!subscription) {
          // No subscription object, so set the state
          // to allow the user to subscribe to push
          subBtn.disabled = false;
          messageBox.textContent = 'Subscription is not available';
          //messageBox.style.display = 'block';
          return;
        }
        postSubscribeObj('unsubscribe', subscription);
      }
    )  
}

function postSubscribeObj(statusType, subscription) {
  // Send the information to the server with fetch API.
  // the type of the request, the name of the user subscribing, 
  // and the push subscription endpoint + key the server needs
  // to send push messages
  
  var browser = navigator.userAgent.match(/(firefox|msie|chrome|safari|trident)/ig)[0].toLowerCase(),
    data = {  status_type: statusType,
              subscription: subscription.toJSON(),
              browser: browser,
              group: subBtn.dataset.group
           };

  fetch(subBtn.dataset.url, {
    method: 'post',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data),
    credentials: 'include'
  })
    .then(
      function(response) {
        // Check the information is saved successfully into server
        if ((response.status == 201) && (statusType == 'subscribe')) {
          // Show unsubscribe button instead
          subBtn.textContent = 'Already subscribed. Thanks!';
          subBtn.disabled = true;
          isPushEnabled = true;
          messageBox.textContent = 'Successfully subscribed for Push Notification';
          //messageBox.style.display = 'block';
          console.log('User now subscribed');
        }

        // Check if the information is deleted from server
        if ((response.status == 202) && (statusType == 'unsubscribe')) {
          // Get the Subscription
          getSubscription(registration)
            .then(
              function(subscription) {
                // Remove the subscription
                subscription.unsubscribe()
                .then(
                  function(successful) {
                    subBtn.textContent = 'Enable Push Messaging';
                    messageBox.textContent = 'Successfully unsubscribed for Push Notification';
                    //messageBox.style.display = 'block';
                    isPushEnabled = false;
                    subBtn.disabled = false;
                  }
                )
              }
            )
            .catch(
              function(error) {
                subBtn.textContent = 'Already subscribed. Thanks!';
                messageBox.textContent = 'Error during unsubscribe from Push Notification';
                //messageBox.style.display = 'block';
                subBtn.disabled = true;
              }
            );
        }
      }
    )
}
