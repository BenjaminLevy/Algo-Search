// Update this variable to point to your domain.
var apigatewayendpoint = 'https://wj7tdqfv2e.execute-api.us-east-1.amazonaws.com/test_0-0-0';
var loadingdiv = $('#loading');
var noresults = $('#noresults');
var resultdiv = $('#results');
var searchbox = $('input#search');
var timer = 0;

// Executes the search function 250 milliseconds after user stops typing
searchbox.keyup(function () {
  clearTimeout(timer);
  timer = setTimeout(search, 250);
});

async function search() {
  // Clear results before searching
  noresults.hide();
  resultdiv.empty();
  loadingdiv.show();
  // Get the query from the user
  let query = searchbox.val();
  // Only run a query if the string contains at least three characters
  if (query.length > 2) {
    // Make the HTTP request with the query as a parameter and wait for the JSON results
    let response = await $.get(apigatewayendpoint, { q: query, size: 25 }, 'json');
    // Get the part of the JSON response that we care about
    let results = response['hits']['hits'];
    if (results.length > 0) {
      loadingdiv.hide();
      // Iterate through the results and write them to HTML
      resultdiv.append('<p>Found ' + results.length + ' results.</p>');
      console.log(results[0])
      for (var item in results) {
        let url = results[item]._source.url;
        let title = results[item]._source.title_element;
        let body = results[item].highlight.body.join(" [...] ");
        let chapter_title = results[item]._source.chapter_title;
        // Construct the full HTML string that we want to append to the div
        resultdiv.append('<div class="result">' + '<div><a href="' + url + '"><h2>' + title + ' &ndash; ' +  chapter_title + '</h2><h3>' + url.slice(0,75) + '...</h3></a><p>' + body + '</p></div></div>');
      }
    } else {
      noresults.show();
    }
  }
  loadingdiv.hide();
}

// Tiny function to catch images that fail to load and replace them
function imageError(image) {
  image.src = 'images/no-image.png';
}
