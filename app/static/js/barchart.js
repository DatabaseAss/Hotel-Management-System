var bchart = {
    // (A) HELPER FUNCTION - GENERATE RANDOM DARK COLOR
    // source: https://gist.github.com/Chak10/dc24c61c9bf2f651cb6d290eeef864c1
    rcolor : () => {
      let lum = -0.25, rgb = "#", c, i,
          hex = String("#" + Math.random().toString(16).slice(2, 8).toUpperCase()).replace(/[^0-9a-f]/gi, "");
      if (hex.length < 6) { hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2]; }
      for (i = 0; i < 3; i++) {
        c = parseInt(hex.substr(i * 2, 2), 16);
        c = Math.round(Math.min(Math.max(0, c + (c * lum)), 255)).toString(16);
        rgb += ("00" + c).substr(c.length);
      }
      return rgb;
    },
   
    // (B) DRAW BAR CHART
    draw : (instance) => {
      // (B1) INIT CHART CONTAINER
      let hor = instance.type=="h";
      instance.target.classList.add((hor ? "hbar" : "vbar"));
      instance.target.innerHTML = "";
   
      // (B2) GET LARGEST VALUE FROM DATA
      let largest = 0;
      instance.data.forEach(el => {
        if (el[1] > largest) { largest = el[1]; }
      });
   
      // (B3) DRAW CHART
      let bars = new DocumentFragment(), bar, percent;
      instance.data.forEach(el => {
        // (B3-1) CREATE <DIV> BAR
        bar = document.createElement("div");
        bars.appendChild(bar);
   
        // (B3-2) SET WIDTH/HEIGHT
        percent = Math.ceil((el[1] / largest) * 100) + "%";
        if (hor) { bar.style.width = percent; } else { bar.style.height = percent; }
   
        // (B3-3) BACKGROUND COLOR & TEXT
        bar.style.background = el[2] ? el[2] : bchart.rcolor();
        bar.innerHTML = el[0] + ": " + el[1];
      });
      instance.target.appendChild(bars);
    }
  };