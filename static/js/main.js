const letters = document.querySelectorAll('[data-initial]');
const letter = document.querySelector('#letter h1');
const glossaryIndex = document.querySelectorAll('.index menu li a');
const hamburgerMenu = document.querySelector('nav ul li');
const allEntries = document.querySelector('#all div pre');
const randomEntry = document.querySelector('#random div pre');
const searchTerm = document.querySelector('#search-term div pre');
const searchLimit = document.querySelector('#limited-search div pre');

const navMenu = `
   <div class="menu-window">
     <a href="" class="close">[X] Close</a>
     <menu>
       <li><a href="/about">About</a></li>
       <li><a href="/documentation">Documentation</a></li>
       <li><a href="#subscription" id="subscribe-button">Subscribe</a></li>
     </menu>
   </div>`;

const subscriptionHTML = `
  <div id="subscription">
      <a href="" class="close">[X]</a>
      <h3>Subscribe for what?</h3>
      <p>
        If you are learning to code you can subscribe to receive e-mails with
        daily tech terminology along with tips and tricks that will help you
        to be a better developer. In the future (perhaps by the time you read this),
        I will be adding diagrams and short videos to demo various concepts related
        to the terms you search.
      </p>
     <form method="POST" action="/subscribe">
         <input type="email" name="subscriber" placeholder="E-mail address" required>
         <input type="submit" value="Send">
     </form>
 </div>`;

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
      if (glossaryIndex[index].textContent == initial.toUpperCase()) {
         glossaryIndex[index].style.color = 'red';
      } else {
         glossaryIndex[index].style.color = '#FAFAFA';
      }
  })
}

function loadMenu() {
  const template = document.createElement('template');
  template.innerHTML = navMenu;
  document.body.appendChild(template.content);
  document.querySelector('.menu-window').style.opacity = 0;
  document.querySelector('.close').addEventListener('click', (e) => {
      document.querySelector('.menu-window').setAttribute('id', 'menu-window');
  });
  subscriptionModal();
}

function subscriptionModal() {
  const subscribeButton = document.querySelector('#subscribe-button');
  const overlay = document.createElement('div');
  overlay.setAttribute('id', 'overlay');
  subscribeButton.addEventListener('click', (e) => {
     document.querySelector('.menu-window').setAttribute('id', 'menu-window');
     const template = document.createElement('template');
     template.innerHTML = subscriptionHTML;
     overlay.appendChild(template.content);
     setTimeout((e) => {  document.body.appendChild(overlay) }, 800);
  })
}

function characterIdentifier(){
  let characterIdentifier = document.documentURI.charAt(document.documentURI.length - 2);
  if (characterIdentifier == '/') {
     let initial = document.documentURI.charAt(document.documentURI.length - 1);
     setInitial(initial);
  } else {
      setInitial('a');
  }
}

hamburgerMenu.addEventListener('click', (e) => {
   loadMenu();
})

document.addEventListener('DOMContentLoaded', (e) => {
   characterIdentifier();
   if (location.pathname == '/documentation') glossaryDemo();
});
