console.debug("loaded util.js")



    /*
        click -> sort
        click+shift -> add to sort
        click+ctrl -> toggle display
    */
    function ctrl_clk( event, elem, k ) {
        if ( null == event ) {
            changeClassCss( "." + k, 'display', 'none', 'block');
            elem.classList.toggle("ctrlDivDisabled");
        } else if ( event.shiftKey && event.ctrlKey ) {
            var k_ = k.startsWith("d_") ? k.substring(2) : k;
            changeClassCss( "." + k, 'display', 'none', 'none'); // enforce hidden
            elem.classList.toggle("ctrlDivGrouped");
            document.getElementById("sortKeys").value = (document.getElementById("sortKeys").value + " " + k_ + ":G").trim();
            sortDivElements();
        } else if ( event.ctrlKey ) {
            changeClassCss( "." + k, 'display', 'none', 'block');
            elem.classList.toggle("ctrlDivDisabled");
        } else if ( event.shiftKey ) {
            var k_ = k.startsWith("d_") ? k.substring(2) : k;
            document.getElementById("sortKeys").value = (document.getElementById("sortKeys").value + " " + k_).trim();
            sortDivElements();
        } else {
            var k_ = k.startsWith("d_") ? k.substring(2) : k;
            document.getElementById("sortKeys").value = k_;
            sortDivElements();
        }
    }






    //  changeClassCss( ".element", "display", "none");
    function changeClassCss( cssSelector, prop, val, val2 ) {
        const stylesheet = document.styleSheets[0];
        let elementRules = null;
        for(let i = 0; i < stylesheet.cssRules.length; i++) {
          if(stylesheet.cssRules[i].selectorText === cssSelector) {
            elementRules = stylesheet.cssRules[i];
            if (null != val2) {
               val = val == elementRules.style.getPropertyValue(prop) ? val2 : val;
            }
            elementRules.style.setProperty(prop, val);

          }
        }
        if (null == elementRules){
            stylesheet.insertRule( cssSelector + " {" + prop + ": " + val + "}", 1);
            stylesheet.addRule( cssSelector ,  prop + ": " + val , 1);
        }

    }
