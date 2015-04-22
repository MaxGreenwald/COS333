Parse.initialize("Ntrn4oOn926ELlVzwozZL2hJpR3OHN87Z0vIr8f0", "119CjghihfTpAA0qHFt5l6xyyiThZuJks1Zzt0cK");

function showUsers() {
	var users = Parse.Object.extend("User");
	var query = new Parse.Query(users);

	query.find({
		success: function(results) {
			// alert("Successfully retrieved " + results.length + " scores.");

			var dataset = results.map(function(result) {
				var row = [];
				row.push(result.get("firstName"));
				row.push(result.get("lastName"));
				row.push(result.get("phoneNumber"));
				return row;
			});
			displayUsers(dataset);
		},
		error: function(error) {
			alert("Error: " + error.code + " " + error.message);
		}
	});

}



function displayUsers(dataSet) {

	$('#users').html( '<table cellpadding="0" cellspacing="0" border="0" class="display" id="userTable"></table>' );
//alert($('#userTable').DataTable)
$('#userTable').DataTable( {
	"data": dataSet,
	"columns": [
	{ "title": "First Name" },
	{ "title": "Last Name" },
	{ "title": "Phone Number "}
	]
} ); 

}








  // This is called with the results from from FB.getLoginStatus().
  function statusChangeCallback(response) {
  	console.log('statusChangeCallback');
  	console.log(response);
    // The response object is returned with a status field that lets the
    // app know the current login status of the person.
    // Full docs on the response object can be found in the documentation
    // for FB.getLoginStatus().
    if (response.status === 'connected') {
      // Logged into your app and Facebook.
      linkToParse();
  } else if (response.status === 'not_authorized') {
      // The person is logged into Facebook, but not your app.
      document.getElementById('status').innerHTML = 'Please log ' +
      'into this app.';
  } else {
      // The person is not logged into Facebook, so we're not sure if
      // they are logged into this app or not.
      document.getElementById('status').innerHTML = 'Please log ' +
      'into Facebook.';
  }
}

  // This function is called when someone finishes with the Login
  // Button.  See the onlogin handler attached to it in the sample
  // code below.
  function checkLoginState() {
  	FB.getLoginStatus(function(response) {
  		statusChangeCallback(response);
  	});
  }


window.fbAsyncInit = function() {
  Parse.FacebookUtils.init({
    appId      : '1094688440545035',
    cookie     : true,  // enable cookies to allow the server to access 
                        // the session
    xfbml      : true,  // parse social plugins on this page
    version    : 'v2.2' // use version 2.2
  });

  // Now that we've initialized the JavaScript SDK, we call 
  // FB.getLoginStatus().  This function gets the state of the
  // person visiting this page and can return one of three states to
  // the callback you provide.  They can be:
  //
  // 1. Logged into your app ('connected')
  // 2. Logged into Facebook, but not your app ('not_authorized')
  // 3. Not logged into Facebook and can't tell if they are logged into
  //    your app or not.
  //
  // These three cases are handled in the callback function.

  FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
  });

  };
  // Load the SDK asynchronously
  (function(d, s, id) {
  	var js, fjs = d.getElementsByTagName(s)[0];
  	if (d.getElementById(id)) return;
  	js = d.createElement(s); js.id = id;
  	js.src = "//connect.facebook.net/en_US/sdk.js";
  	fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));

  // Here we run a very simple test of the Graph API after login is
  // successful.  See statusChangeCallback() for when this call is made.

  function linkToParse() {


  	Parse.FacebookUtils.logIn(null, {
  		success: function(swapUserWithLocation) {
  			if (!swapUserWithLocation.existed()) {
  				alert("User signed up and logged in through Facebook!");
  			} else {
  				alert("User logged in through Facebook!");
  			}
  			$("#showSwap").show();
  		},
  		error: function(swapUserWithLocation, error) {
  			alert("User cancelled the Facebook login or did not fully authorize.");
  		}
  	});





  	console.log('Welcome!  Fetching your information.... ');
  	FB.api('/me', function(response) {
  		console.log('Successful login for: ' + response.name);
  		document.getElementById('status').innerHTML =
  		'Thanks for logging in, ' + response.name + '!';
  	});
  }

  function fbLogout() {
  	FB.logout(function (response) {
            //Do what ever you want here when logged out like reloading the page
            window.location.reload();
        });
  }







