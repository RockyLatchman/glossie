const letters = document.querySelectorAll('[data-initial]');
const letter = document.querySelector('#letter h1');
const glossaryIndex = document.querySelectorAll('.index menu li a');
const hamburgerMenu = document.querySelector('nav ul li');
const allEntries = document.querySelector('#all pre');
const randomEntry = document.querySelector('#random pre');
const searchTerm = document.querySelector('#search-term pre');
const searchLimit = document.querySelector('#limited-search pre');

const glossaryJSONData = [
    { 'url': '/api/list/all', 'elem': allEntries},
    { 'url': '/api/random-term', 'elem': randomEntry},
    { 'url': '/api/search/algorithm', 'elem': searchTerm},
    { 'url': '/api/list/limit/4', 'elem': searchLimit},
];

function glossaryDemo(){
  glossaryJSONData.forEach((item, index) => {
    fetch(item['url'])
      .then(response => response.json())
      .then(data => {
         item['elem'].textContent = JSON.stringify(data, null, 2);
      })
      .catch(error => console.error('Error fetching data:', error));
  })
}

const observer = new IntersectionObserver(entries => {
    entries.forEach((entry, index) => {
        if (entry.isIntersecting){
          letter.textContent = entry.target.attributes['data-initial'].value;
          setInitial(letter.textContent);
        }
     })
  });

letters.forEach(letter => {
  observer.observe(letter);
})

function setInitial(initial) {
  glossaryIndex.forEach((_, index) => {
      if (glossaryIndex[index].textContent == initial.toUpperCase()){
          glossaryIndex[index].style.color = 'red';
      } else {
          glossaryIndex[index].style.color = '#FAFAFA';
      }
  })
}

function loadMenu() {
  const navMenu = `
     <div class="menu-window">
       <a href="" id="close">[X] Close</a>
       <menu>
         <li><a href="/about">About</a></li>
         <li><a href="/documentation">Documentation</a></li>
         <li><a href="/subscribe">Subscribe</a></li>
       </menu>
     </div>
  `;
  // refactor this
  const template = document.createElement('template');
  template.innerHTML = navMenu;
  document.body.appendChild(template.content);
  document.querySelector('.menu-window').style.opacity = 0;
  // end
  document.querySelector('#close').addEventListener('click', (e) => {
      document.querySelector('.menu-window').setAttribute('id', 'menu-window');
  });
}

hamburgerMenu.addEventListener('click', (e) => {
   loadMenu();
})

document.addEventListener('DOMContentLoaded', (e) => {
   const initial = document.documentURI.charAt(document.documentURI.length - 1);
   setInitial(initial);
   glossaryDemo();
});
