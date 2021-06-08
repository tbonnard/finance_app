document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('#variation').forEach(varia => {
        let qty = varia.dataset.qty;
        let average = varia.dataset.avg;
        let symbol = varia.dataset.symb;
        let stock_price = `/get_stock_price/${symbol}`
        fetch(stock_price)
        .then(response => response.json())
        .then(i => {
            let last_price=i.latestPrice
            let variation_perc = ((qty * last_price) - (qty * average)) / (qty * average) * 100;
            if (variation_perc >= 0) {
                varia.className = 'table_cell green'
            } else {
                varia.className = 'table_cell red'
            }
            varia.innerHTML = `${variation_perc.toFixed(2)}%`;
            varia.title = `$${last_price}`;
            document.querySelector(`#${symbol}`).innerHTML = `$${last_price}`;
            val = last_price * document.querySelector(`#value_${symbol}`).dataset.qty;
            document.querySelector(`#value_${symbol}`).innerHTML = `$${val.toFixed(2)} `;
        })
    })

});

