const letters = document.querySelectorAll('[data-initial]');
const letter = document.querySelector('#letter h1');
const glossaryIndex = document.querySelectorAll('.index menu li a');
const hamburgerMenu = document.querySelector('nav ul li');

const observer = new IntersectionObserver(entries => {
    entries.forEach((entry, index) => {
        if (entry.isIntersecting){
          letter.textContent = entry.target.attributes['data-initial'].value;
          glossaryIndex.forEach((glossary_item, index) => {
              if (glossaryIndex[index].textContent == letter.textContent){
                  glossaryIndex[index].style.color = 'red';
              } else {
                  glossaryIndex[index].style.color = '#FAFAFA';
              }
          })
        }
     })
  });

letters.forEach(letter => {
  observer.observe(letter);
})

function loadMenu() {
  const navMenu = `
     <div class="menu-window">
       <a href="" id="close">[X] Close</a>
       <menu>
         <li><a href="/about">About</a></li>
         <li><a href="/documentation">Documentation</a></li>
         <li><a href="/newsletter">Newsletter</a></li>
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
