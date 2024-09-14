function clearInput(){
    document.getElementById('searchTerm').value = "";
    document.getElementById('TopN').value = "";
    document.getElementById('suggestedTags').innerHTML= "";
    document.getElementById('results').innerHTML = "";
  }

function searchPosts(event) {
    event.preventDefault();
    const searchTerm = document.getElementById('searchTerm').value;
    const topN = document.getElementById('TopN').value;
    fetch('http://localhost:8001/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({searchTerm: searchTerm, topN: topN})
      })
      .then(response => response.text())
      .then(text => {
        // Replace panda NaN values with null
        const cleanText = text.replace(/NaN/g, 'null');
        return JSON.parse(cleanText);
      })
      .then(data => displayResults(data))
      .catch(error => console.log(error));
  }
  
function displayResults(info) {
    const results = document.getElementById('results');
    results.innerHTML = '';
    // add suggestes tag section
    const suggestedTags = document.getElementById('suggestedTags');
    suggestedTags.innerHTML = '';
    const tagHeader = document.createElement('div');
    tagHeader.classList.add('tags-header');
    tagHeader.innerHTML = `<h2>Suggested Tags:</h2>`;
    suggestedTags.appendChild(tagHeader);
    const tags = document.createElement('div');
    tags.classList.add('tag-bubbles');
    info['suggestedTags'].forEach(tag=>{
      tags.innerHTML += `<span class='tag'>${tag}</span>`;
    });
    suggestedTags.appendChild(tags);
    // add retrieved posts section
    const resultHeader = document.createElement('div');
    resultHeader.classList.add('tags-header');
    resultHeader.innerHTML = `<h2>Relevant Posts:</h2>`;
    results.appendChild(resultHeader)
    //posts.forEach(post => {
    Object.entries(info['posts']).forEach(([key, val]) => {
      title = val['Title'];
      content = val['Content'];
      tag = val['Tag'];
      docID = val['ID'];
      const postDiv = document.createElement('div');
      postDiv.classList.add('post');
      postDiv.innerHTML = `<h2>${title}</h2><p>ID: ${docID}</p><p>Tag: ${tag}</p><p>${content}</p>`;
      //postDiv.addEventListener('click', () => {
        //window.location.href = `https://www.reddit.com${post.data.permalink}`;
      //});
      results.appendChild(postDiv);
    });


  }
