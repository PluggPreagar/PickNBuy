console.debug("loaded util.js")


    var data_idx = 0;
    var keys_visible_default = " img img_lnk price ";

            function addData( responseText ) { // id img_lnk descr price hash
                console.debug( responseText );

                key_idx = 0 ; img_src_idx=1; img_lnk_idx=2; descr_idx=3; price_idx=4;
                var data = JSON.parse( responseText);
                var val = data;

                itm_div = '';
                data.priceVB = data.price.includes("VB") ? "VB":"";
                data.price = data.price.replace(" VB","");
                k="href";
                itm_div += '<a class="d_' + k + '" href="' + data[k] + '">';
                for ( var k in data ) {
                    if ( null == data[k] ) {
                    } else if ( "img" == k ) {
                        itm_div += '<img class="d_' + k + '" src="' + data[k] + '"/>';
                    } else if ( data[k].startsWith("http") ) {
                        // itm_div += '<a class="d_' + k + '" href="' + data[k] + '"></a>';
                    } else  {
                        itm_div += '<div class="d_' + k + '">' + data[k] + '</div>';
                    }
                    // console.debug( k + " -> " + data[k] );
                }
                itm_div += '</a>';
                /*
                itm_div = '';
                itm_div += '<a   class="d_href" href="' + val[img_lnk_idx] + '">"';
                itm_div += '<img class="d_img" src="' + val[img_src_idx] + '"/>';
                itm_div += '<div class="d_price">' + val[price_idx].replace(" VB","") + '</div>';
                itm_div += '<div class="d_priceVB">' + (val[price_idx].includes("VB") ? "VB":"") + '</div>';
                itm_div += '<div class="d_idx">' + val[key_idx] + '</div>';
                itm_div += '</a>';
                */
                //
                var newElement = document.createElement('div');
                newElement.classList.add("d_offer");
                newElement.classList.add("sortableDiv");
                newElement.innerHTML = itm_div;
                newElement.id = data['key'];
                document.getElementById("datas").appendChild(newElement);

                // add toggler
                for ( var k in data ) {
                    key = "ctrl_"+k;
                    if ( null == document.getElementById( key )) {
                        newElement = document.createElement('div');
                        newElement.id = key;
                        newElement.classList.add("ctrlDiv");
                        newElement.classList.add("button");
                        newElement.setAttribute("srcId","d_" + k );
                        newElement.setAttribute("onclick","ctrl_clk( event, this, 'd_" + k + "');");
                        // newElement.setAttribute("onclick","changeClassCss( '.d_" + k + "', 'display', 'none', 'block');");
                        newElement.innerHTML = k;
                        document.getElementById("ctrl").appendChild(newElement);
                        // preset ...
                        if ( !keys_visible_default.includes( " " + k + " " ) ) {
                            ctrl_clk( null, newElement, "d_" + k );
                        }
                    }
                }

            }

            /*
                click -> sort
                click+shift -> add to sort
                click+ctrl -> toggle display
            */
            function ctrl_clk( event, elem, k ) {
                if ( null == event || event.ctrlKey ) {
                    changeClassCss( "." + k, 'display', 'none', 'block');
                    elem.classList.toggle("ctrlDivDisabled");
                } else if ( event.shiftKey ) {
                    k_ = k.startsWith("d_") ? k.substring(2) : k;
                    document.getElementById("sortKeys").value = document.getElementById("sortKeys").value + " " + k_;
                    sortDivElements();
                } else {
                    k_ = k.startsWith("d_") ? k.substring(2) : k;
                    document.getElementById("sortKeys").value = k_;
                    sortDivElements();
                }
            }

            function pollData() {
                if (document.getElementById('liveUpdate').checked) {
                    var d = new Date();
                    var datestring = ("0" + d.getDate()).slice(-2) + "-" + ("0"+(d.getMonth()+1)).slice(-2) + "-" +
                            d.getFullYear() + " " + ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2) +
                            ":" + ("0" + d.getSeconds()).slice(-2);
                    document.getElementById('liveUpdateLabel').innerHTML="liveUpdate " + datestring;
                    var xhr = new XMLHttpRequest();
                    xhr.onreadystatechange = function() {
                        if (xhr.readyState === 4 && xhr.status === 200) {
                            addData( xhr.responseText);
                            data_idx=data_idx+1;
                            setTimeout(pollData, 10);
                        }
                    };
                    xhr.open("GET", "/json?idx=" + data_idx , true);
                    xhr.send();
                } // if liveUpdate
            }
            setInterval(pollData, 5000);






      function sortDivElements() {
        var container = document.getElementById("datas");
        var divList = Array.prototype.slice.call(container.getElementsByClassName("sortableDiv"));
        var sortKeys = (document.getElementById("sortKeys").value + " price").split(" ");
        for(let i = 0; i < sortKeys.length; i++) {
            if(!sortKeys[i].startsWith("d_")) {
                sortKeys[i] = "d_" +sortKeys[i];
            }
        }


        divList.sort(function (a, b) {
            for (let key of sortKeys) {
              if ("" != key) {
                var keyNum = key.includes(":n") || "d_price".includes( key );
                if (keyNum) {
                    key = key.replace(":n","");
                }
                var a_ = a.getElementsByClassName(key);
                var aKey = undefined == a_ || a_.length < 1 ? "" : a_[0].innerText;
                var b_ = b.getElementsByClassName(key);
                var bKey = undefined == b_ || b_.length < 1 ? "" : b_[0].innerText;
                if (aKey == bKey) {
                } else if (keyNum) {
                    aKey = aKey.replace(".","");
                    bKey = bKey.replace(".","");
                    return 1*aKey < 1*bKey ? -1 : 1 ;
                } else {
                    return aKey.localeCompare(bKey);
                } // diff
              } // key
            } // keys
            return 0; // If all keys are equal
        });

        container.innerHTML = "";
        for (var i = 0; i < divList.length; i++) {
          container.appendChild(divList[i]);
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