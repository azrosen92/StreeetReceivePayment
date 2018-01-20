dwolla.configure('sandbox');
if (window.iavToken) {
  console.log("IAV Token: " + window.iavToken);
  dwolla.iav.start(window.iavToken, {
          container: 'iavContainer',
          stylesheets: [
            'http://fonts.googleapis.com/css?family=Lato&subset=latin,latin-ext',
          ],
          microDeposits: false,
          fallbackToMicroDeposits: true
        }, function(err, res) {
    console.log('Error: ' + JSON.stringify(err) + ' -- Response: ' + JSON.stringify(res));
    return JSON.stringify(res)
  });
} else {
  document.querySelector("#errorContainer").innerHTML = "Error: no IAV token"
}

