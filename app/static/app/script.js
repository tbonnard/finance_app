document.addEventListener('DOMContentLoaded', function() {
    let symbols_all=[];
    // Store the data (Session, not locally, just in case there might be new symbols so at least, it might refresh the data more often than just locally)
    // To avoid too many calls to the API
    function initiateData() {
        if(sessionStorage.getItem("symbols_all")) {
            symbols_all = JSON.parse(sessionStorage.getItem("symbols_all"));
		}
        else {
            let url_list_symbol = "/get_symbols/";
            fetch(url_list_symbol)
            .then(response => response.json())
            .then(symbols => {
                symbols.forEach(i => {
                    symbols_all.push(i)
                    });
                store(symbols_all);
            })
            .catch(function(error) {
                const divsymbols_list = document.querySelector('#symbols_list');
                remove(divsymbols_list);
                const p = document.createElement('p');
                divsymbols_list.append(p);
                p.innerHTML = "Sorry, it seems there's an error with the API looking for companies. Please try again.";
                console.log(`Error --> ${error}`);
              })        
            }
    }

    function store(data) {
        sessionStorage.setItem('symbols_all', JSON.stringify(data));
    }

initiateData();

    function remove(parent){
        while(parent.firstChild){
            parent.removeChild(parent.firstChild);
        }
    }

    if (document.querySelector('#quote')) {
        document.querySelector('#quote').addEventListener('keyup', function () {
            const divsymbols_list = document.querySelector('#symbols_list');
            remove(divsymbols_list);
            let q = document.querySelector('#quote').value.toLowerCase();
            if (q.length == 1) {
                const divsymbols_list = document.querySelector('#symbols_list');
                remove(divsymbols_list);
                const p = document.createElement('p');
                p.className='info';
                divsymbols_list.append(p);
                p.innerHTML = `You must enter at least 2 characters.`;
            }
            if (q.length > 1) {
                var newArray = symbols_all.filter(i =>
                    i.name.toLowerCase().includes(q) );
                newArray.forEach( i => {
                    const div = document.createElement('div');
                    if( i.region != undefined || i.primaryExchange !=undefined)  {
                    div.innerHTML = `<a href='/symbol/${i.symbol}/'>${i.symbol}</a> - ${i.name} (${i.region} / (${i.primaryExchange}) `;
                    } else {
                        div.innerHTML = `<a href='/symbol/${i.symbol}/'>${i.symbol}</a> - ${i.name} `;
                    }
                    divsymbols_list.append(div);
                })
                if (newArray.length == 0) {
                    const divsymbols_list = document.querySelector('#symbols_list');
                    remove(divsymbols_list);
                    const p = document.createElement('p');
                    p.className='info';
                    divsymbols_list.append(p);
                    p.innerHTML = `No results for "${q}".`;
                } 
            }
        });
    }
    

    document.querySelectorAll('.logo').forEach(i => {
        i.onmouseover = function() {
            let a = Math.floor(Math.random() * 256);
            let b = Math.floor(Math.random() * 256);
            let c = Math.floor(Math.random() * 256);
            i.style.color = `rgb(${a}, ${b}, ${c})`;
        }
    })
    

    
    if (document.querySelector('#percent')) {
        document.querySelectorAll('#percent').forEach( i => {
            value = i.innerHTML;
            valuePercent = value * 100; 
            i.innerHTML = `${valuePercent.toFixed(2)}%`
        })

    }

});