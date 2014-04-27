var signInButton = document.getElementById('signin');
if (signInButton) {
  signInButton.onclick = function() { navigator.id.request(); };
}
var signOutButton = document.getElementById('signout');
if (signOutButton) {
  signOutButton.onclick = function() { navigator.id.logout(); };
}
$.ajax({url: '/auth/status', success: loggedIn, error: loggedOut});


var currentUser = 'Julian@GrayVines.com'
navigator.id.watch({
    loggedInUser: currentUser,
    onlogin: function(assertion) {
        $.ajax({
            type: 'POST',
            url: '/auth/login',
            data: {assertion: assertion},
            success: loggedIn,
            error: function(xhr, status, err) {
                navigator.id.logout();
                alert("Login failure: " + err);
            }
        });
    },
    onlogout: function() {
        $.ajax({
            type: 'POST',
            url: '/auth/logout',
            success: loggedOut,
            error: function(xhr, status, err) { alert("Logout failure: " + err); }
        });
    }
});


function loggedIn(res, status, xhr) {
    $("#signin").hide();
    $("#signout").show();
}
function loggedOut(res, status, xhr) {
    $("#signin").show();
    $("#signout").hide();
}
