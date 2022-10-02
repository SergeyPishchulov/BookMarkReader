let books_url = '/books';
let response = fetch(books_url);

let books = response.then((response) => {
    response.json().then((r)=>{
    for (const book of r){
        document.getElementById("bookList")
        .innerHTML+=`<li><a href="/reader/${book.id}">${book.title}</a></li>`;

}
    console.log(r)
})
  }); // читаем ответ в формате JSON

alert(books);