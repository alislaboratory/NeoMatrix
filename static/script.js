document.addEventListener('DOMContentLoaded', ()=> {
  const grid = document.getElementById('grid');
  const colorPicker = document.getElementById('colorPicker');

  // build 32×16 grid
  for(let y=0; y<16; y++){
    for(let x=0; x<32; x++){
      let cell = document.createElement('div');
      cell.classList.add('cell');
      cell.dataset.x = x;
      cell.dataset.y = y;
      cell.addEventListener('click', ()=> {
        let hex = colorPicker.value;
        let r = parseInt(hex.substr(1,2),16);
        let g = parseInt(hex.substr(3,2),16);
        let b = parseInt(hex.substr(5,2),16);
        fetch('/api/pixel', {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({ x,y,r,g,b,on:true })
        });
        cell.style.background = hex;
      });
      grid.appendChild(cell);
    }
  }

  // text form
  document.getElementById('textForm').addEventListener('submit', e=>{
    e.preventDefault();
    let txt = document.getElementById('textInput').value;
    fetch('/api/text', {
      method:'POST',
      headers:{'Content-Type':'application/x-www-form-urlencoded'},
      body: `text=${encodeURIComponent(txt)}`
    });
  });

  // default programs
  document.querySelectorAll('.progBtn').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      let prog = btn.dataset.prog;
      fetch('/api/program', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ program: prog })
      });
    });
  });

  // clear
  document.getElementById('clearBtn').addEventListener('click', ()=>{
    fetch('/api/clear', { method:'POST' });
    document.querySelectorAll('.cell').forEach(c=>c.style.background='#000');
  });

  // existing setup…
document.getElementById('startTicker').addEventListener('click', () => {
  const raw = document.getElementById('cryptoInput').value;
  const symbols = raw.split(',')
                     .map(s => s.trim())
                     .filter(s => s);
  const priceColor = document.getElementById('tickerPriceColor').value;
  if (symbols.length) {
    fetch('/api/crypto', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ symbols, price_color: priceColor })
    });
  }
});

});
