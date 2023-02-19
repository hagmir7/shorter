
if (!localStorage.getItem('urls')) {
    localStorage.setItem('urls', JSON.stringify({ urls: [] }));
};

async function sendLink(e) {

    const data = {
        url: document.getElementById('url-link').value
    }


    if (data.url.length > 5) {
        await fetch('{% url "link" %}', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)

        }).then(response => response.json()
        ).then(result => {
            document.getElementById('url-link').value = ""
            document.getElementById('list-links').insertAdjacentHTML("afterbegin", `
            <li class="list-group-item" >
                <div class="me-auto">
                    ${data.url.length > 50 ? data.url.slice(0, 50) + "..." : data.url}
                    <div class="fw-bold mb-2 bg-light rounded-pill p-1 mt-2 px-3 text-center border">${result.message}</div>
                </div>
                <div class="mt-2">
                    <button onclick="(copy(text-${result.id}))" class="btn btn-primary w-100 btn-sm rounded-pill">Copy</button>
                </div>
            </li>
        `)

            const old = JSON.parse(localStorage.getItem('urls')).urls;
            const newd = { oldurl: data.url, newurl: result.message, id: result.id }



            localStorage.setItem('urls', JSON.stringify({ urls: [...old, newd] }));

        }).catch(error => {
            console.log(error)
        })
    }
    


}


const data = JSON.parse(localStorage.getItem('urls')).urls;

if (data.length == 0) {
    document.getElementById('list-links').insertAdjacentHTML("afterbegin", '<h3 class="text-center py-3">No URLs</h3>');
}


data.map(item => {
    document.getElementById('list-links').insertAdjacentHTML("afterbegin",
        `<li class="list-group-item" >
            <div class="me-auto">
              ${item.oldurl.length > 50 ? item.oldurl.slice(0, 50) + "..." : item.oldurl}
              <div class="fw-bold mb-2 bg-light rounded-pill p-1 mt-1 px-3 text-center border" onclick="copy(${item.newurl})">${item.newurl}</div>
            </div>
            <div class="mt-2">
              <button onclick="(copy("${item.newurl}"))" class="btn btn-primary w-100 btn-sm rounded-pill">Copy</button>
            </div>
        </li> `
    )
});



function copy(text) {
    navigator.clipboard.writeText(text);
    alert("Copied the text: " + text);
};



const App = () => {
    return (
        <div class="col-lg-8">
            <h4>Shorten your link now!</h4>
            <p>Simplify your links and share more efficiently with our easy-to-use link shortener.</p>
            <form>
                <input type="text" id="url-link" name="url" placeholder="Shorten your link" />
                <input type="button" onclick="sendLink()" value="Shorten" />
            </form>
            <ul class="list-group mt-2 p-2 list-short-links" id="list-links">
                <li class="list-group-item">
                    <div class="me-auto">
                        <div class="fw-bold mb-2 bg-light rounded-pill p-1 px-3 text-center border">https://agmir.link/KDMIV</div>
                        https://www.freewsad.com/books
                    </div>
                    <div class="mt-2">
                        <button onclick="(copy(text-2))" class="btn btn-primary btn-sm rounded-pill">Copy</button>
                    </div>
                </li>
            </ul>
        </div>
    );
};


