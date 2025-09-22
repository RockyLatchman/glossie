const letters = document.querySelectorAll('[data-initial]');
const letter = document.querySelector('#letter h1');
const glossaryIndex = document.querySelectorAll('.index menu li a');

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
