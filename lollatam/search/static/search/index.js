document.addEventListener('DOMContentLoaded', (e) => {

  const $searchBtn = document.getElementById('search-btn');
  $searchBtn.onclick = get_summoner_stats;

});

async function get_summoner_stats(e) {

  const summoner = document.getElementById('summoner').value;
  const server = document.getElementById('server').value;
  const url = `stats/${server}/${summoner}/`;

  const response = await fetch(url, {
    method: 'GET',
  });

  if (response.ok) {

    const accountStats = await response.json();
    console.log(accountStats);
    
  } else {

    const errorData = await response.json();
    console.log(errorData.message);
    
  }

}
